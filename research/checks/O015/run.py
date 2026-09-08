#!/usr/bin/env python3
"""O015 exact algebraic-class exhaustion. Never writes result.json."""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction as Q
from itertools import product
import json, os, subprocess, sys
from pathlib import Path
from typing import Iterable, Mapping

OID, MODEL = "O015", "openai/gpt-5.6-sol"
PASSED, FAILED, INCONCLUSIVE, ERROR = 0, 1, 2, 3
PREFIX, ETA = "##OBSERVATIONS##", (-1, 1, 1, 1, 1)
MUTATION = os.environ.get("O015_INTENTIONAL_MUTATION", "")
MUTATIONS = ("omit-polar-pair-order", "reverse-fiber-sign", "omit-coframe-companion",
             "premature-deltaK-zero", "all-plus-noether", "undeclared-exact-ibp-quotient")

def parity(w):
    if len(set(w)) != len(w): return 0
    return -1 if sum(w[i] > w[j] for i in range(len(w)) for j in range(i+1,len(w)))%2 else 1

def canon_word(atoms):
    a=list(atoms); s=1
    for i in range(len(a)):
        for j in range(len(a)-1-i):
            if a[j]>a[j+1]: a[j],a[j+1]=a[j+1],a[j]; s=-s
    return (0,()) if len(set(a))<len(a) else (s,tuple(a))

def diagrams(n=4):
    def rec(left):
        if not left: return [()]
        f,r=left[0],left[1:]; out=[(('V',f,-1),)+t for t in rec(r)]
        for p,o in enumerate(r): out += [(('eta',f,o),)+t for t in rec(r[:p]+r[p+1:])]
        return out
    return tuple(rec(tuple(range(n))))

class UnsupportedQuotient(ValueError): pass
class AlgebraicDomain:
    allowed={"V2=1","V.K=0","wedge","invariant-tensor"}
    def __init__(self, accept_undeclared=False):
        self.accept_undeclared=accept_undeclared
    def quotient(self, relation):
        if relation not in self.allowed and not self.accept_undeclared:
            raise UnsupportedQuotient("undeclared quotient: "+relation)

def eval_diagram(species,d):
    out={}
    for ix in product(range(5),repeat=4):
        q=Q(1)
        for k,i,j in d:
            q *= Q(ix[i]==4) if k=='V' else Q(ix[i]==ix[j])*ETA[ix[i]]
        if not q or any(s=='K' and ix[i]==4 for i,s in enumerate(species)): continue
        sign,w=canon_word(tuple((s,ix[i]) for i,s in enumerate(species)))
        if sign: out[w]=out.get(w,Q())+q*sign
    return {m:c for m,c in out.items() if c}

def eval_epsilon(species):
    out={}
    for ix in product(range(5),repeat=4):
        if any(s=='K' and ix[i]==4 for i,s in enumerate(species)): continue
        q=parity((4,)+ix)
        if not q: continue
        sign,w=canon_word(tuple((s,ix[i]) for i,s in enumerate(species)))
        if sign: out[w]=out.get(w,Q())+q*sign
    return {m:c for m,c in out.items() if c}

def rank(vectors):
    vectors=list(vectors); cols=sorted({k for v in vectors for k in v}); a=[[Q(v.get(k,0)) for k in cols] for v in vectors]; r=0
    for c in range(len(cols)):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]; z=a[r][c]; a[r]=[x/z for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]: z=a[i][c]; a[i]=[x-z*y for x,y in zip(a[i],a[r])]
        r+=1
    return r

def sector(species):
    ds=diagrams(); alg=[eval_diagram(species,d) for d in ds]; eps=eval_epsilon(species); vec=alg+[eps]
    return {"diagrams":len(ds),"candidates":len(vec),"nonzero":sum(bool(x) for x in vec),"rank":rank(vec),
            "eta_zero":all(not v for d,v in zip(ds,alg) if all(x[0]=='eta' for x in d)),
            "vleg_zero":all(not v for d,v in zip(ds,alg) if any(x[0]=='V' for x in d)),"epsilon":eps}

@dataclass(frozen=True,order=True)
class Atom:
    family:str; indices:tuple[int,...]=(); degree:int=0
    def label(self): return self.family+''.join(map(str,self.indices))
def A(f,*i,degree=0): return Atom(f,tuple(i),degree)

@dataclass(frozen=True)
class Poly:
    terms:tuple=()
    @staticmethod
    def scalar(v): v=Q(v); return Poly((((),v),)) if v else Poly()
    @staticmethod
    def atom(a): return Poly((((a,),Q(1)),))
    @staticmethod
    def collect(items):
        out={}
        for fs0,c0 in items:
            fs=list(fs0); c=Q(c0)
            for i in range(len(fs)):
                for j in range(len(fs)-1-i):
                    if fs[j]>fs[j+1]:
                        if fs[j].degree*fs[j+1].degree%2:c=-c
                        fs[j],fs[j+1]=fs[j+1],fs[j]
            if any(fs[i]==fs[i+1] and fs[i].degree%2 for i in range(len(fs)-1)): continue
            k=tuple(fs); out[k]=out.get(k,Q())+c
        return Poly(tuple(sorted((m,c) for m,c in out.items() if c)))
    def __add__(self,o): return Poly.collect(self.terms+o.terms)
    def __neg__(self): return Poly(tuple((m,-c) for m,c in self.terms))
    def __sub__(self,o): return self+-o
    def __mul__(self,o):
        if not isinstance(o,Poly): o=Poly.scalar(o)
        return Poly.collect((a+b,ca*cb) for a,ca in self.terms for b,cb in o.terms)
    __rmul__=__mul__
    @property
    def is_zero(self): return not self.terms
    def coefficient(self,marker):
        out=Poly()
        for fs,c in self.terms:
            if fs.count(marker)!=1: continue
            p=fs.index(marker); sign=-1 if marker.degree*sum(x.degree for x in fs[:p])%2 else 1
            out += Poly(((fs[:p]+fs[p+1:],c*sign),))
        return out
    def substitute(self,mapping:Mapping):
        out=Poly()
        for fs,c in self.terms:
            t=Poly.scalar(c)
            for a in fs:
                r=mapping.get(a,Poly.atom(a)); t*=r if isinstance(r,Poly) else Poly.scalar(r)
            out+=t
        return out
    def text(self): return '0' if self.is_zero else '+'.join(f'{c}*'+'^'.join(a.label() for a in m) for m,c in self.terms)
def psum(xs):
    o=Poly()
    for x in xs:o+=x
    return o

@dataclass(frozen=True)
class Expr:
    op:str; args:tuple=(); leaf:Atom|None=None; coefficient:Q=Q(1)
    @staticmethod
    def atom(a):return Expr('atom',leaf=a)
    @staticmethod
    def scalar(v):return Expr('scalar',coefficient=Q(v))
    def __add__(self,o):return Expr('add',(self,o))
    def __mul__(self,o):return Expr('mul',(self,o if isinstance(o,Expr) else Expr.scalar(o)))
    __rmul__=__mul__
    def compile(self):
        if self.op=='atom': return Poly.atom(self.leaf)
        if self.op=='scalar': return Poly.scalar(self.coefficient)
        if self.op=='add': return self.args[0].compile()+self.args[1].compile()
        if self.op=='mul': return self.args[0].compile()*self.args[1].compile()
        raise ValueError(self.op)
def esum(xs):
    o=Expr.scalar(0)
    for x in xs:o=o+x
    return o
def X(f,i,d):return Expr.atom(A(f,i,degree=d))
def dW(i,j):
    if i==j:return Expr.scalar(0)
    return Expr.atom(A('dW',min(i,j),max(i,j),degree=1))*(1 if i<j else -1)

def graph():
    l,g=Expr.atom(A('lambda')),Expr.atom(A('gamma'))
    i0=Q(1,24)*esum(Expr.scalar(e)*X('V',a,0)*X('E',b,1)*X('E',c,1)*X('E',d,1)*X('E',f,1)
        for a,b,c,d,f in product(range(5),repeat=5) if (e:=parity((a,b,c,d,f))))
    i1=Q(1,6)*esum(Expr.scalar(e)*X('V',a,0)*X('K',b,1)*X('E',c,1)*X('E',d,1)*X('E',f,1)
        for a,b,c,d,f in product(range(5),repeat=5) if (e:=parity((a,b,c,d,f))))
    return l*i0+g*i1

def delta_leaf(a,omit_e,freeze_k):
    f,i=a.family,a.indices
    if f=='V':return X('dV',i[0],0)
    if f=='E':return Expr.scalar(0) if omit_e else X('dE',i[0],1)
    if f=='K':
        if freeze_k:return Expr.scalar(0)
        return X('DKdV',i[0],1)+esum(ETA[c]*dW(i[0],c)*X('V',c,0) for c in range(5))
    return Expr.scalar(0)
def vary(e,omit_e=False,freeze_k=False):
    if e.op=='atom':return delta_leaf(e.leaf,omit_e,freeze_k)
    if e.op=='scalar':return Expr.scalar(0)
    if e.op=='add':return vary(e.args[0],omit_e,freeze_k)+vary(e.args[1],omit_e,freeze_k)
    if e.op=='mul':return vary(e.args[0],omit_e,freeze_k)*e.args[1]+e.args[0]*vary(e.args[1],omit_e,freeze_k)
    raise ValueError(e.op)

def covd(p):
    out=Poly()
    for fs,c in p.terms:
        for i,a in enumerate(fs):
            der=Poly.atom(A('K',a.indices[0],degree=1)) if a.family=='V' else Poly.atom(A('DE',a.indices[0],degree=2)) if a.family=='E' else Poly()
            if der.is_zero:continue
            t=Poly.scalar(c*(-1 if sum(x.degree for x in fs[:i])%2 else 1))
            for j,b in enumerate(fs):t*=der if i==j else Poly.atom(b)
            out+=t
    return out
def ibp(raw):
    bulk,corner=Poly(),Poly()
    for fs,c0 in raw.terms:
        ms=[x for x in fs if x.family=='DKdV']
        if not ms:bulk+=Poly(((fs,c0),));continue
        if len(ms)!=1:raise ValueError('nonlinear D(delta V)')
        m=ms[0]; p=fs.index(m); c=c0*(-1 if sum(x.degree for x in fs[:p])%2 else 1); q=Poly(((fs[:p]+fs[p+1:],Q(1)),)); dv=Poly.atom(A('dV',m.indices[0]))
        corner+=c*dv*q; bulk+=-c*dv*covd(q)
    return bulk,corner

def pi(a,b):
    return Q(1,12)*psum(Poly.scalar(e)*Poly.atom(A('E',c,degree=1))*Poly.atom(A('E',d,degree=1))*Poly.atom(A('E',f,degree=1))
        for c,d,f in product(range(5),repeat=3) if (e:=parity((a,b,c,d,f))))
def expected_rows():
    g,l=Poly.atom(A('gamma')),Poly.atom(A('lambda')); ow={}
    for i in range(5):
      for j in range(i+1,5):
        z=Q(1,6)*g*psum(Poly.scalar(e*ETA[c])*Poly.atom(A('V',a))*dW(b,c).compile()*Poly.atom(A('V',c))*Poly.atom(A('E',d,degree=1))*Poly.atom(A('E',f,degree=1))*Poly.atom(A('E',h,degree=1))
            for a,b,c,d,f,h in product(range(5),repeat=6) if (e:=parity((a,b,d,f,h))))
        ow[i,j]=z.coefficient(A('dW',i,j,degree=1))
    er={}
    for c in range(5):
        w=Q(1,6)*psum(Poly.scalar(e)*Poly.atom(A('V',a))*Poly.atom(A('E',d,degree=1))*Poly.atom(A('E',f,degree=1))*Poly.atom(A('E',h,degree=1)) for a,d,f,h in product(range(5),repeat=4) if (e:=parity((a,c,d,f,h))))
        j=Q(-1,2)*psum(Poly.scalar(e)*Poly.atom(A('V',a))*Poly.atom(A('K',b,degree=1))*Poly.atom(A('E',d,degree=1))*Poly.atom(A('E',f,degree=1)) for a,b,d,f in product(range(5),repeat=4) if (e:=parity((a,b,c,d,f))))
        er[c]=l*w+g*j
    vr={}; cr={}
    for a in range(5):
        u=Q(1,24)*psum(Poly.scalar(e)*Poly.atom(A('E',b,degree=1))*Poly.atom(A('E',c,degree=1))*Poly.atom(A('E',d,degree=1))*Poly.atom(A('E',f,degree=1)) for b,c,d,f in product(range(5),repeat=4) if (e:=parity((a,b,c,d,f))))
        h=2*psum(Poly.atom(A('V',b))*covd(pi(a,b))+2*Poly.atom(A('K',b,degree=1))*pi(a,b) for b in range(5))
        vr[a]=l*u+g*h; cr[a]=-2*g*psum(Poly.atom(A('V',b))*pi(a,b) for b in range(5))
    return ow,er,vr,cr
def alpha(a,b):
    if a==b:return Poly()
    return ETA[b]*(1 if a<b else -1)*Poly.atom(A('alpha',min(a,b),max(a,b)))
def noether(ow,er,vr,wrong=False):
    x=psum(Poly.atom(A('alpha',i,j))*covd(ow[i,j]) for i in range(5) for j in range(i+1,5))
    e=psum((er[a]*alpha(a,b)*Poly.atom(A('E',b,degree=1)) if wrong else alpha(a,b)*Poly.atom(A('E',b,degree=1))*er[a]) for a in range(5) for b in range(5))
    v=psum(vr[a]*alpha(a,b)*Poly.atom(A('V',b)) for a in range(5) for b in range(5))
    return x+e+v

def polar(root,bulk,corner,mutation):
    z=Poly(); x=[Poly.atom(A('x',i,degree=1)) for i in range(3)]; th=Poly.atom(A('theta',degree=1)); c=Poly.atom(A('c')); tau=Poly.atom(A('tau')); g=Poly.atom(A('gamma')); ki=Poly.atom(A('kappa5_inv')); dc=Poly.atom(A('dchi'))
    val={A('V',i):Q(i==4) for i in range(5)}; val.update({A('E',i,degree=1):(x[i] if i<3 else z) for i in range(5)}); val.update({A('K',i,degree=1):(-c*th if i==3 else z) for i in range(5)})
    action=root.compile().substitute(val); pv={(a,b):pi(a,b).substitute(val) for a in range(5) for b in range(5)}
    base=dict(val); base.update({A('dW',i,j,degree=1):z for i in range(5) for j in range(i+1,5)}); base.update({A('dE',i,degree=1):z for i in range(5)}); base.update({A('dV',i):z for i in range(5)}); base[A('dW',3,4,degree=1)]=-dc*th
    prim=bulk.substitute(base); d004=Poly(); orders=[(4,3),(3,4)] if mutation!='omit-polar-pair-order' else [(4,3)]
    for a,b in orders:d004+=ki*(dc*th if (a,b)==(4,3) else -dc*th)*pv[a,b]
    al=Poly.atom(A('scale')); sm=dict(val); sm.update({A('dW',i,j,degree=1):z for i in range(5) for j in range(i+1,5)}); sm.update({A('dV',i):z for i in range(5)}); sm.update({A('dE',i,degree=1):(al*x[i] if i<3 else z) for i in range(5)}); scale=bulk.substitute(sm)
    tm=dict(val); tm.update({A('dW',i,j,degree=1):z for i in range(5) for j in range(i+1,5)}); tm.update({A('dV',i):z for i in range(5)}); tm.update({A('dE',i,degree=1):(th if i==3 else z) for i in range(5)}); trans=bulk.substitute(tm)
    ders={A('DE',i,degree=2):z for i in range(5)}; vv=[bulk.coefficient(A('dV',i)).substitute(val).substitute(ders) for i in range(5)]
    pb=dict(val); pb[A('x',2,degree=1)]=z; pb.update({A('dV',i):Poly.atom(A('cornerV',i)) for i in range(5)}); cp=corner.substitute(pb).substitute({A('x',2,degree=1):z})
    sign=-1 if mutation=='reverse-fiber-sign' else 1
    # Canonical Atom ordering places theta before x0,x1,x2.  Fiber integration
    # is defined with the fiber leg moved right, so extracting theta from a
    # horizontal-three-form product contributes the required additional minus.
    integ=lambda p:-sign*tau*p.substitute({A('theta',degree=1):Poly.scalar(1)})
    return {"action":action,"p43":pv[4,3],"p34":pv[3,4],"mixed":integ(d004+prim),"scale":integ(scale),"trans":integ(trans),"v":vv,"corner":cp,
      "em":tau*(ki-g)*dc*x[0]*x[1]*x[2],"es":-3*tau*g*c*al*x[0]*x[1]*x[2],"et":tau*Poly.atom(A('lambda'))*x[0]*x[1]*x[2],"orientation":x[0]*x[1]*x[2]*th}

@dataclass
class Recorder:
    results:dict[str,bool]=field(default_factory=dict)
    def require(self,n,c):
        if n in self.results or type(c) is not bool:raise ValueError(n)
        self.results[n]=c
    @property
    def failed(self):return sorted(k for k,v in self.results.items() if not v)

def evaluate(mutation):
    if mutation and mutation not in MUTATIONS:raise ValueError('unsupported mutation')
    r=Recorder(); rejected=False
    # The semantic mutation corrupts the domain boundary upstream: its API
    # wrongly accepts the forbidden action quotient.  The ordinary positive
    # rejection assertion below then detects the changed behavior.
    domain=AlgebraicDomain(accept_undeclared=(mutation=='undeclared-exact-ibp-quotient'))
    try:domain.quotient('total-derivative/IBP')
    except UnsupportedQuotient:rejected=True
    r.require('domain.undeclared_IBP_quotient_rejected',rejected)
    s0,s1,s2=sector(('E',)*4),sector(('K','E','E','E')),sector(('K','K','E','E'))
    i0_normal={m:c/Q(24) for m,c in s0['epsilon'].items()}; i1_normal={m:c/Q(6) for m,c in s1['epsilon'].items()}
    r.require('class.generated_counts',(s0['candidates'],s1['candidates'])==(11,11)); r.require('class.ranks_1_1',(s0['rank'],s1['rank'])==(1,1)); r.require('class.eta_only_zero',s0['eta_zero'] and s1['eta_zero']); r.require('class.VE_zero',s0['vleg_zero'] and s1['vleg_zero']); r.require('class.I0_normalization',len(i0_normal)==1 and all(abs(c)==1 for c in i0_normal.values())); r.require('class.I1_normalization',len(i1_normal)==4 and all(abs(c)==1 for c in i1_normal.values())); r.require('class.twoK_boundary_rank_changes',s2['rank']>1)
    root=graph(); raw=vary(root,mutation=='omit-coframe-companion',mutation=='premature-deltaK-zero').compile(); bulk,corner=ibp(raw); ew,ee,ev,ec=expected_rows(); rw={(i,j):bulk.coefficient(A('dW',i,j,degree=1)) for i in range(5) for j in range(i+1,5)}; re={i:bulk.coefficient(A('dE',i,degree=1)) for i in range(5)}; rv={i:bulk.coefficient(A('dV',i)) for i in range(5)}; rc={i:corner.coefficient(A('dV',i)) for i in range(5)}
    r.require('variation.connection_rows',rw==ew); r.require('variation.coframe_rows',re==ee); r.require('variation.V_rows',rv==ev); r.require('variation.minus_corner',rc==ec and not corner.is_zero); r.require('variation.corrected_noether',noether(rw,re,rv,mutation=='all-plus-noether').is_zero); r.require('variation.all_plus_nonzero',not noether(ew,ee,ev,True).is_zero)
    p=polar(root,bulk,corner,mutation); g,c=Poly.atom(A('gamma')),Poly.atom(A('c'))
    osigma=Poly.atom(A('x',0,degree=1))*Poly.atom(A('x',1,degree=1))*Poly.atom(A('x',2,degree=1))
    r.require('polar.I0_zero_and_I1_minus_c',p['action']==-g*c*p['orientation']); r.require('polar.P43',p['p43']==Q(-1,2)*osigma); r.require('polar.P34',p['p34']==Q(1,2)*osigma); r.require('polar.mixed',p['mixed']==p['em']); r.require('polar.scale',p['scale']==p['es']); r.require('polar.transverse_E',p['trans']==p['et']); r.require('polar.transverse_V',all(x.is_zero for x in p['v'][:4])); r.require('polar.longitudinal_control',not p['v'][4].is_zero); r.require('polar.corner_pullback',p['corner'].is_zero)
    # Divide the rescaling equation only by the stipulated nonzero c.  In
    # unknowns (gamma,kappa5_inv), the exact rows gamma-kappa5_inv=0 and
    # gamma=0 have rank two and force kappa5_inv=0, contradicting the declared
    # finite nonzero kappa5.  Coframe rows in (lambda,gamma) are independent.
    decisive=[{"gamma":Q(1),"kappa5_inv":Q(-1)},{"gamma":Q(1)}]
    coframe=[{"lambda":Q(1)},{"gamma":Q(1)}]
    r.require('coefficients.decisive_rows_rank_two',rank(decisive)==2)
    r.require('coefficients.force_forbidden_kappa5_inv_zero',rank(decisive)==2 and decisive[0]["kappa5_inv"]!=0)
    r.require('coefficients.complete_coframe_rank_two',rank(coframe)==2)
    return r,{"mutation":mutation or None,"class":{"generated_diagrams":[s0['diagrams'],s1['diagrams']],"generated_candidates":[s0['candidates'],s1['candidates']],"nonzero":[s0['nonzero'],s1['nonzero']],"ranks":[s0['rank'],s1['rank']],"twoK_rank":s2['rank'],"basis":["epsilon(V,E,E,E,E)/24","epsilon(V,K,E,E,E)/6"]},"variation":{"root":"lambda*I0+gamma*I1 epsilon graph","raw_terms":len(raw.terms),"bulk_terms":len(bulk.terms),"corner_terms":len(corner.terms),"deltaK":"D(delta V)+delta omega V","action_IBP_quotient":not rejected,"undeclared_quotient_rejected":rejected},"polar":{"I0":"0","I1":"-c*oSigma*dtheta","sparse_action_theta_first_canonical":p['action'].text(),"action_fiber_right_geometric":"-gamma*c*oSigma*dtheta","mixed":"tau*(kappa5_inv-gamma)","rescaling":"-3*tau*gamma*c","transverse_E":"tau*lambda","tau":"formal 2*pi","corner":p['corner'].text()}}

def emit(x):print(PREFIX+' '+json.dumps(x,sort_keys=True,allow_nan=False,default=str))
def check():
    r,d=evaluate(MUTATION); runs={}
    if not MUTATION:
        for m in MUTATIONS:
            env=dict(os.environ);env['O015_INTENTIONAL_MUTATION']=m;p=subprocess.run([sys.executable,str(Path(__file__).resolve())],env=env,capture_output=True,text=True,check=False);runs[m]={"exit_code":p.returncode,"detected":p.returncode==FAILED};r.require('mutation_process.'+m,p.returncode==FAILED)
    f=r.failed;emit({"obligation_id":OID,"producer_model":MODEL,"infrastructure_producer_models":[MODEL],"representation_and_trust":{"domain":"generated eta/epsilon/V contraction orbits and exact graded variation","coefficient_ring":"integers/Fraction","normal_form":"canonical sparse maps and exact RREF","generator_premise_trusted":"SO(1,4) invariant tensors generated by eta,epsilon; epsilon^2 reduces to eta determinant","adapted_frame":"V=e4 represents the unit-spacelike orbit; residual stabilizer count is covariant","arbitrary_V":"V2, V.K, repeated-V epsilon, and explicit V.E legs","CAS":False,"floating_point":False,"random_sampling":False,"action_IBP_quotient":MUTATION=='undeclared-exact-ibp-quotient'},"details":d,"mutation_processes":runs,"assertions":{"total":len(r.results),"passed":len(r.results)-len(f),"failed":len(f),"failed_names":f}})
    if f:
        for n in f:print('FAILED: '+n,file=sys.stderr)
        return FAILED
    return PASSED
def main():
    try:return check()
    except (ValueError,KeyError,AssertionError) as e:emit({"obligation_id":OID,"producer_model":MODEL,"inconclusive_reason":str(e)});return INCONCLUSIVE
    except Exception as e:print(f'{OID} execution error: {e!r}',file=sys.stderr);return ERROR
if __name__=='__main__':raise SystemExit(main())
