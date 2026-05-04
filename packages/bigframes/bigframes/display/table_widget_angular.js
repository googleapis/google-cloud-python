// dist/table-widget-angular/browser/main.js
var dc = Object.defineProperty;
var fc = Object.defineProperties;
var pc = Object.getOwnPropertyDescriptors;
var ni = Object.getOwnPropertySymbols;
var hc = Object.prototype.hasOwnProperty;
var gc = Object.prototype.propertyIsEnumerable;
var ri = (e6, t, n) => t in e6 ? dc(e6, t, { enumerable: true, configurable: true, writable: true, value: n }) : e6[t] = n;
var A = (e6, t) => {
  for (var n in t ||= {})
    hc.call(t, n) && ri(e6, n, t[n]);
  if (ni)
    for (var n of ni(t))
      gc.call(t, n) && ri(e6, n, t[n]);
  return e6;
};
var B = (e6, t) => fc(e6, pc(t));
var S = null;
var Ft = false;
var Wn = 1;
var mc = null;
var G = Symbol("SIGNAL");
function y(e6) {
  let t = S;
  return S = e6, t;
}
function Lt() {
  return S;
}
var Pt = { version: 0, lastCleanEpoch: 0, dirty: false, producers: void 0, producersTail: void 0, consumers: void 0, consumersTail: void 0, recomputing: false, consumerAllowSignalWrites: false, consumerIsAlwaysLive: false, kind: "unknown", producerMustRecompute: () => false, producerRecomputeValue: () => {
}, consumerMarkedDirty: () => {
}, consumerOnSignalRead: () => {
} };
function oi(e6) {
  if (Ft)
    throw new Error("");
  if (S === null)
    return;
  S.consumerOnSignalRead(e6);
  let t = S.producersTail;
  if (t !== void 0 && t.producer === e6)
    return;
  let n, r = S.recomputing;
  if (r && (n = t !== void 0 ? t.nextProducer : S.producers, n !== void 0 && n.producer === e6)) {
    S.producersTail = n, n.lastReadVersion = e6.version;
    return;
  }
  let o = e6.consumersTail;
  if (o !== void 0 && o.consumer === S && (!r || Dc(o, S)))
    return;
  let i = Me(S), s = { producer: e6, consumer: S, nextProducer: n, prevConsumer: o, lastReadVersion: e6.version, nextConsumer: void 0 };
  S.producersTail = s, t !== void 0 ? t.nextProducer = s : S.producers = s, i && li(e6, s);
}
function ii() {
  Wn++;
}
function si(e6) {
  if (!(Me(e6) && !e6.dirty) && !(!e6.dirty && e6.lastCleanEpoch === Wn)) {
    if (!e6.producerMustRecompute(e6) && !Qn(e6)) {
      Gn(e6);
      return;
    }
    e6.producerRecomputeValue(e6), Gn(e6);
  }
}
function qn(e6) {
  if (e6.consumers === void 0)
    return;
  let t = Ft;
  Ft = true;
  try {
    for (let n = e6.consumers; n !== void 0; n = n.nextConsumer) {
      let r = n.consumer;
      r.dirty || yc(r);
    }
  } finally {
    Ft = t;
  }
}
function Zn() {
  return S?.consumerAllowSignalWrites !== false;
}
function yc(e6) {
  e6.dirty = true, qn(e6), e6.consumerMarkedDirty?.(e6);
}
function Gn(e6) {
  e6.dirty = false, e6.lastCleanEpoch = Wn;
}
function Yn(e6) {
  return e6 && ai(e6), y(e6);
}
function ai(e6) {
  e6.producersTail = void 0, e6.recomputing = true;
}
function ci(e6, t) {
  y(t), e6 && ui(e6);
}
function ui(e6) {
  e6.recomputing = false;
  let t = e6.producersTail, n = t !== void 0 ? t.nextProducer : e6.producers;
  if (n !== void 0) {
    if (Me(e6))
      do
        n = Kn(n);
      while (n !== void 0);
    t !== void 0 ? t.nextProducer = void 0 : e6.producers = void 0;
  }
}
function Qn(e6) {
  for (let t = e6.producers; t !== void 0; t = t.nextProducer) {
    let n = t.producer, r = t.lastReadVersion;
    if (r !== n.version || (si(n), r !== n.version))
      return true;
  }
  return false;
}
function jt(e6) {
  if (Me(e6)) {
    let t = e6.producers;
    for (; t !== void 0; )
      t = Kn(t);
  }
  e6.producers = void 0, e6.producersTail = void 0, e6.consumers = void 0, e6.consumersTail = void 0;
}
function li(e6, t) {
  let n = e6.consumersTail, r = Me(e6);
  if (n !== void 0 ? (t.nextConsumer = n.nextConsumer, n.nextConsumer = t) : (t.nextConsumer = void 0, e6.consumers = t), t.prevConsumer = n, e6.consumersTail = t, !r)
    for (let o = e6.producers; o !== void 0; o = o.nextProducer)
      li(o.producer, o);
}
function Kn(e6) {
  let t = e6.producer, n = e6.nextProducer, r = e6.nextConsumer, o = e6.prevConsumer;
  if (e6.nextConsumer = void 0, e6.prevConsumer = void 0, r !== void 0 ? r.prevConsumer = o : t.consumersTail = o, o !== void 0)
    o.nextConsumer = r;
  else if (t.consumers = r, !Me(t)) {
    let i = t.producers;
    for (; i !== void 0; )
      i = Kn(i);
  }
  return n;
}
function Me(e6) {
  return e6.consumerIsAlwaysLive || e6.consumers !== void 0;
}
function di(e6) {
  mc?.(e6);
}
function Dc(e6, t) {
  let n = t.producersTail;
  if (n !== void 0) {
    let r = t.producers;
    do {
      if (r === e6)
        return true;
      if (r === n)
        break;
      r = r.nextProducer;
    } while (r !== void 0);
  }
  return false;
}
function fi(e6, t) {
  return Object.is(e6, t);
}
function vc() {
  throw new Error();
}
var pi = vc;
function hi(e6) {
  pi(e6);
}
function Jn(e6) {
  pi = e6;
}
var Ec = null;
function Xn(e6, t) {
  let n = Object.create(yi);
  n.value = e6, t !== void 0 && (n.equal = t);
  let r = () => gi(n);
  return r[G] = n, di(n), [r, (s) => er(n, s), (s) => mi(n, s)];
}
function gi(e6) {
  return oi(e6), e6.value;
}
function er(e6, t) {
  Zn() || hi(e6), e6.equal(e6.value, t) || (e6.value = t, Ic(e6));
}
function mi(e6, t) {
  Zn() || hi(e6), er(e6, t(e6.value));
}
var yi = B(A({}, Pt), { equal: fi, value: void 0, kind: "signal" });
function Ic(e6) {
  e6.version++, ii(), qn(e6), Ec?.(e6);
}
function N(e6) {
  return typeof e6 == "function";
}
function Bt(e6) {
  let n = e6((r) => {
    Error.call(r), r.stack = new Error().stack;
  });
  return n.prototype = Object.create(Error.prototype), n.prototype.constructor = n, n;
}
var Vt = Bt((e6) => function(n) {
  e6(this), this.message = n ? `${n.length} errors occurred during unsubscription:
${n.map((r, o) => `${o + 1}) ${r.toString()}`).join(`
  `)}` : "", this.name = "UnsubscriptionError", this.errors = n;
});
function Ke(e6, t) {
  if (e6) {
    let n = e6.indexOf(t);
    0 <= n && e6.splice(n, 1);
  }
}
var b = class e {
  constructor(t) {
    this.initialTeardown = t, this.closed = false, this._parentage = null, this._finalizers = null;
  }
  unsubscribe() {
    let t;
    if (!this.closed) {
      this.closed = true;
      let { _parentage: n } = this;
      if (n)
        if (this._parentage = null, Array.isArray(n))
          for (let i of n)
            i.remove(this);
        else
          n.remove(this);
      let { initialTeardown: r } = this;
      if (N(r))
        try {
          r();
        } catch (i) {
          t = i instanceof Vt ? i.errors : [i];
        }
      let { _finalizers: o } = this;
      if (o) {
        this._finalizers = null;
        for (let i of o)
          try {
            Di(i);
          } catch (s) {
            t = t ?? [], s instanceof Vt ? t = [...t, ...s.errors] : t.push(s);
          }
      }
      if (t)
        throw new Vt(t);
    }
  }
  add(t) {
    var n;
    if (t && t !== this)
      if (this.closed)
        Di(t);
      else {
        if (t instanceof e) {
          if (t.closed || t._hasParent(this))
            return;
          t._addParent(this);
        }
        (this._finalizers = (n = this._finalizers) !== null && n !== void 0 ? n : []).push(t);
      }
  }
  _hasParent(t) {
    let { _parentage: n } = this;
    return n === t || Array.isArray(n) && n.includes(t);
  }
  _addParent(t) {
    let { _parentage: n } = this;
    this._parentage = Array.isArray(n) ? (n.push(t), n) : n ? [n, t] : t;
  }
  _removeParent(t) {
    let { _parentage: n } = this;
    n === t ? this._parentage = null : Array.isArray(n) && Ke(n, t);
  }
  remove(t) {
    let { _finalizers: n } = this;
    n && Ke(n, t), t instanceof e && t._removeParent(this);
  }
};
b.EMPTY = (() => {
  let e6 = new b();
  return e6.closed = true, e6;
})();
var tr = b.EMPTY;
function Ht(e6) {
  return e6 instanceof b || e6 && "closed" in e6 && N(e6.remove) && N(e6.add) && N(e6.unsubscribe);
}
function Di(e6) {
  N(e6) ? e6() : e6.unsubscribe();
}
var V = { onUnhandledError: null, onStoppedNotification: null, Promise: void 0, useDeprecatedSynchronousErrorHandling: false, useDeprecatedNextContext: false };
var _e = { setTimeout(e6, t, ...n) {
  let { delegate: r } = _e;
  return r?.setTimeout ? r.setTimeout(e6, t, ...n) : setTimeout(e6, t, ...n);
}, clearTimeout(e6) {
  let { delegate: t } = _e;
  return (t?.clearTimeout || clearTimeout)(e6);
}, delegate: void 0 };
function vi(e6) {
  _e.setTimeout(() => {
    let { onUnhandledError: t } = V;
    if (t)
      t(e6);
    else
      throw e6;
  });
}
function nr() {
}
var Ei = rr("C", void 0, void 0);
function Ii(e6) {
  return rr("E", void 0, e6);
}
function Ci(e6) {
  return rr("N", e6, void 0);
}
function rr(e6, t, n) {
  return { kind: e6, value: t, error: n };
}
var de = null;
function Se(e6) {
  if (V.useDeprecatedSynchronousErrorHandling) {
    let t = !de;
    if (t && (de = { errorThrown: false, error: null }), e6(), t) {
      let { errorThrown: n, error: r } = de;
      if (de = null, n)
        throw r;
    }
  } else
    e6();
}
function wi(e6) {
  V.useDeprecatedSynchronousErrorHandling && de && (de.errorThrown = true, de.error = e6);
}
var fe = class extends b {
  constructor(t) {
    super(), this.isStopped = false, t ? (this.destination = t, Ht(t) && t.add(this)) : this.destination = Tc;
  }
  static create(t, n, r) {
    return new be(t, n, r);
  }
  next(t) {
    this.isStopped ? ir(Ci(t), this) : this._next(t);
  }
  error(t) {
    this.isStopped ? ir(Ii(t), this) : (this.isStopped = true, this._error(t));
  }
  complete() {
    this.isStopped ? ir(Ei, this) : (this.isStopped = true, this._complete());
  }
  unsubscribe() {
    this.closed || (this.isStopped = true, super.unsubscribe(), this.destination = null);
  }
  _next(t) {
    this.destination.next(t);
  }
  _error(t) {
    try {
      this.destination.error(t);
    } finally {
      this.unsubscribe();
    }
  }
  _complete() {
    try {
      this.destination.complete();
    } finally {
      this.unsubscribe();
    }
  }
};
var Cc = Function.prototype.bind;
function or(e6, t) {
  return Cc.call(e6, t);
}
var sr = class {
  constructor(t) {
    this.partialObserver = t;
  }
  next(t) {
    let { partialObserver: n } = this;
    if (n.next)
      try {
        n.next(t);
      } catch (r) {
        $t(r);
      }
  }
  error(t) {
    let { partialObserver: n } = this;
    if (n.error)
      try {
        n.error(t);
      } catch (r) {
        $t(r);
      }
    else
      $t(t);
  }
  complete() {
    let { partialObserver: t } = this;
    if (t.complete)
      try {
        t.complete();
      } catch (n) {
        $t(n);
      }
  }
};
var be = class extends fe {
  constructor(t, n, r) {
    super();
    let o;
    if (N(t) || !t)
      o = { next: t ?? void 0, error: n ?? void 0, complete: r ?? void 0 };
    else {
      let i;
      this && V.useDeprecatedNextContext ? (i = Object.create(t), i.unsubscribe = () => this.unsubscribe(), o = { next: t.next && or(t.next, i), error: t.error && or(t.error, i), complete: t.complete && or(t.complete, i) }) : o = t;
    }
    this.destination = new sr(o);
  }
};
function $t(e6) {
  V.useDeprecatedSynchronousErrorHandling ? wi(e6) : vi(e6);
}
function wc(e6) {
  throw e6;
}
function ir(e6, t) {
  let { onStoppedNotification: n } = V;
  n && _e.setTimeout(() => n(e6, t));
}
var Tc = { closed: true, next: nr, error: wc, complete: nr };
var Ti = typeof Symbol == "function" && Symbol.observable || "@@observable";
function Mi(e6) {
  return e6;
}
function _i(e6) {
  return e6.length === 0 ? Mi : e6.length === 1 ? e6[0] : function(n) {
    return e6.reduce((r, o) => o(r), n);
  };
}
var Ne = (() => {
  class e6 {
    constructor(n) {
      n && (this._subscribe = n);
    }
    lift(n) {
      let r = new e6();
      return r.source = this, r.operator = n, r;
    }
    subscribe(n, r, o) {
      let i = _c(n) ? n : new be(n, r, o);
      return Se(() => {
        let { operator: s, source: a } = this;
        i.add(s ? s.call(i, a) : a ? this._subscribe(i) : this._trySubscribe(i));
      }), i;
    }
    _trySubscribe(n) {
      try {
        return this._subscribe(n);
      } catch (r) {
        n.error(r);
      }
    }
    forEach(n, r) {
      return r = Si(r), new r((o, i) => {
        let s = new be({ next: (a) => {
          try {
            n(a);
          } catch (c) {
            i(c), s.unsubscribe();
          }
        }, error: i, complete: o });
        this.subscribe(s);
      });
    }
    _subscribe(n) {
      var r;
      return (r = this.source) === null || r === void 0 ? void 0 : r.subscribe(n);
    }
    [Ti]() {
      return this;
    }
    pipe(...n) {
      return _i(n)(this);
    }
    toPromise(n) {
      return n = Si(n), new n((r, o) => {
        let i;
        this.subscribe((s) => i = s, (s) => o(s), () => r(i));
      });
    }
  }
  return e6.create = (t) => new e6(t), e6;
})();
function Si(e6) {
  var t;
  return (t = e6 ?? V.Promise) !== null && t !== void 0 ? t : Promise;
}
function Mc(e6) {
  return e6 && N(e6.next) && N(e6.error) && N(e6.complete);
}
function _c(e6) {
  return e6 && e6 instanceof fe || Mc(e6) && Ht(e6);
}
function Sc(e6) {
  return N(e6?.lift);
}
function bi(e6) {
  return (t) => {
    if (Sc(t))
      return t.lift(function(n) {
        try {
          return e6(n, this);
        } catch (r) {
          this.error(r);
        }
      });
    throw new TypeError("Unable to lift unknown Observable type");
  };
}
function Ni(e6, t, n, r, o) {
  return new ar(e6, t, n, r, o);
}
var ar = class extends fe {
  constructor(t, n, r, o, i, s) {
    super(t), this.onFinalize = i, this.shouldUnsubscribe = s, this._next = n ? function(a) {
      try {
        n(a);
      } catch (c) {
        t.error(c);
      }
    } : super._next, this._error = o ? function(a) {
      try {
        o(a);
      } catch (c) {
        t.error(c);
      } finally {
        this.unsubscribe();
      }
    } : super._error, this._complete = r ? function() {
      try {
        r();
      } catch (a) {
        t.error(a);
      } finally {
        this.unsubscribe();
      }
    } : super._complete;
  }
  unsubscribe() {
    var t;
    if (!this.shouldUnsubscribe || this.shouldUnsubscribe()) {
      let { closed: n } = this;
      super.unsubscribe(), !n && ((t = this.onFinalize) === null || t === void 0 || t.call(this));
    }
  }
};
var Ai = Bt((e6) => function() {
  e6(this), this.name = "ObjectUnsubscribedError", this.message = "object unsubscribed";
});
var oe = (() => {
  class e6 extends Ne {
    constructor() {
      super(), this.closed = false, this.currentObservers = null, this.observers = [], this.isStopped = false, this.hasError = false, this.thrownError = null;
    }
    lift(n) {
      let r = new Ut(this, this);
      return r.operator = n, r;
    }
    _throwIfClosed() {
      if (this.closed)
        throw new Ai();
    }
    next(n) {
      Se(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.currentObservers || (this.currentObservers = Array.from(this.observers));
          for (let r of this.currentObservers)
            r.next(n);
        }
      });
    }
    error(n) {
      Se(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.hasError = this.isStopped = true, this.thrownError = n;
          let { observers: r } = this;
          for (; r.length; )
            r.shift().error(n);
        }
      });
    }
    complete() {
      Se(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.isStopped = true;
          let { observers: n } = this;
          for (; n.length; )
            n.shift().complete();
        }
      });
    }
    unsubscribe() {
      this.isStopped = this.closed = true, this.observers = this.currentObservers = null;
    }
    get observed() {
      var n;
      return ((n = this.observers) === null || n === void 0 ? void 0 : n.length) > 0;
    }
    _trySubscribe(n) {
      return this._throwIfClosed(), super._trySubscribe(n);
    }
    _subscribe(n) {
      return this._throwIfClosed(), this._checkFinalizedStatuses(n), this._innerSubscribe(n);
    }
    _innerSubscribe(n) {
      let { hasError: r, isStopped: o, observers: i } = this;
      return r || o ? tr : (this.currentObservers = null, i.push(n), new b(() => {
        this.currentObservers = null, Ke(i, n);
      }));
    }
    _checkFinalizedStatuses(n) {
      let { hasError: r, thrownError: o, isStopped: i } = this;
      r ? n.error(o) : i && n.complete();
    }
    asObservable() {
      let n = new Ne();
      return n.source = this, n;
    }
  }
  return e6.create = (t, n) => new Ut(t, n), e6;
})();
var Ut = class extends oe {
  constructor(t, n) {
    super(), this.destination = t, this.source = n;
  }
  next(t) {
    var n, r;
    (r = (n = this.destination) === null || n === void 0 ? void 0 : n.next) === null || r === void 0 || r.call(n, t);
  }
  error(t) {
    var n, r;
    (r = (n = this.destination) === null || n === void 0 ? void 0 : n.error) === null || r === void 0 || r.call(n, t);
  }
  complete() {
    var t, n;
    (n = (t = this.destination) === null || t === void 0 ? void 0 : t.complete) === null || n === void 0 || n.call(t);
  }
  _subscribe(t) {
    var n, r;
    return (r = (n = this.source) === null || n === void 0 ? void 0 : n.subscribe(t)) !== null && r !== void 0 ? r : tr;
  }
};
var Je = class extends oe {
  constructor(t) {
    super(), this._value = t;
  }
  get value() {
    return this.getValue();
  }
  _subscribe(t) {
    let n = super._subscribe(t);
    return !n.closed && t.next(this._value), n;
  }
  getValue() {
    let { hasError: t, thrownError: n, _value: r } = this;
    if (t)
      throw n;
    return this._throwIfClosed(), r;
  }
  next(t) {
    super.next(this._value = t);
  }
};
function cr(e6, t) {
  return bi((n, r) => {
    let o = 0;
    n.subscribe(Ni(r, (i) => {
      r.next(e6.call(t, i, o++));
    }));
  });
}
var ur;
function zt() {
  return ur;
}
function W(e6) {
  let t = ur;
  return ur = e6, t;
}
var xi = Symbol("NotFound");
function Ae(e6) {
  return e6 === xi || e6?.name === "\u0275NotFound";
}
var g = class extends Error {
  code;
  constructor(t, n) {
    super(Mr(t, n)), this.code = t;
  }
};
function xc(e6) {
  return `NG0${Math.abs(e6)}`;
}
function Mr(e6, t) {
  return `${xc(e6)}${t ? ": " + t : ""}`;
}
function C(e6) {
  for (let t in e6)
    if (e6[t] === C)
      return t;
  throw Error("");
}
function _r(e6, t) {
  return e6 ? t ? `${e6} ${t}` : e6 : t || "";
}
var Rc = C({ __forward_ref__: C });
function Qt(e6) {
  return e6.__forward_ref__ = Qt, e6;
}
function R(e6) {
  return Li(e6) ? e6() : e6;
}
function Li(e6) {
  return typeof e6 == "function" && e6.hasOwnProperty(Rc) && e6.__forward_ref__ === Qt;
}
function _(e6) {
  return { token: e6.token, providedIn: e6.providedIn || null, factory: e6.factory, value: void 0 };
}
function rt(e6) {
  return { providers: e6.providers || [], imports: e6.imports || [] };
}
function Kt(e6) {
  return Oc(e6, Jt);
}
function Oc(e6, t) {
  return e6.hasOwnProperty(t) && e6[t] || null;
}
function kc(e6) {
  let t = e6?.[Jt] ?? null;
  return t || null;
}
function dr(e6) {
  return e6 && e6.hasOwnProperty(Wt) ? e6[Wt] : null;
}
var Jt = C({ \u0275prov: C });
var Wt = C({ \u0275inj: C });
var D = class {
  _desc;
  ngMetadataName = "InjectionToken";
  \u0275prov;
  constructor(t, n) {
    this._desc = t, this.\u0275prov = void 0, typeof n == "number" ? this.__NG_ELEMENT_ID__ = n : n !== void 0 && (this.\u0275prov = _({ token: this, providedIn: n.providedIn || "root", factory: n.factory }));
  }
  get multi() {
    return this;
  }
  toString() {
    return `InjectionToken ${this._desc}`;
  }
};
function Sr(e6) {
  return e6 && !!e6.\u0275providers;
}
var br = C({ \u0275cmp: C });
var Nr = C({ \u0275dir: C });
var Ar = C({ \u0275pipe: C });
var fr = C({ \u0275fac: C });
var De = C({ __NG_ELEMENT_ID__: C });
var Ri = C({ __NG_ENV_ID__: C });
function ot(e6) {
  return Rr(e6, "@Component"), e6[br] || null;
}
function xr(e6) {
  return Rr(e6, "@Directive"), e6[Nr] || null;
}
function Pi(e6) {
  return Rr(e6, "@Pipe"), e6[Ar] || null;
}
function Rr(e6, t) {
  if (e6 == null)
    throw new g(-919, false);
}
function ji(e6) {
  return typeof e6 == "string" ? e6 : e6 == null ? "" : String(e6);
}
var Bi = C({ ngErrorCode: C });
var Fc = C({ ngErrorMessage: C });
var Lc = C({ ngTokenPath: C });
function Or(e6, t) {
  return Vi("", -200, t);
}
function Xt(e6, t) {
  throw new g(-201, false);
}
function Vi(e6, t, n) {
  let r = new g(t, e6);
  return r[Bi] = t, r[Fc] = e6, n && (r[Lc] = n), r;
}
function Pc(e6) {
  return e6[Bi];
}
var pr;
function Hi() {
  return pr;
}
function x(e6) {
  let t = pr;
  return pr = e6, t;
}
function kr(e6, t, n) {
  let r = Kt(e6);
  if (r && r.providedIn == "root")
    return r.value === void 0 ? r.value = r.factory() : r.value;
  if (n & 8)
    return null;
  if (t !== void 0)
    return t;
  Xt(e6, "");
}
var jc = {};
var pe = jc;
var Bc = "__NG_DI_FLAG__";
var hr = class {
  injector;
  constructor(t) {
    this.injector = t;
  }
  retrieve(t, n) {
    let r = he(n) || 0;
    try {
      return this.injector.get(t, r & 8 ? null : pe, r);
    } catch (o) {
      if (Ae(o))
        return o;
      throw o;
    }
  }
};
function Vc(e6, t = 0) {
  let n = zt();
  if (n === void 0)
    throw new g(-203, false);
  if (n === null)
    return kr(e6, void 0, t);
  {
    let r = Hc(t), o = n.retrieve(e6, r);
    if (Ae(o)) {
      if (r.optional)
        return null;
      throw o;
    }
    return o;
  }
}
function E(e6, t = 0) {
  return (Hi() || Vc)(R(e6), t);
}
function v(e6, t) {
  return E(e6, he(t));
}
function he(e6) {
  return typeof e6 > "u" || typeof e6 == "number" ? e6 : 0 | (e6.optional && 8) | (e6.host && 1) | (e6.self && 2) | (e6.skipSelf && 4);
}
function Hc(e6) {
  return { optional: !!(e6 & 8), host: !!(e6 & 1), self: !!(e6 & 2), skipSelf: !!(e6 & 4) };
}
function gr(e6) {
  let t = [];
  for (let n = 0; n < e6.length; n++) {
    let r = R(e6[n]);
    if (Array.isArray(r)) {
      if (r.length === 0)
        throw new g(900, false);
      let o, i = 0;
      for (let s = 0; s < r.length; s++) {
        let a = r[s], c = $c(a);
        typeof c == "number" ? c === -1 ? o = a.token : i |= c : o = a;
      }
      t.push(E(o, i));
    } else
      t.push(E(r));
  }
  return t;
}
function $c(e6) {
  return e6[Bc];
}
function Re(e6, t) {
  let n = e6.hasOwnProperty(fr);
  return n ? e6[fr] : null;
}
function en(e6, t) {
  e6.forEach((n) => Array.isArray(n) ? en(n, t) : t(n));
}
function Fr(e6, t) {
  return t >= e6.length - 1 ? e6.pop() : e6.splice(t, 1)[0];
}
var ve = {};
var H = [];
var ke = new D("");
var Lr = new D("", -1);
var Pr = new D("");
var et = class {
  get(t, n = pe) {
    if (n === pe) {
      let o = Vi("", -201);
      throw o.name = "\u0275NotFound", o;
    }
    return n;
  }
};
function tn(e6) {
  return { \u0275providers: e6 };
}
function $i(e6) {
  return tn([{ provide: ke, multi: true, useValue: e6 }]);
}
function Ui(...e6) {
  return { \u0275providers: jr(true, e6), \u0275fromNgModule: true };
}
function jr(e6, ...t) {
  let n = [], r = /* @__PURE__ */ new Set(), o, i = (s) => {
    n.push(s);
  };
  return en(t, (s) => {
    let a = s;
    qt(a, i, [], r) && (o ||= [], o.push(a));
  }), o !== void 0 && zi(o, i), n;
}
function zi(e6, t) {
  for (let n = 0; n < e6.length; n++) {
    let { ngModule: r, providers: o } = e6[n];
    Br(o, (i) => {
      t(i, r);
    });
  }
}
function qt(e6, t, n, r) {
  if (e6 = R(e6), !e6)
    return false;
  let o = null, i = dr(e6), s = !i && ot(e6);
  if (!i && !s) {
    let c = e6.ngModule;
    if (i = dr(c), i)
      o = c;
    else
      return false;
  } else {
    if (s && !s.standalone)
      return false;
    o = e6;
  }
  let a = r.has(o);
  if (s) {
    if (a)
      return false;
    if (r.add(o), s.dependencies) {
      let c = typeof s.dependencies == "function" ? s.dependencies() : s.dependencies;
      for (let u of c)
        qt(u, t, n, r);
    }
  } else if (i) {
    if (i.imports != null && !a) {
      r.add(o);
      let u;
      en(i.imports, (l) => {
        qt(l, t, n, r) && (u ||= [], u.push(l));
      }), u !== void 0 && zi(u, t);
    }
    if (!a) {
      let u = Re(o) || (() => new o());
      t({ provide: o, useFactory: u, deps: H }, o), t({ provide: Pr, useValue: o, multi: true }, o), t({ provide: ke, useValue: () => E(o), multi: true }, o);
    }
    let c = i.providers;
    if (c != null && !a) {
      let u = e6;
      Br(c, (l) => {
        t(l, u);
      });
    }
  } else
    return false;
  return o !== e6 && e6.providers !== void 0;
}
function Br(e6, t) {
  for (let n of e6)
    Sr(n) && (n = n.\u0275providers), Array.isArray(n) ? Br(n, t) : t(n);
}
var Uc = C({ provide: String, useValue: C });
function Gi(e6) {
  return e6 !== null && typeof e6 == "object" && Uc in e6;
}
function zc(e6) {
  return !!(e6 && e6.useExisting);
}
function Gc(e6) {
  return !!(e6 && e6.useFactory);
}
function Zt(e6) {
  return typeof e6 == "function";
}
var it = new D("");
var Gt = {};
var Oi = {};
var lr;
function st() {
  return lr === void 0 && (lr = new et()), lr;
}
var $ = class {
};
var ge = class extends $ {
  parent;
  source;
  scopes;
  records = /* @__PURE__ */ new Map();
  _ngOnDestroyHooks = /* @__PURE__ */ new Set();
  _onDestroyHooks = [];
  get destroyed() {
    return this._destroyed;
  }
  _destroyed = false;
  injectorDefTypes;
  constructor(t, n, r, o) {
    super(), this.parent = n, this.source = r, this.scopes = o, yr(t, (s) => this.processProvider(s)), this.records.set(Lr, xe(void 0, this)), o.has("environment") && this.records.set($, xe(void 0, this));
    let i = this.records.get(it);
    i != null && typeof i.value == "string" && this.scopes.add(i.value), this.injectorDefTypes = new Set(this.get(Pr, H, { self: true }));
  }
  retrieve(t, n) {
    let r = he(n) || 0;
    try {
      return this.get(t, pe, r);
    } catch (o) {
      if (Ae(o))
        return o;
      throw o;
    }
  }
  destroy() {
    Xe(this), this._destroyed = true;
    let t = y(null);
    try {
      for (let r of this._ngOnDestroyHooks)
        r.ngOnDestroy();
      let n = this._onDestroyHooks;
      this._onDestroyHooks = [];
      for (let r of n)
        r();
    } finally {
      this.records.clear(), this._ngOnDestroyHooks.clear(), this.injectorDefTypes.clear(), y(t);
    }
  }
  onDestroy(t) {
    return Xe(this), this._onDestroyHooks.push(t), () => this.removeOnDestroy(t);
  }
  runInContext(t) {
    Xe(this);
    let n = W(this), r = x(void 0), o;
    try {
      return t();
    } finally {
      W(n), x(r);
    }
  }
  get(t, n = pe, r) {
    if (Xe(this), t.hasOwnProperty(Ri))
      return t[Ri](this);
    let o = he(r), i, s = W(this), a = x(void 0);
    try {
      if (!(o & 4)) {
        let u = this.records.get(t);
        if (u === void 0) {
          let l = Qc(t) && Kt(t);
          l && this.injectableDefInScope(l) ? u = xe(mr(t), Gt) : u = null, this.records.set(t, u);
        }
        if (u != null)
          return this.hydrate(t, u, o);
      }
      let c = o & 2 ? st() : this.parent;
      return n = o & 8 && n === pe ? null : n, c.get(t, n);
    } catch (c) {
      let u = Pc(c);
      throw u === -200 || u === -201 ? new g(u, null) : c;
    } finally {
      x(a), W(s);
    }
  }
  resolveInjectorInitializers() {
    let t = y(null), n = W(this), r = x(void 0), o;
    try {
      let i = this.get(ke, H, { self: true });
      for (let s of i)
        s();
    } finally {
      W(n), x(r), y(t);
    }
  }
  toString() {
    return "R3Injector[...]";
  }
  processProvider(t) {
    t = R(t);
    let n = Zt(t) ? t : R(t && t.provide), r = qc(t);
    if (!Zt(t) && t.multi === true) {
      let o = this.records.get(n);
      o || (o = xe(void 0, Gt, true), o.factory = () => gr(o.multi), this.records.set(n, o)), n = t, o.multi.push(t);
    }
    this.records.set(n, r);
  }
  hydrate(t, n, r) {
    let o = y(null);
    try {
      if (n.value === Oi)
        throw Or("");
      return n.value === Gt && (n.value = Oi, n.value = n.factory(void 0, r)), typeof n.value == "object" && n.value && Yc(n.value) && this._ngOnDestroyHooks.add(n.value), n.value;
    } finally {
      y(o);
    }
  }
  injectableDefInScope(t) {
    if (!t.providedIn)
      return false;
    let n = R(t.providedIn);
    return typeof n == "string" ? n === "any" || this.scopes.has(n) : this.injectorDefTypes.has(n);
  }
  removeOnDestroy(t) {
    let n = this._onDestroyHooks.indexOf(t);
    n !== -1 && this._onDestroyHooks.splice(n, 1);
  }
};
function mr(e6) {
  let t = Kt(e6), n = t !== null ? t.factory : Re(e6);
  if (n !== null)
    return n;
  if (e6 instanceof D)
    throw new g(-204, false);
  if (e6 instanceof Function)
    return Wc(e6);
  throw new g(-204, false);
}
function Wc(e6) {
  if (e6.length > 0)
    throw new g(-204, false);
  let n = kc(e6);
  return n !== null ? () => n.factory(e6) : () => new e6();
}
function qc(e6) {
  if (Gi(e6))
    return xe(void 0, e6.useValue);
  {
    let t = Wi(e6);
    return xe(t, Gt);
  }
}
function Wi(e6, t, n) {
  let r;
  if (Zt(e6)) {
    let o = R(e6);
    return Re(o) || mr(o);
  } else if (Gi(e6))
    r = () => R(e6.useValue);
  else if (Gc(e6))
    r = () => e6.useFactory(...gr(e6.deps || []));
  else if (zc(e6))
    r = (o, i) => E(R(e6.useExisting), i !== void 0 && i & 8 ? 8 : void 0);
  else {
    let o = R(e6 && (e6.useClass || e6.provide));
    if (Zc(e6))
      r = () => new o(...gr(e6.deps));
    else
      return Re(o) || mr(o);
  }
  return r;
}
function Xe(e6) {
  if (e6.destroyed)
    throw new g(-205, false);
}
function xe(e6, t, n = false) {
  return { factory: e6, value: t, multi: n ? [] : void 0 };
}
function Zc(e6) {
  return !!e6.deps;
}
function Yc(e6) {
  return e6 !== null && typeof e6 == "object" && typeof e6.ngOnDestroy == "function";
}
function Qc(e6) {
  return typeof e6 == "function" || typeof e6 == "object" && e6.ngMetadataName === "InjectionToken";
}
function yr(e6, t) {
  for (let n of e6)
    Array.isArray(n) ? yr(n, t) : n && Sr(n) ? yr(n.\u0275providers, t) : t(n);
}
function nn(e6, t) {
  let n;
  e6 instanceof ge ? (Xe(e6), n = e6) : n = new hr(e6);
  let r, o = W(n), i = x(void 0);
  try {
    return t();
  } finally {
    W(o), x(i);
  }
}
function qi() {
  return Hi() !== void 0 || zt() != null;
}
var q = 0;
var m = 1;
var h = 2;
var O = 3;
var ee = 4;
var te = 5;
var rn = 6;
var on = 7;
var k = 8;
var Ee = 9;
var ne = 10;
var P = 11;
var Fe = 12;
var Vr = 13;
var Le = 14;
var Z = 15;
var at = 16;
var Ie = 17;
var sn = 18;
var ie = 19;
var Hr = 20;
var J = 21;
var an = 22;
var ct = 23;
var F = 24;
var cn = 25;
var Pe = 26;
var U = 27;
var Zi = 1;
var un = 7;
var Yi = 8;
var ut = 9;
var re = 10;
function se(e6) {
  return Array.isArray(e6) && typeof e6[Zi] == "object";
}
function ae(e6) {
  return Array.isArray(e6) && e6[Zi] === true;
}
function $r(e6) {
  return (e6.flags & 4) !== 0;
}
function lt(e6) {
  return e6.componentOffset > -1;
}
function Qi(e6) {
  return (e6.flags & 1) === 1;
}
function je(e6) {
  return !!e6.template;
}
function Be(e6) {
  return (e6[h] & 512) !== 0;
}
function Ce(e6) {
  return (e6[h] & 256) === 256;
}
var Ki = "svg";
var Ji = "math";
function ce(e6) {
  for (; Array.isArray(e6); )
    e6 = e6[q];
  return e6;
}
function Xi(e6, t) {
  return ce(t[e6]);
}
function Ve(e6, t) {
  return ce(t[e6.index]);
}
function es(e6, t) {
  return e6.data[t];
}
function ue(e6, t) {
  let n = t[e6];
  return se(n) ? n : n[q];
}
function ln(e6) {
  return (e6[h] & 128) === 128;
}
function dt(e6, t) {
  return t == null ? null : e6[t];
}
function Ur(e6) {
  e6[Ie] = 0;
}
function zr(e6) {
  e6[h] & 1024 || (e6[h] |= 1024, ln(e6) && pt(e6));
}
function ft(e6) {
  return !!(e6[h] & 9216 || e6[F]?.dirty);
}
function Gr(e6) {
  e6[ne].changeDetectionScheduler?.notify(8), e6[h] & 64 && (e6[h] |= 1024), ft(e6) && pt(e6);
}
function pt(e6) {
  e6[ne].changeDetectionScheduler?.notify(0);
  let t = me(e6);
  for (; t !== null && !(t[h] & 8192 || (t[h] |= 8192, !ln(t))); )
    t = me(t);
}
function Wr(e6, t) {
  if (Ce(e6))
    throw new g(911, false);
  e6[J] === null && (e6[J] = []), e6[J].push(t);
}
function ts(e6, t) {
  if (e6[J] === null)
    return;
  let n = e6[J].indexOf(t);
  n !== -1 && e6[J].splice(n, 1);
}
function me(e6) {
  let t = e6[O];
  return ae(t) ? t[O] : t;
}
var w = { lFrame: ms(null), bindingsEnabled: true, skipHydrationRootTNode: null };
var Dr = false;
function ns() {
  return w.lFrame.elementDepthCount;
}
function rs() {
  w.lFrame.elementDepthCount++;
}
function os() {
  w.lFrame.elementDepthCount--;
}
function is() {
  return w.skipHydrationRootTNode !== null;
}
function ss(e6) {
  return w.skipHydrationRootTNode === e6;
}
function as() {
  w.skipHydrationRootTNode = null;
}
function Y() {
  return w.lFrame.lView;
}
function qr() {
  return w.lFrame.tView;
}
function He() {
  let e6 = Zr();
  for (; e6 !== null && e6.type === 64; )
    e6 = e6.parent;
  return e6;
}
function Zr() {
  return w.lFrame.currentTNode;
}
function cs() {
  let e6 = w.lFrame, t = e6.currentTNode;
  return e6.isParent ? t : t.parent;
}
function ht(e6, t) {
  let n = w.lFrame;
  n.currentTNode = e6, n.isParent = t;
}
function Yr() {
  return w.lFrame.isParent;
}
function us() {
  w.lFrame.isParent = false;
}
function Qr() {
  return Dr;
}
function Kr(e6) {
  let t = Dr;
  return Dr = e6, t;
}
function ls(e6) {
  return w.lFrame.bindingIndex = e6;
}
function ds() {
  return w.lFrame.bindingIndex++;
}
function fs() {
  return w.lFrame.inI18n;
}
function ps(e6, t) {
  let n = w.lFrame;
  n.bindingIndex = n.bindingRootIndex = e6, dn(t);
}
function hs() {
  return w.lFrame.currentDirectiveIndex;
}
function dn(e6) {
  w.lFrame.currentDirectiveIndex = e6;
}
function Jr(e6) {
  w.lFrame.currentQueryIndex = e6;
}
function Kc(e6) {
  let t = e6[m];
  return t.type === 2 ? t.declTNode : t.type === 1 ? e6[te] : null;
}
function Xr(e6, t, n) {
  if (n & 4) {
    let o = t, i = e6;
    for (; o = o.parent, o === null && !(n & 1); )
      if (o = Kc(i), o === null || (i = i[Le], o.type & 10))
        break;
    if (o === null)
      return false;
    t = o, e6 = i;
  }
  let r = w.lFrame = gs();
  return r.currentTNode = t, r.lView = e6, true;
}
function fn(e6) {
  let t = gs(), n = e6[m];
  w.lFrame = t, t.currentTNode = n.firstChild, t.lView = e6, t.tView = n, t.contextLView = e6, t.bindingIndex = n.bindingStartIndex, t.inI18n = false;
}
function gs() {
  let e6 = w.lFrame, t = e6 === null ? null : e6.child;
  return t === null ? ms(e6) : t;
}
function ms(e6) {
  let t = { currentTNode: null, isParent: true, lView: null, tView: null, selectedIndex: -1, contextLView: null, elementDepthCount: 0, currentNamespace: null, currentDirectiveIndex: -1, bindingRootIndex: -1, bindingIndex: -1, currentQueryIndex: 0, parent: e6, child: null, inI18n: false };
  return e6 !== null && (e6.child = t), t;
}
function ys() {
  let e6 = w.lFrame;
  return w.lFrame = e6.parent, e6.currentTNode = null, e6.lView = null, e6;
}
var eo = ys;
function pn() {
  let e6 = ys();
  e6.isParent = true, e6.tView = null, e6.selectedIndex = -1, e6.contextLView = null, e6.elementDepthCount = 0, e6.currentDirectiveIndex = -1, e6.currentNamespace = null, e6.bindingRootIndex = -1, e6.bindingIndex = -1, e6.currentQueryIndex = 0;
}
function hn() {
  return w.lFrame.selectedIndex;
}
function le(e6) {
  w.lFrame.selectedIndex = e6;
}
function Ds() {
  return w.lFrame.currentNamespace;
}
var vs = true;
function to() {
  return vs;
}
function no(e6) {
  vs = e6;
}
function vr(e6, t = null, n = null, r) {
  let o = Es(e6, t, n, r);
  return o.resolveInjectorInitializers(), o;
}
function Es(e6, t = null, n = null, r, o = /* @__PURE__ */ new Set()) {
  let i = [n || H, Ui(e6)], s;
  return new ge(i, t || st(), s || null, o);
}
var ye = class e2 {
  static THROW_IF_NOT_FOUND = pe;
  static NULL = new et();
  static create(t, n) {
    if (Array.isArray(t))
      return vr({ name: "" }, n, t, "");
    {
      let r = t.name ?? "";
      return vr({ name: r }, t.parent, t.providers, r);
    }
  }
  static \u0275prov = _({ token: e2, providedIn: "any", factory: () => E(Lr) });
  static __NG_ELEMENT_ID__ = -1;
};
var j = new D("");
var gt = /* @__PURE__ */ (() => {
  class e6 {
    static __NG_ELEMENT_ID__ = Jc;
    static __NG_ENV_ID__ = (n) => n;
  }
  return e6;
})();
var Er = class extends gt {
  _lView;
  constructor(t) {
    super(), this._lView = t;
  }
  get destroyed() {
    return Ce(this._lView);
  }
  onDestroy(t) {
    let n = this._lView;
    return Wr(n, t), () => ts(n, t);
  }
};
function Jc() {
  return new Er(Y());
}
var Is = false;
var Cs = new D("");
var $e = (() => {
  class e6 {
    taskId = 0;
    pendingTasks = /* @__PURE__ */ new Set();
    destroyed = false;
    pendingTask = new Je(false);
    debugTaskTracker = v(Cs, { optional: true });
    get hasPendingTasks() {
      return this.destroyed ? false : this.pendingTask.value;
    }
    get hasPendingTasksObservable() {
      return this.destroyed ? new Ne((n) => {
        n.next(false), n.complete();
      }) : this.pendingTask;
    }
    add() {
      !this.hasPendingTasks && !this.destroyed && this.pendingTask.next(true);
      let n = this.taskId++;
      return this.pendingTasks.add(n), this.debugTaskTracker?.add(n), n;
    }
    has(n) {
      return this.pendingTasks.has(n);
    }
    remove(n) {
      this.pendingTasks.delete(n), this.debugTaskTracker?.remove(n), this.pendingTasks.size === 0 && this.hasPendingTasks && this.pendingTask.next(false);
    }
    ngOnDestroy() {
      this.pendingTasks.clear(), this.hasPendingTasks && this.pendingTask.next(false), this.destroyed = true, this.pendingTask.unsubscribe();
    }
    static \u0275prov = _({ token: e6, providedIn: "root", factory: () => new e6() });
  }
  return e6;
})();
var Ir = class extends oe {
  __isAsync;
  destroyRef = void 0;
  pendingTasks = void 0;
  constructor(t = false) {
    super(), this.__isAsync = t, qi() && (this.destroyRef = v(gt, { optional: true }) ?? void 0, this.pendingTasks = v($e, { optional: true }) ?? void 0);
  }
  emit(t) {
    let n = y(null);
    try {
      super.next(t);
    } finally {
      y(n);
    }
  }
  subscribe(t, n, r) {
    let o = t, i = n || (() => null), s = r;
    if (t && typeof t == "object") {
      let c = t;
      o = c.next?.bind(c), i = c.error?.bind(c), s = c.complete?.bind(c);
    }
    this.__isAsync && (i = this.wrapInTimeout(i), o && (o = this.wrapInTimeout(o)), s && (s = this.wrapInTimeout(s)));
    let a = super.subscribe({ next: o, error: i, complete: s });
    return t instanceof b && t.add(a), a;
  }
  wrapInTimeout(t) {
    return (n) => {
      let r = this.pendingTasks?.add();
      setTimeout(() => {
        try {
          t(n);
        } finally {
          r !== void 0 && this.pendingTasks?.remove(r);
        }
      });
    };
  }
};
var K = Ir;
function Yt(...e6) {
}
function ro(e6) {
  let t, n;
  function r() {
    e6 = Yt;
    try {
      n !== void 0 && typeof cancelAnimationFrame == "function" && cancelAnimationFrame(n), t !== void 0 && clearTimeout(t);
    } catch {
    }
  }
  return t = setTimeout(() => {
    e6(), r();
  }), typeof requestAnimationFrame == "function" && (n = requestAnimationFrame(() => {
    e6(), r();
  })), () => r();
}
function ws(e6) {
  return queueMicrotask(() => e6()), () => {
    e6 = Yt;
  };
}
var oo = "isAngularZone";
var tt = oo + "_ID";
var Xc = 0;
var L = class e3 {
  hasPendingMacrotasks = false;
  hasPendingMicrotasks = false;
  isStable = true;
  onUnstable = new K(false);
  onMicrotaskEmpty = new K(false);
  onStable = new K(false);
  onError = new K(false);
  constructor(t) {
    let { enableLongStackTrace: n = false, shouldCoalesceEventChangeDetection: r = false, shouldCoalesceRunChangeDetection: o = false, scheduleInRootZone: i = Is } = t;
    if (typeof Zone > "u")
      throw new g(908, false);
    Zone.assertZonePatched();
    let s = this;
    s._nesting = 0, s._outer = s._inner = Zone.current, Zone.TaskTrackingZoneSpec && (s._inner = s._inner.fork(new Zone.TaskTrackingZoneSpec())), n && Zone.longStackTraceZoneSpec && (s._inner = s._inner.fork(Zone.longStackTraceZoneSpec)), s.shouldCoalesceEventChangeDetection = !o && r, s.shouldCoalesceRunChangeDetection = o, s.callbackScheduled = false, s.scheduleInRootZone = i, nu(s);
  }
  static isInAngularZone() {
    return typeof Zone < "u" && Zone.current.get(oo) === true;
  }
  static assertInAngularZone() {
    if (!e3.isInAngularZone())
      throw new g(909, false);
  }
  static assertNotInAngularZone() {
    if (e3.isInAngularZone())
      throw new g(909, false);
  }
  run(t, n, r) {
    return this._inner.run(t, n, r);
  }
  runTask(t, n, r, o) {
    let i = this._inner, s = i.scheduleEventTask("NgZoneEvent: " + o, t, eu, Yt, Yt);
    try {
      return i.runTask(s, n, r);
    } finally {
      i.cancelTask(s);
    }
  }
  runGuarded(t, n, r) {
    return this._inner.runGuarded(t, n, r);
  }
  runOutsideAngular(t) {
    return this._outer.run(t);
  }
};
var eu = {};
function io(e6) {
  if (e6._nesting == 0 && !e6.hasPendingMicrotasks && !e6.isStable)
    try {
      e6._nesting++, e6.onMicrotaskEmpty.emit(null);
    } finally {
      if (e6._nesting--, !e6.hasPendingMicrotasks)
        try {
          e6.runOutsideAngular(() => e6.onStable.emit(null));
        } finally {
          e6.isStable = true;
        }
    }
}
function tu(e6) {
  if (e6.isCheckStableRunning || e6.callbackScheduled)
    return;
  e6.callbackScheduled = true;
  function t() {
    ro(() => {
      e6.callbackScheduled = false, Cr(e6), e6.isCheckStableRunning = true, io(e6), e6.isCheckStableRunning = false;
    });
  }
  e6.scheduleInRootZone ? Zone.root.run(() => {
    t();
  }) : e6._outer.run(() => {
    t();
  }), Cr(e6);
}
function nu(e6) {
  let t = () => {
    tu(e6);
  }, n = Xc++;
  e6._inner = e6._inner.fork({ name: "angular", properties: { [oo]: true, [tt]: n, [tt + n]: true }, onInvokeTask: (r, o, i, s, a, c) => {
    if (ru(c))
      return r.invokeTask(i, s, a, c);
    try {
      return ki(e6), r.invokeTask(i, s, a, c);
    } finally {
      (e6.shouldCoalesceEventChangeDetection && s.type === "eventTask" || e6.shouldCoalesceRunChangeDetection) && t(), Fi(e6);
    }
  }, onInvoke: (r, o, i, s, a, c, u) => {
    try {
      return ki(e6), r.invoke(i, s, a, c, u);
    } finally {
      e6.shouldCoalesceRunChangeDetection && !e6.callbackScheduled && !ou(c) && t(), Fi(e6);
    }
  }, onHasTask: (r, o, i, s) => {
    r.hasTask(i, s), o === i && (s.change == "microTask" ? (e6._hasPendingMicrotasks = s.microTask, Cr(e6), io(e6)) : s.change == "macroTask" && (e6.hasPendingMacrotasks = s.macroTask));
  }, onHandleError: (r, o, i, s) => (r.handleError(i, s), e6.runOutsideAngular(() => e6.onError.emit(s)), false) });
}
function Cr(e6) {
  e6._hasPendingMicrotasks || (e6.shouldCoalesceEventChangeDetection || e6.shouldCoalesceRunChangeDetection) && e6.callbackScheduled === true ? e6.hasPendingMicrotasks = true : e6.hasPendingMicrotasks = false;
}
function ki(e6) {
  e6._nesting++, e6.isStable && (e6.isStable = false, e6.onUnstable.emit(null));
}
function Fi(e6) {
  e6._nesting--, io(e6);
}
var nt = class {
  hasPendingMicrotasks = false;
  hasPendingMacrotasks = false;
  isStable = true;
  onUnstable = new K();
  onMicrotaskEmpty = new K();
  onStable = new K();
  onError = new K();
  run(t, n, r) {
    return t.apply(n, r);
  }
  runGuarded(t, n, r) {
    return t.apply(n, r);
  }
  runOutsideAngular(t) {
    return t();
  }
  runTask(t, n, r, o) {
    return t.apply(n, r);
  }
};
function ru(e6) {
  return Ts(e6, "__ignore_ng_zone__");
}
function ou(e6) {
  return Ts(e6, "__scheduler_tick__");
}
function Ts(e6, t) {
  return !Array.isArray(e6) || e6.length !== 1 ? false : e6[0]?.data?.[t] === true;
}
var X = class {
  _console = console;
  handleError(t) {
    this._console.error("ERROR", t);
  }
};
var Ue = new D("", { factory: () => {
  let e6 = v(L), t = v($), n;
  return (r) => {
    e6.runOutsideAngular(() => {
      t.destroyed && !n ? setTimeout(() => {
        throw r;
      }) : (n ??= t.get(X), n.handleError(r));
    });
  };
} });
var Ms = { provide: ke, useValue: () => {
  let e6 = v(X, { optional: true });
}, multi: true };
var iu = new D("", { factory: () => {
  let e6 = v(j).defaultView;
  if (!e6)
    return;
  let t = v(Ue), n = (i) => {
    t(i.reason), i.preventDefault();
  }, r = (i) => {
    i.error ? t(i.error) : t(new Error(i.message, { cause: i })), i.preventDefault();
  }, o = () => {
    e6.addEventListener("unhandledrejection", n), e6.addEventListener("error", r);
  };
  typeof Zone < "u" ? Zone.root.run(o) : o(), v(gt).onDestroy(() => {
    e6.removeEventListener("error", r), e6.removeEventListener("unhandledrejection", n);
  });
} });
function so() {
  return tn([$i(() => {
    v(iu);
  })]);
}
function gn(e6, t) {
  let [n, r, o] = Xn(e6, t?.equal), i = n, s = i[G];
  return i.set = r, i.update = o, i.asReadonly = _s.bind(i), i;
}
function _s() {
  let e6 = this[G];
  if (e6.readonlyFn === void 0) {
    let t = () => this();
    t[G] = e6, e6.readonlyFn = t;
  }
  return e6.readonlyFn;
}
var Oe = class {
};
var mt = new D("", { factory: () => true });
var ao = new D("");
var co = (() => {
  class e6 {
    static \u0275prov = _({ token: e6, providedIn: "root", factory: () => new wr() });
  }
  return e6;
})();
var wr = class {
  dirtyEffectCount = 0;
  queues = /* @__PURE__ */ new Map();
  add(t) {
    this.enqueue(t), this.schedule(t);
  }
  schedule(t) {
    t.dirty && this.dirtyEffectCount++;
  }
  remove(t) {
    let n = t.zone, r = this.queues.get(n);
    r.has(t) && (r.delete(t), t.dirty && this.dirtyEffectCount--);
  }
  enqueue(t) {
    let n = t.zone;
    this.queues.has(n) || this.queues.set(n, /* @__PURE__ */ new Set());
    let r = this.queues.get(n);
    r.has(t) || r.add(t);
  }
  flush() {
    for (; this.dirtyEffectCount > 0; ) {
      let t = false;
      for (let [n, r] of this.queues)
        n === null ? t ||= this.flushQueue(r) : t ||= n.run(() => this.flushQueue(r));
      t || (this.dirtyEffectCount = 0);
    }
  }
  flushQueue(t) {
    let n = false;
    for (let r of t)
      r.dirty && (this.dirtyEffectCount--, n = true, r.run());
    return n;
  }
};
var Tr = class {
  [G];
  constructor(t) {
    this[G] = t;
  }
  destroy() {
    this[G].destroy();
  }
};
function bo(e6) {
  return { toString: e6 }.toString();
}
function Ws(e6, t, n, r) {
  t !== null ? t.applyValueToInputSignal(t, r) : e6[n] = r;
}
var vn = class {
  previousValue;
  currentValue;
  firstChange;
  constructor(t, n, r) {
    this.previousValue = t, this.currentValue = n, this.firstChange = r;
  }
  isFirstChange() {
    return this.firstChange;
  }
};
function wu(e6) {
  return e6.type.prototype.ngOnChanges && (e6.setInput = Mu), Tu;
}
function Tu() {
  let e6 = Zs(this), t = e6?.current;
  if (t) {
    let n = e6.previous;
    if (n === ve)
      e6.previous = t;
    else
      for (let r in t)
        n[r] = t[r];
    e6.current = null, this.ngOnChanges(t);
  }
}
function Mu(e6, t, n, r, o) {
  let i = this.declaredInputs[r], s = Zs(e6) || _u(e6, { previous: ve, current: null }), a = s.current || (s.current = {}), c = s.previous, u = c[i];
  a[i] = new vn(u && u.currentValue, n, c === ve), Ws(e6, t, o, n);
}
var qs = "__ngSimpleChanges__";
function Zs(e6) {
  return e6[qs] || null;
}
function _u(e6, t) {
  return e6[qs] = t;
}
var Ss = [];
var M = function(e6, t = null, n) {
  for (let r = 0; r < Ss.length; r++) {
    let o = Ss[r];
    o(e6, t, n);
  }
};
var I = function(e6) {
  return e6[e6.TemplateCreateStart = 0] = "TemplateCreateStart", e6[e6.TemplateCreateEnd = 1] = "TemplateCreateEnd", e6[e6.TemplateUpdateStart = 2] = "TemplateUpdateStart", e6[e6.TemplateUpdateEnd = 3] = "TemplateUpdateEnd", e6[e6.LifecycleHookStart = 4] = "LifecycleHookStart", e6[e6.LifecycleHookEnd = 5] = "LifecycleHookEnd", e6[e6.OutputStart = 6] = "OutputStart", e6[e6.OutputEnd = 7] = "OutputEnd", e6[e6.BootstrapApplicationStart = 8] = "BootstrapApplicationStart", e6[e6.BootstrapApplicationEnd = 9] = "BootstrapApplicationEnd", e6[e6.BootstrapComponentStart = 10] = "BootstrapComponentStart", e6[e6.BootstrapComponentEnd = 11] = "BootstrapComponentEnd", e6[e6.ChangeDetectionStart = 12] = "ChangeDetectionStart", e6[e6.ChangeDetectionEnd = 13] = "ChangeDetectionEnd", e6[e6.ChangeDetectionSyncStart = 14] = "ChangeDetectionSyncStart", e6[e6.ChangeDetectionSyncEnd = 15] = "ChangeDetectionSyncEnd", e6[e6.AfterRenderHooksStart = 16] = "AfterRenderHooksStart", e6[e6.AfterRenderHooksEnd = 17] = "AfterRenderHooksEnd", e6[e6.ComponentStart = 18] = "ComponentStart", e6[e6.ComponentEnd = 19] = "ComponentEnd", e6[e6.DeferBlockStateStart = 20] = "DeferBlockStateStart", e6[e6.DeferBlockStateEnd = 21] = "DeferBlockStateEnd", e6[e6.DynamicComponentStart = 22] = "DynamicComponentStart", e6[e6.DynamicComponentEnd = 23] = "DynamicComponentEnd", e6[e6.HostBindingsUpdateStart = 24] = "HostBindingsUpdateStart", e6[e6.HostBindingsUpdateEnd = 25] = "HostBindingsUpdateEnd", e6;
}(I || {});
function Su(e6, t, n) {
  let { ngOnChanges: r, ngOnInit: o, ngDoCheck: i } = t.type.prototype;
  if (r) {
    let s = wu(t);
    (n.preOrderHooks ??= []).push(e6, s), (n.preOrderCheckHooks ??= []).push(e6, s);
  }
  o && (n.preOrderHooks ??= []).push(0 - e6, o), i && ((n.preOrderHooks ??= []).push(e6, i), (n.preOrderCheckHooks ??= []).push(e6, i));
}
function bu(e6, t) {
  for (let n = t.directiveStart, r = t.directiveEnd; n < r; n++) {
    let i = e6.data[n].type.prototype, { ngAfterContentInit: s, ngAfterContentChecked: a, ngAfterViewInit: c, ngAfterViewChecked: u, ngOnDestroy: l } = i;
    s && (e6.contentHooks ??= []).push(-n, s), a && ((e6.contentHooks ??= []).push(n, a), (e6.contentCheckHooks ??= []).push(n, a)), c && (e6.viewHooks ??= []).push(-n, c), u && ((e6.viewHooks ??= []).push(n, u), (e6.viewCheckHooks ??= []).push(n, u)), l != null && (e6.destroyHooks ??= []).push(n, l);
  }
}
function mn(e6, t, n) {
  Ys(e6, t, 3, n);
}
function yn(e6, t, n, r) {
  (e6[h] & 3) === n && Ys(e6, t, n, r);
}
function uo(e6, t) {
  let n = e6[h];
  (n & 3) === t && (n &= 16383, n += 1, e6[h] = n);
}
function Ys(e6, t, n, r) {
  let o = r !== void 0 ? e6[Ie] & 65535 : 0, i = r ?? -1, s = t.length - 1, a = 0;
  for (let c = o; c < s; c++)
    if (typeof t[c + 1] == "number") {
      if (a = t[c], r != null && a >= r)
        break;
    } else
      t[c] < 0 && (e6[Ie] += 65536), (a < i || i == -1) && (Nu(e6, n, t, c), e6[Ie] = (e6[Ie] & 4294901760) + c + 2), c++;
}
function bs(e6, t) {
  M(I.LifecycleHookStart, e6, t);
  let n = y(null);
  try {
    t.call(e6);
  } finally {
    y(n), M(I.LifecycleHookEnd, e6, t);
  }
}
function Nu(e6, t, n, r) {
  let o = n[r] < 0, i = n[r + 1], s = o ? -n[r] : n[r], a = e6[s];
  o ? e6[h] >> 14 < e6[Ie] >> 16 && (e6[h] & 3) === t && (e6[h] += 16384, bs(a, i)) : bs(a, i);
}
var Ge = -1;
var vt = class {
  factory;
  name;
  injectImpl;
  resolving = false;
  canSeeViewProviders;
  multi;
  componentProviders;
  index;
  providerFactory;
  constructor(t, n, r, o) {
    this.factory = t, this.name = o, this.canSeeViewProviders = n, this.injectImpl = r;
  }
};
function Au(e6, t, n) {
  let r = 0;
  for (; r < n.length; ) {
    let o = n[r];
    if (typeof o == "number") {
      if (o !== 0)
        break;
      r++;
      let i = n[r++], s = n[r++], a = n[r++];
      e6.setAttribute(t, s, a, i);
    } else {
      let i = o, s = n[++r];
      xu(i) ? e6.setProperty(t, i, s) : e6.setAttribute(t, i, s), r++;
    }
  }
  return r;
}
function xu(e6) {
  return e6.charCodeAt(0) === 64;
}
function No(e6, t) {
  if (!(t === null || t.length === 0))
    if (e6 === null || e6.length === 0)
      e6 = t.slice();
    else {
      let n = -1;
      for (let r = 0; r < t.length; r++) {
        let o = t[r];
        typeof o == "number" ? n = o : n === 0 || (n === -1 || n === 2 ? Ns(e6, n, o, null, t[++r]) : Ns(e6, n, o, null, null));
      }
    }
  return e6;
}
function Ns(e6, t, n, r, o) {
  let i = 0, s = e6.length;
  if (t === -1)
    s = -1;
  else
    for (; i < e6.length; ) {
      let a = e6[i++];
      if (typeof a == "number") {
        if (a === t) {
          s = -1;
          break;
        } else if (a > t) {
          s = i - 1;
          break;
        }
      }
    }
  for (; i < e6.length; ) {
    let a = e6[i];
    if (typeof a == "number")
      break;
    if (a === n) {
      o !== null && (e6[i + 1] = o);
      return;
    }
    i++, o !== null && i++;
  }
  s !== -1 && (e6.splice(s, 0, t), i = s + 1), e6.splice(i++, 0, n), o !== null && e6.splice(i++, 0, o);
}
function Ru(e6) {
  return e6 !== Ge;
}
function po(e6) {
  return e6 & 32767;
}
function Ou(e6) {
  return e6 >> 16;
}
function ho(e6, t) {
  let n = Ou(e6), r = t;
  for (; n > 0; )
    r = r[Le], n--;
  return r;
}
var go = true;
function As(e6) {
  let t = go;
  return go = e6, t;
}
var ku = 256;
var Qs = ku - 1;
var Ks = 5;
var Fu = 0;
var Q = {};
function Lu(e6, t, n) {
  let r;
  typeof n == "string" ? r = n.charCodeAt(0) || 0 : n.hasOwnProperty(De) && (r = n[De]), r == null && (r = n[De] = Fu++);
  let o = r & Qs, i = 1 << o;
  t.data[e6 + (o >> Ks)] |= i;
}
function Js(e6, t) {
  let n = Xs(e6, t);
  if (n !== -1)
    return n;
  let r = t[m];
  r.firstCreatePass && (e6.injectorIndex = t.length, lo(r.data, e6), lo(t, null), lo(r.blueprint, null));
  let o = ea(e6, t), i = e6.injectorIndex;
  if (Ru(o)) {
    let s = po(o), a = ho(o, t), c = a[m].data;
    for (let u = 0; u < 8; u++)
      t[i + u] = a[s + u] | c[s + u];
  }
  return t[i + 8] = o, i;
}
function lo(e6, t) {
  e6.push(0, 0, 0, 0, 0, 0, 0, 0, t);
}
function Xs(e6, t) {
  return e6.injectorIndex === -1 || e6.parent && e6.parent.injectorIndex === e6.injectorIndex || t[e6.injectorIndex + 8] === null ? -1 : e6.injectorIndex;
}
function ea(e6, t) {
  if (e6.parent && e6.parent.injectorIndex !== -1)
    return e6.parent.injectorIndex;
  let n = 0, r = null, o = t;
  for (; o !== null; ) {
    if (r = ia(o), r === null)
      return Ge;
    if (n++, o = o[Le], r.injectorIndex !== -1)
      return r.injectorIndex | n << 16;
  }
  return Ge;
}
function Pu(e6, t, n) {
  Lu(e6, t, n);
}
function ta(e6, t, n) {
  if (n & 8 || e6 !== void 0)
    return e6;
  Xt(t, "NodeInjector");
}
function na(e6, t, n, r) {
  if (n & 8 && r === void 0 && (r = null), (n & 3) === 0) {
    let o = e6[Ee], i = x(void 0);
    try {
      return o ? o.get(t, r, n & 8) : kr(t, r, n & 8);
    } finally {
      x(i);
    }
  }
  return ta(r, t, n);
}
function ra(e6, t, n, r = 0, o) {
  if (e6 !== null) {
    if (t[h] & 2048 && !(r & 2)) {
      let s = $u(e6, t, n, r, Q);
      if (s !== Q)
        return s;
    }
    let i = oa(e6, t, n, r, Q);
    if (i !== Q)
      return i;
  }
  return na(t, n, r, o);
}
function oa(e6, t, n, r, o) {
  let i = Vu(n);
  if (typeof i == "function") {
    if (!Xr(t, e6, r))
      return r & 1 ? ta(o, n, r) : na(t, n, r, o);
    try {
      let s;
      if (s = i(r), s == null && !(r & 8))
        Xt(n);
      else
        return s;
    } finally {
      eo();
    }
  } else if (typeof i == "number") {
    let s = null, a = Xs(e6, t), c = Ge, u = r & 1 ? t[Z][te] : null;
    for ((a === -1 || r & 4) && (c = a === -1 ? ea(e6, t) : t[a + 8], c === Ge || !Rs(r, false) ? a = -1 : (s = t[m], a = po(c), t = ho(c, t))); a !== -1; ) {
      let l = t[m];
      if (xs(i, a, l.data)) {
        let d = ju(a, t, n, s, r, u);
        if (d !== Q)
          return d;
      }
      c = t[a + 8], c !== Ge && Rs(r, t[m].data[a + 8] === u) && xs(i, a, t) ? (s = l, a = po(c), t = ho(c, t)) : a = -1;
    }
  }
  return o;
}
function ju(e6, t, n, r, o, i) {
  let s = t[m], a = s.data[e6 + 8], c = r == null ? lt(a) && go : r != s && (a.type & 3) !== 0, u = o & 1 && i === a, l = Bu(a, s, n, c, u);
  return l !== null ? mo(t, s, l, a, o) : Q;
}
function Bu(e6, t, n, r, o) {
  let i = e6.providerIndexes, s = t.data, a = i & 1048575, c = e6.directiveStart, u = e6.directiveEnd, l = i >> 20, d = r ? a : a + l, p = o ? a + l : u;
  for (let f = d; f < p; f++) {
    let T = s[f];
    if (f < c && n === T || f >= c && T.type === n)
      return f;
  }
  if (o) {
    let f = s[c];
    if (f && je(f) && f.type === n)
      return c;
  }
  return null;
}
function mo(e6, t, n, r, o) {
  let i = e6[n], s = t.data;
  if (i instanceof vt) {
    let a = i;
    if (a.resolving)
      throw Or("");
    let c = As(a.canSeeViewProviders);
    a.resolving = true;
    let u = s[n].type || s[n], l, d = a.injectImpl ? x(a.injectImpl) : null, p = Xr(e6, r, 0);
    try {
      i = e6[n] = a.factory(void 0, o, s, e6, r), t.firstCreatePass && n >= r.directiveStart && Su(n, s[n], t);
    } finally {
      d !== null && x(d), As(c), a.resolving = false, eo();
    }
  }
  return i;
}
function Vu(e6) {
  if (typeof e6 == "string")
    return e6.charCodeAt(0) || 0;
  let t = e6.hasOwnProperty(De) ? e6[De] : void 0;
  return typeof t == "number" ? t >= 0 ? t & Qs : Hu : t;
}
function xs(e6, t, n) {
  let r = 1 << e6;
  return !!(n[t + (e6 >> Ks)] & r);
}
function Rs(e6, t) {
  return !(e6 & 2) && !(e6 & 1 && t);
}
var En = class {
  _tNode;
  _lView;
  constructor(t, n) {
    this._tNode = t, this._lView = n;
  }
  get(t, n, r) {
    return ra(this._tNode, this._lView, t, he(r), n);
  }
};
function Hu() {
  return new En(He(), Y());
}
function $u(e6, t, n, r, o) {
  let i = e6, s = t;
  for (; i !== null && s !== null && s[h] & 2048 && !Be(s); ) {
    let a = oa(i, s, n, r | 2, Q);
    if (a !== Q)
      return a;
    let c = i.parent;
    if (!c) {
      let u = s[Hr];
      if (u) {
        let l = u.get(n, Q, r & -5);
        if (l !== Q)
          return l;
      }
      c = ia(s), s = s[Le];
    }
    i = c;
  }
  return o;
}
function ia(e6) {
  let t = e6[m], n = t.type;
  return n === 2 ? t.declTNode : n === 1 ? e6[te] : null;
}
function Uu() {
  return sa(He(), Y());
}
function sa(e6, t) {
  return new Ao(Ve(e6, t));
}
var Ao = /* @__PURE__ */ (() => {
  class e6 {
    nativeElement;
    constructor(n) {
      this.nativeElement = n;
    }
    static __NG_ELEMENT_ID__ = Uu;
  }
  return e6;
})();
function zu(e6) {
  return (e6.flags & 128) === 128;
}
var xo = function(e6) {
  return e6[e6.OnPush = 0] = "OnPush", e6[e6.Eager = 1] = "Eager", e6[e6.Default = 1] = "Default", e6;
}(xo || {});
var aa = /* @__PURE__ */ new Map();
var Gu = 0;
function Wu() {
  return Gu++;
}
function qu(e6) {
  aa.set(e6[ie], e6);
}
function yo(e6) {
  aa.delete(e6[ie]);
}
var Os = "__ngContext__";
function Et(e6, t) {
  se(t) ? (e6[Os] = t[ie], qu(t)) : e6[Os] = t;
}
function ca(e6) {
  return la(e6[Fe]);
}
function ua(e6) {
  return la(e6[ee]);
}
function la(e6) {
  for (; e6 !== null && !ae(e6); )
    e6 = e6[ee];
  return e6;
}
var Zu;
function Ro(e6) {
  Zu = e6;
}
var _n = new D("", { factory: () => Yu });
var Yu = "ng";
var Sn = new D("");
var wt = new D("", { providedIn: "platform", factory: () => "unknown" });
var bn = new D("", { factory: () => v(j).body?.querySelector("[ngCspNonce]")?.getAttribute("ngCspNonce") || null });
var da = false;
var fa = new D("", { factory: () => da });
function Oo(e6) {
  return (e6.flags & 32) === 32;
}
var Qu = () => null;
function pa(e6, t, n = false) {
  return Qu(e6, t, n);
}
function ha(e6, t) {
  let n = e6.contentQueries;
  if (n !== null) {
    let r = y(null);
    try {
      for (let o = 0; o < n.length; o += 2) {
        let i = n[o], s = n[o + 1];
        if (s !== -1) {
          let a = e6.data[s];
          Jr(i), a.contentQueries(2, t[s], s);
        }
      }
    } finally {
      y(r);
    }
  }
}
function Do(e6, t, n) {
  Jr(0);
  let r = y(null);
  try {
    t(e6, n);
  } finally {
    y(r);
  }
}
function Ku(e6, t, n) {
  if ($r(t)) {
    let r = y(null);
    try {
      let o = t.directiveStart, i = t.directiveEnd;
      for (let s = o; s < i; s++) {
        let a = e6.data[s];
        if (a.contentQueries) {
          let c = n[s];
          a.contentQueries(1, c, s);
        }
      }
    } finally {
      y(r);
    }
  }
}
var z = function(e6) {
  return e6[e6.Emulated = 0] = "Emulated", e6[e6.None = 2] = "None", e6[e6.ShadowDom = 3] = "ShadowDom", e6[e6.ExperimentalIsolatedShadowDom = 4] = "ExperimentalIsolatedShadowDom", e6;
}(z || {});
function Ju(e6, t) {
  return e6.createText(t);
}
function Xu(e6, t, n) {
  e6.setValue(t, n);
}
function ga(e6, t, n) {
  return e6.createElement(t, n);
}
function vo(e6, t, n, r, o) {
  e6.insertBefore(t, n, r, o);
}
function ma(e6, t, n) {
  e6.appendChild(t, n);
}
function ks(e6, t, n, r, o) {
  r !== null ? vo(e6, t, n, r, o) : ma(e6, t, n);
}
function el(e6, t, n, r) {
  e6.removeChild(null, t, n, r);
}
function tl(e6, t, n) {
  e6.setAttribute(t, "style", n);
}
function nl(e6, t, n) {
  n === "" ? e6.removeAttribute(t, "class") : e6.setAttribute(t, "class", n);
}
function ya(e6, t, n) {
  let { mergedAttrs: r, classes: o, styles: i } = n;
  r !== null && Au(e6, t, r), o !== null && nl(e6, t, o), i !== null && tl(e6, t, i);
}
var rl = "ng-template";
function ol(e6) {
  return e6.type === 4 && e6.value !== rl;
}
function Eo(e6) {
  return (e6 & 1) === 0;
}
function Fs(e6, t) {
  return e6 ? ":not(" + t.trim() + ")" : t;
}
function il(e6) {
  let t = e6[0], n = 1, r = 2, o = "", i = false;
  for (; n < e6.length; ) {
    let s = e6[n];
    if (typeof s == "string")
      if (r & 2) {
        let a = e6[++n];
        o += "[" + s + (a.length > 0 ? '="' + a + '"' : "") + "]";
      } else
        r & 8 ? o += "." + s : r & 4 && (o += " " + s);
    else
      o !== "" && !Eo(s) && (t += Fs(i, o), o = ""), r = s, i = i || !Eo(r);
    n++;
  }
  return o !== "" && (t += Fs(i, o)), t;
}
function sl(e6) {
  return e6.map(il).join(",");
}
function al(e6) {
  let t = [], n = [], r = 1, o = 2;
  for (; r < e6.length; ) {
    let i = e6[r];
    if (typeof i == "string")
      o === 2 ? i !== "" && t.push(i, e6[++r]) : o === 8 && n.push(i);
    else {
      if (!Eo(o))
        break;
      o = i;
    }
    r++;
  }
  return n.length && t.push(1, ...n), t;
}
var qe = {};
function Da(e6, t, n, r, o, i, s, a, c, u, l) {
  let d = U + r, p = d + o, f = cl(d, p), T = typeof u == "function" ? u() : u;
  return f[m] = { type: e6, blueprint: f, template: n, queries: null, viewQuery: a, declTNode: t, data: f.slice().fill(null, d), bindingStartIndex: d, expandoStartIndex: p, hostBindingOpCodes: null, firstCreatePass: true, firstUpdatePass: true, staticViewQueries: false, staticContentQueries: false, preOrderHooks: null, preOrderCheckHooks: null, contentHooks: null, contentCheckHooks: null, viewHooks: null, viewCheckHooks: null, destroyHooks: null, cleanup: null, contentQueries: null, components: null, directiveRegistry: typeof i == "function" ? i() : i, pipeRegistry: typeof s == "function" ? s() : s, firstChild: null, schemas: c, consts: T, incompleteFirstPass: false, ssrId: l };
}
function cl(e6, t) {
  let n = [];
  for (let r = 0; r < t; r++)
    n.push(r < e6 ? null : qe);
  return n;
}
function ul(e6) {
  let t = e6.tView;
  return t === null || t.incompleteFirstPass ? e6.tView = Da(1, null, e6.template, e6.decls, e6.vars, e6.directiveDefs, e6.pipeDefs, e6.viewQuery, e6.schemas, e6.consts, e6.id) : t;
}
function va(e6, t, n, r, o, i, s, a, c, u, l) {
  let d = t.blueprint.slice();
  return d[q] = o, d[h] = r | 4 | 128 | 8 | 64 | 1024, (u !== null || e6 && e6[h] & 2048) && (d[h] |= 2048), Ur(d), d[O] = d[Le] = e6, d[k] = n, d[ne] = s || e6 && e6[ne], d[P] = a || e6 && e6[P], d[Ee] = c || e6 && e6[Ee] || null, d[te] = i, d[ie] = Wu(), d[rn] = l, d[Hr] = u, d[Z] = t.type == 2 ? e6[Z] : d, d;
}
function ll(e6, t, n) {
  let r = Ve(t, e6), o = ul(n), i = e6[ne].rendererFactory, s = dl(e6, va(e6, o, null, Ea(n), r, t, null, i.createRenderer(r, n), null, null, null));
  return e6[t.index] = s;
}
function Ea(e6) {
  let t = 16;
  return e6.signals ? t = 4096 : e6.onPush && (t = 64), t;
}
function Ia(e6, t, n, r) {
  if (n === 0)
    return -1;
  let o = t.length;
  for (let i = 0; i < n; i++)
    t.push(r), e6.blueprint.push(r), e6.data.push(null);
  return o;
}
function dl(e6, t) {
  return e6[Fe] ? e6[Vr][ee] = t : e6[Fe] = t, e6[Vr] = t, t;
}
function ko(e6 = 1) {
  Ca(qr(), Y(), hn() + e6, false);
}
function Ca(e6, t, n, r) {
  if (!r)
    if ((t[h] & 3) === 3) {
      let i = e6.preOrderCheckHooks;
      i !== null && mn(t, i, n);
    } else {
      let i = e6.preOrderHooks;
      i !== null && yn(t, i, 0, n);
    }
  le(n);
}
var Nn = function(e6) {
  return e6[e6.None = 0] = "None", e6[e6.SignalBased = 1] = "SignalBased", e6[e6.HasDecoratorInputTransform = 2] = "HasDecoratorInputTransform", e6;
}(Nn || {});
function Io(e6, t, n, r) {
  let o = y(null);
  try {
    let [i, s, a] = e6.inputs[n], c = null;
    (s & Nn.SignalBased) !== 0 && (c = t[i][G]), c !== null && c.transformFn !== void 0 ? r = c.transformFn(r) : a !== null && (r = a.call(t, r)), e6.setInput !== null ? e6.setInput(t, c, r, n, i) : Ws(t, c, i, r);
  } finally {
    y(o);
  }
}
var Te = function(e6) {
  return e6[e6.Important = 1] = "Important", e6[e6.DashCase = 2] = "DashCase", e6;
}(Te || {});
var fl;
function wa(e6, t) {
  return fl(e6, t);
}
var Jg = typeof document < "u" && typeof document?.documentElement?.getAnimations == "function";
var Co = /* @__PURE__ */ new WeakMap();
var yt = /* @__PURE__ */ new WeakSet();
function pl(e6, t) {
  let n = Co.get(e6);
  if (!n || n.length === 0)
    return;
  let r = t.parentNode, o = t.previousSibling;
  for (let i = n.length - 1; i >= 0; i--) {
    let s = n[i], a = s.parentNode;
    s === t ? (n.splice(i, 1), yt.add(s), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } }))) : (o && s === o || a && r && a !== r) && (n.splice(i, 1), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } })), s.parentNode?.removeChild(s));
  }
}
function hl(e6, t) {
  let n = Co.get(e6);
  n ? n.includes(t) || n.push(t) : Co.set(e6, [t]);
}
var We = /* @__PURE__ */ new Set();
var Fo = function(e6) {
  return e6[e6.CHANGE_DETECTION = 0] = "CHANGE_DETECTION", e6[e6.AFTER_NEXT_RENDER = 1] = "AFTER_NEXT_RENDER", e6;
}(Fo || {});
var Ze = new D("");
var Ls = /* @__PURE__ */ new Set();
function Ta(e6) {
  Ls.has(e6) || (Ls.add(e6), performance?.mark?.("mark_feature_usage", { detail: { feature: e6 } }));
}
var Ma = (() => {
  class e6 {
    impl = null;
    execute() {
      this.impl?.execute();
    }
    static \u0275prov = _({ token: e6, providedIn: "root", factory: () => new e6() });
  }
  return e6;
})();
var gl = new D("", { factory: () => ({ queue: /* @__PURE__ */ new Set(), isScheduled: false, scheduler: null, injector: v($) }) });
function _a(e6, t, n) {
  let r = e6.get(gl);
  if (Array.isArray(t))
    for (let o of t)
      r.queue.add(o), n?.detachedLeaveAnimationFns?.push(o);
  else
    r.queue.add(t), n?.detachedLeaveAnimationFns?.push(t);
  r.scheduler && r.scheduler(e6);
}
function ml(e6, t) {
  for (let [n, r] of t)
    _a(e6, r.animateFns);
}
function Ps(e6, t, n, r) {
  let o = e6?.[Pe]?.enter;
  t !== null && o && o.has(n.index) && ml(r, o);
}
function ze(e6, t, n, r, o, i, s, a) {
  if (o != null) {
    let c, u = false;
    ae(o) ? c = o : se(o) && (u = true, o = o[q]);
    let l = ce(o);
    e6 === 0 && r !== null ? (Ps(a, r, i, n), s == null ? ma(t, r, l) : vo(t, r, l, s || null, true)) : e6 === 1 && r !== null ? (Ps(a, r, i, n), vo(t, r, l, s || null, true), pl(i, l)) : e6 === 2 ? (a?.[Pe]?.leave?.has(i.index) && hl(i, l), yt.delete(l), js(a, i, n, (d) => {
      if (yt.has(l)) {
        yt.delete(l);
        return;
      }
      el(t, l, u, d);
    })) : e6 === 3 && (yt.delete(l), js(a, i, n, () => {
      t.destroyNode(l);
    })), c != null && Al(t, e6, n, c, i, r, s);
  }
}
function yl(e6, t) {
  Sa(e6, t), t[q] = null, t[te] = null;
}
function Sa(e6, t) {
  t[ne].changeDetectionScheduler?.notify(9), jo(e6, t, t[P], 2, null, null);
}
function Dl(e6) {
  let t = e6[Fe];
  if (!t)
    return fo(e6[m], e6);
  for (; t; ) {
    let n = null;
    if (se(t))
      n = t[Fe];
    else {
      let r = t[re];
      r && (n = r);
    }
    if (!n) {
      for (; t && !t[ee] && t !== e6; )
        se(t) && fo(t[m], t), t = t[O];
      t === null && (t = e6), se(t) && fo(t[m], t), n = t && t[ee];
    }
    t = n;
  }
}
function Lo(e6, t) {
  let n = e6[ut], r = n.indexOf(t);
  n.splice(r, 1);
}
function vl(e6, t) {
  if (Ce(t))
    return;
  let n = t[P];
  n.destroyNode && jo(e6, t, n, 3, null, null), Dl(t);
}
function fo(e6, t) {
  if (Ce(t))
    return;
  let n = y(null);
  try {
    t[h] &= -129, t[h] |= 256, t[F] && jt(t[F]), Cl(e6, t), Il(e6, t), t[m].type === 1 && t[P].destroy();
    let r = t[at];
    if (r !== null && ae(t[O])) {
      r !== t[O] && Lo(r, t);
      let o = t[sn];
      o !== null && o.detachView(e6);
    }
    yo(t);
  } finally {
    y(n);
  }
}
function js(e6, t, n, r) {
  let o = e6?.[Pe];
  if (o == null || o.leave == null || !o.leave.has(t.index))
    return r(false);
  e6 && We.add(e6[ie]), _a(n, () => {
    if (o.leave && o.leave.has(t.index)) {
      let s = o.leave.get(t.index), a = [];
      if (s) {
        for (let c = 0; c < s.animateFns.length; c++) {
          let u = s.animateFns[c], { promise: l } = u();
          a.push(l);
        }
        o.detachedLeaveAnimationFns = void 0;
      }
      o.running = Promise.allSettled(a), El(e6, r);
    } else
      e6 && We.delete(e6[ie]), r(false);
  }, o);
}
function El(e6, t) {
  let n = e6[Pe]?.running;
  if (n) {
    n.then(() => {
      e6[Pe].running = void 0, We.delete(e6[ie]), t(true);
    });
    return;
  }
  t(false);
}
function Il(e6, t) {
  let n = e6.cleanup, r = t[on];
  if (n !== null)
    for (let s = 0; s < n.length - 1; s += 2)
      if (typeof n[s] == "string") {
        let a = n[s + 3];
        a >= 0 ? r[a]() : r[-a].unsubscribe(), s += 2;
      } else {
        let a = r[n[s + 1]];
        n[s].call(a);
      }
  r !== null && (t[on] = null);
  let o = t[J];
  if (o !== null) {
    t[J] = null;
    for (let s = 0; s < o.length; s++) {
      let a = o[s];
      a();
    }
  }
  let i = t[ct];
  if (i !== null) {
    t[ct] = null;
    for (let s of i)
      s.destroy();
  }
}
function Cl(e6, t) {
  let n;
  if (e6 != null && (n = e6.destroyHooks) != null)
    for (let r = 0; r < n.length; r += 2) {
      let o = t[n[r]];
      if (!(o instanceof vt)) {
        let i = n[r + 1];
        if (Array.isArray(i))
          for (let s = 0; s < i.length; s += 2) {
            let a = o[i[s]], c = i[s + 1];
            M(I.LifecycleHookStart, a, c);
            try {
              c.call(a);
            } finally {
              M(I.LifecycleHookEnd, a, c);
            }
          }
        else {
          M(I.LifecycleHookStart, o, i);
          try {
            i.call(o);
          } finally {
            M(I.LifecycleHookEnd, o, i);
          }
        }
      }
    }
}
function wl(e6, t, n) {
  return Tl(e6, t.parent, n);
}
function Tl(e6, t, n) {
  let r = t;
  for (; r !== null && r.type & 168; )
    t = r, r = t.parent;
  if (r === null)
    return n[q];
  if (lt(r)) {
    let { encapsulation: o } = e6.data[r.directiveStart + r.componentOffset];
    if (o === z.None || o === z.Emulated)
      return null;
  }
  return Ve(r, n);
}
function Ml(e6, t, n) {
  return Sl(e6, t, n);
}
function _l(e6, t, n) {
  return e6.type & 40 ? Ve(e6, n) : null;
}
var Sl = _l;
var Bs;
function ba(e6, t, n, r) {
  let o = wl(e6, r, t), i = t[P], s = r.parent || t[te], a = Ml(s, r, t);
  if (o != null)
    if (Array.isArray(n))
      for (let c = 0; c < n.length; c++)
        ks(i, o, n[c], a, false);
    else
      ks(i, o, n, a, false);
  Bs !== void 0 && Bs(i, r, t, n, o);
}
function bl(e6, t) {
  if (t !== null) {
    let r = e6[Z][te], o = t.projection;
    return r.projection[o];
  }
  return null;
}
function Po(e6, t, n, r, o, i, s) {
  for (; n != null; ) {
    let a = r[Ee];
    if (n.type === 128) {
      n = n.next;
      continue;
    }
    let c = r[n.index], u = n.type;
    if (s && t === 0 && (c && Et(ce(c), r), n.flags |= 2), !Oo(n))
      if (u & 8)
        Po(e6, t, n.child, r, o, i, false), ze(t, e6, a, o, c, n, i, r);
      else if (u & 32) {
        let l = wa(n, r), d;
        for (; d = l(); )
          ze(t, e6, a, o, d, n, i, r);
        ze(t, e6, a, o, c, n, i, r);
      } else
        u & 16 ? Nl(e6, t, r, n, o, i) : ze(t, e6, a, o, c, n, i, r);
    n = s ? n.projectionNext : n.next;
  }
}
function jo(e6, t, n, r, o, i) {
  Po(n, r, e6.firstChild, t, o, i, false);
}
function Nl(e6, t, n, r, o, i) {
  let s = n[Z], c = s[te].projection[r.projection];
  if (Array.isArray(c))
    for (let u = 0; u < c.length; u++) {
      let l = c[u];
      ze(t, e6, n[Ee], o, l, r, i, n);
    }
  else {
    let u = c, l = s[O];
    zu(r) && (u.flags |= 128), Po(e6, t, u, l, o, i, true);
  }
}
function Al(e6, t, n, r, o, i, s) {
  let a = r[un], c = ce(r);
  a !== c && ze(t, e6, n, i, a, o, s);
  for (let u = re; u < r.length; u++) {
    let l = r[u];
    jo(l[m], l, e6, t, i, a);
  }
}
function Na(e6, t, n, r, o) {
  let i = hn(), s = r & 2;
  try {
    le(-1), s && t.length > U && Ca(e6, t, U, false);
    let a = s ? I.TemplateUpdateStart : I.TemplateCreateStart;
    M(a, o, n), n(r, o);
  } finally {
    le(i);
    let a = s ? I.TemplateUpdateEnd : I.TemplateCreateEnd;
    M(a, o, n);
  }
}
function xl(e6, t, n) {
  Ll(e6, t, n), (n.flags & 64) === 64 && Pl(e6, t, n);
}
function Rl(e6, t, n = Ve) {
  let r = t.localNames;
  if (r !== null) {
    let o = t.index + 1;
    for (let i = 0; i < r.length; i += 2) {
      let s = r[i + 1], a = s === -1 ? n(t, e6) : e6[s];
      e6[o++] = a;
    }
  }
}
function Ol(e6, t, n, r) {
  let i = r.get(fa, da) || n === z.ShadowDom || n === z.ExperimentalIsolatedShadowDom, s = e6.selectRootElement(t, i);
  return kl(s), s;
}
function kl(e6) {
  Fl(e6);
}
var Fl = () => null;
function Ll(e6, t, n) {
  let r = n.directiveStart, o = n.directiveEnd;
  lt(n) && ll(t, n, e6.data[r + n.componentOffset]), e6.firstCreatePass || Js(n, t);
  let i = n.initialInputs;
  for (let s = r; s < o; s++) {
    let a = e6.data[s], c = mo(t, e6, s, n);
    if (Et(c, t), i !== null && Bl(t, s - r, c, a, n, i), je(a)) {
      let u = ue(n.index, t);
      u[k] = mo(t, e6, s, n);
    }
  }
}
function Pl(e6, t, n) {
  let r = n.directiveStart, o = n.directiveEnd, i = n.index, s = hs();
  try {
    le(i);
    for (let a = r; a < o; a++) {
      let c = e6.data[a], u = t[a];
      dn(a), (c.hostBindings !== null || c.hostVars !== 0 || c.hostAttrs !== null) && jl(c, u);
    }
  } finally {
    le(-1), dn(s);
  }
}
function jl(e6, t) {
  e6.hostBindings !== null && e6.hostBindings(1, t);
}
function Bl(e6, t, n, r, o, i) {
  let s = i[t];
  if (s !== null)
    for (let a = 0; a < s.length; a += 2) {
      let c = s[a], u = s[a + 1];
      Io(r, n, c, u);
    }
}
function Vl(e6, t, n, r, o) {
  let i = U + n, s = t[m], a = o(s, t, e6, r, n);
  t[i] = a, ht(e6, true);
  let c = e6.type === 2;
  return c ? (ya(t[P], a, e6), (ns() === 0 || Qi(e6)) && Et(a, t), rs()) : Et(a, t), to() && (!c || !Oo(e6)) && ba(s, t, a, e6), e6;
}
function Hl(e6) {
  let t = e6;
  return Yr() ? us() : (t = t.parent, ht(t, false)), t;
}
function $l(e6, t, n, r, o) {
  let i = e6.inputs?.[r], s = e6.hostDirectiveInputs?.[r], a = false;
  if (s)
    for (let c = 0; c < s.length; c += 2) {
      let u = s[c], l = s[c + 1], d = t.data[u];
      Io(d, n[u], l, o), a = true;
    }
  if (i)
    for (let c of i) {
      let u = n[c], l = t.data[c];
      Io(l, u, r, o), a = true;
    }
  return a;
}
function Ul(e6, t) {
  let n = ue(t, e6), r = n[m];
  zl(r, n);
  let o = n[q];
  o !== null && n[rn] === null && (n[rn] = pa(o, n[Ee])), M(I.ComponentStart);
  try {
    Aa(r, n, n[k]);
  } finally {
    M(I.ComponentEnd, n[k]);
  }
}
function zl(e6, t) {
  for (let n = t.length; n < e6.blueprint.length; n++)
    t.push(e6.blueprint[n]);
}
function Aa(e6, t, n) {
  fn(t);
  try {
    let r = e6.viewQuery;
    r !== null && Do(1, r, n);
    let o = e6.template;
    o !== null && Na(e6, t, o, 1, n), e6.firstCreatePass && (e6.firstCreatePass = false), t[sn]?.finishViewCreation(e6), e6.staticContentQueries && ha(e6, t), e6.staticViewQueries && Do(2, e6.viewQuery, n);
    let i = e6.components;
    i !== null && Gl(t, i);
  } catch (r) {
    throw e6.firstCreatePass && (e6.incompleteFirstPass = true, e6.firstCreatePass = false), r;
  } finally {
    t[h] &= -5, pn();
  }
}
function Gl(e6, t) {
  for (let n = 0; n < t.length; n++)
    Ul(e6, t[n]);
}
function It(e6, t, n, r, o = false) {
  for (; n !== null; ) {
    if (n.type === 128) {
      n = o ? n.projectionNext : n.next;
      continue;
    }
    let i = t[n.index];
    i !== null && r.push(ce(i)), ae(i) && xa(i, r);
    let s = n.type;
    if (s & 8)
      It(e6, t, n.child, r);
    else if (s & 32) {
      let a = wa(n, t), c;
      for (; c = a(); )
        r.push(c);
    } else if (s & 16) {
      let a = bl(t, n);
      if (Array.isArray(a))
        r.push(...a);
      else {
        let c = me(t[Z]);
        It(c[m], c, a, r, true);
      }
    }
    n = o ? n.projectionNext : n.next;
  }
  return r;
}
function xa(e6, t) {
  for (let n = re; n < e6.length; n++) {
    let r = e6[n], o = r[m].firstChild;
    o !== null && It(r[m], r, o, t);
  }
  e6[un] !== e6[q] && t.push(e6[un]);
}
function Ra(e6) {
  if (e6[cn] !== null) {
    for (let t of e6[cn])
      t.impl.addSequence(t);
    e6[cn].length = 0;
  }
}
var Oa = [];
function Wl(e6) {
  return e6[F] ?? ql(e6);
}
function ql(e6) {
  let t = Oa.pop() ?? Object.create(Yl);
  return t.lView = e6, t;
}
function Zl(e6) {
  e6.lView[F] !== e6 && (e6.lView = null, Oa.push(e6));
}
var Yl = B(A({}, Pt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e6) => {
  pt(e6.lView);
}, consumerOnSignalRead() {
  this.lView[F] = this;
} });
function Ql(e6) {
  let t = e6[F] ?? Object.create(Kl);
  return t.lView = e6, t;
}
var Kl = B(A({}, Pt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e6) => {
  let t = me(e6.lView);
  for (; t && !ka(t[m]); )
    t = me(t);
  t && zr(t);
}, consumerOnSignalRead() {
  this.lView[F] = this;
} });
function ka(e6) {
  return e6.type !== 2;
}
function Fa(e6) {
  if (e6[ct] === null)
    return;
  let t = true;
  for (; t; ) {
    let n = false;
    for (let r of e6[ct])
      r.dirty && (n = true, r.zone === null || Zone.current === r.zone ? r.run() : r.zone.run(() => r.run()));
    t = n && !!(e6[h] & 8192);
  }
}
var Jl = 100;
function La(e6, t = 0) {
  let r = e6[ne].rendererFactory, o = false;
  o || r.begin?.();
  try {
    Xl(e6, t);
  } finally {
    o || r.end?.();
  }
}
function Xl(e6, t) {
  let n = Qr();
  try {
    Kr(true), wo(e6, t);
    let r = 0;
    for (; ft(e6); ) {
      if (r === Jl)
        throw new g(103, false);
      r++, wo(e6, 1);
    }
  } finally {
    Kr(n);
  }
}
function ed(e6, t, n, r) {
  if (Ce(t))
    return;
  let o = t[h], i = false, s = false;
  fn(t);
  let a = true, c = null, u = null;
  i || (ka(e6) ? (u = Wl(t), c = Yn(u)) : Lt() === null ? (a = false, u = Ql(t), c = Yn(u)) : t[F] && (jt(t[F]), t[F] = null));
  try {
    Ur(t), ls(e6.bindingStartIndex), n !== null && Na(e6, t, n, 2, r);
    let l = (o & 3) === 3;
    if (!i)
      if (l) {
        let f = e6.preOrderCheckHooks;
        f !== null && mn(t, f, null);
      } else {
        let f = e6.preOrderHooks;
        f !== null && yn(t, f, 0, null), uo(t, 0);
      }
    if (s || td(t), Fa(t), Pa(t, 0), e6.contentQueries !== null && ha(e6, t), !i)
      if (l) {
        let f = e6.contentCheckHooks;
        f !== null && mn(t, f);
      } else {
        let f = e6.contentHooks;
        f !== null && yn(t, f, 1), uo(t, 1);
      }
    rd(e6, t);
    let d = e6.components;
    d !== null && Ba(t, d, 0);
    let p = e6.viewQuery;
    if (p !== null && Do(2, p, r), !i)
      if (l) {
        let f = e6.viewCheckHooks;
        f !== null && mn(t, f);
      } else {
        let f = e6.viewHooks;
        f !== null && yn(t, f, 2), uo(t, 2);
      }
    if (e6.firstUpdatePass === true && (e6.firstUpdatePass = false), t[an]) {
      for (let f of t[an])
        f();
      t[an] = null;
    }
    i || (Ra(t), t[h] &= -73);
  } catch (l) {
    throw i || pt(t), l;
  } finally {
    u !== null && (ci(u, c), a && Zl(u)), pn();
  }
}
function Pa(e6, t) {
  for (let n = ca(e6); n !== null; n = ua(n))
    for (let r = re; r < n.length; r++) {
      let o = n[r];
      ja(o, t);
    }
}
function td(e6) {
  for (let t = ca(e6); t !== null; t = ua(t)) {
    if (!(t[h] & 2))
      continue;
    let n = t[ut];
    for (let r = 0; r < n.length; r++) {
      let o = n[r];
      zr(o);
    }
  }
}
function nd(e6, t, n) {
  M(I.ComponentStart);
  let r = ue(t, e6);
  try {
    ja(r, n);
  } finally {
    M(I.ComponentEnd, r[k]);
  }
}
function ja(e6, t) {
  ln(e6) && wo(e6, t);
}
function wo(e6, t) {
  let r = e6[m], o = e6[h], i = e6[F], s = !!(t === 0 && o & 16);
  if (s ||= !!(o & 64 && t === 0), s ||= !!(o & 1024), s ||= !!(i?.dirty && Qn(i)), s ||= false, i && (i.dirty = false), e6[h] &= -9217, s)
    ed(r, e6, r.template, e6[k]);
  else if (o & 8192) {
    let a = y(null);
    try {
      Fa(e6), Pa(e6, 1);
      let c = r.components;
      c !== null && Ba(e6, c, 1), Ra(e6);
    } finally {
      y(a);
    }
  }
}
function Ba(e6, t, n) {
  for (let r = 0; r < t.length; r++)
    nd(e6, t[r], n);
}
function rd(e6, t) {
  let n = e6.hostBindingOpCodes;
  if (n !== null)
    try {
      for (let r = 0; r < n.length; r++) {
        let o = n[r];
        if (o < 0)
          le(~o);
        else {
          let i = o, s = n[++r], a = n[++r];
          ps(s, i);
          let c = t[i];
          M(I.HostBindingsUpdateStart, c);
          try {
            a(2, c);
          } finally {
            M(I.HostBindingsUpdateEnd, c);
          }
        }
      }
    } finally {
      le(-1);
    }
}
function Va(e6, t) {
  let n = Qr() ? 64 : 1088;
  for (e6[ne].changeDetectionScheduler?.notify(t); e6; ) {
    e6[h] |= n;
    let r = me(e6);
    if (Be(e6) && !r)
      return e6;
    e6 = r;
  }
  return null;
}
function od(e6, t) {
  if (e6.length <= re)
    return;
  let n = re + t, r = e6[n];
  if (r) {
    let o = r[at];
    o !== null && o !== e6 && Lo(o, r), t > 0 && (e6[n - 1][ee] = r[ee]);
    let i = Fr(e6, re + t);
    yl(r[m], r);
    let s = i[sn];
    s !== null && s.detachView(i[m]), r[O] = null, r[ee] = null, r[h] &= -129;
  }
  return r;
}
function id(e6, t) {
  let n = e6[ut], r = t[O];
  if (se(r))
    e6[h] |= 2;
  else {
    let o = r[O][Z];
    t[Z] !== o && (e6[h] |= 2);
  }
  n === null ? e6[ut] = [t] : n.push(t);
}
var In = class {
  _lView;
  _cdRefInjectingView;
  _appRef = null;
  _attachedToViewContainer = false;
  exhaustive;
  get rootNodes() {
    let t = this._lView, n = t[m];
    return It(n, t, n.firstChild, []);
  }
  constructor(t, n) {
    this._lView = t, this._cdRefInjectingView = n;
  }
  get context() {
    return this._lView[k];
  }
  set context(t) {
    this._lView[k] = t;
  }
  get destroyed() {
    return Ce(this._lView);
  }
  destroy() {
    if (this._appRef)
      this._appRef.detachView(this);
    else if (this._attachedToViewContainer) {
      let t = this._lView[O];
      if (ae(t)) {
        let n = t[Yi], r = n ? n.indexOf(this) : -1;
        r > -1 && (od(t, r), Fr(n, r));
      }
      this._attachedToViewContainer = false;
    }
    vl(this._lView[m], this._lView);
  }
  onDestroy(t) {
    Wr(this._lView, t);
  }
  markForCheck() {
    Va(this._cdRefInjectingView || this._lView, 4);
  }
  detach() {
    this._lView[h] &= -129;
  }
  reattach() {
    Gr(this._lView), this._lView[h] |= 128;
  }
  detectChanges() {
    this._lView[h] |= 1024, La(this._lView);
  }
  checkNoChanges() {
  }
  attachToViewContainerRef() {
    if (this._appRef)
      throw new g(902, false);
    this._attachedToViewContainer = true;
  }
  detachFromAppRef() {
    this._appRef = null;
    let t = Be(this._lView), n = this._lView[at];
    n !== null && !t && Lo(n, this._lView), Sa(this._lView[m], this._lView);
  }
  attachToAppRef(t) {
    if (this._attachedToViewContainer)
      throw new g(902, false);
    this._appRef = t;
    let n = Be(this._lView), r = this._lView[at];
    r !== null && !n && id(r, this._lView), Gr(this._lView);
  }
};
function Bo(e6, t, n, r, o) {
  let i = e6.data[t];
  if (i === null)
    i = sd(e6, t, n, r, o), fs() && (i.flags |= 32);
  else if (i.type & 64) {
    i.type = n, i.value = r, i.attrs = o;
    let s = cs();
    i.injectorIndex = s === null ? -1 : s.injectorIndex;
  }
  return ht(i, true), i;
}
function sd(e6, t, n, r, o) {
  let i = Zr(), s = Yr(), a = s ? i : i && i.parent, c = e6.data[t] = cd(e6, a, n, t, r, o);
  return ad(e6, c, i, s), c;
}
function ad(e6, t, n, r) {
  e6.firstChild === null && (e6.firstChild = t), n !== null && (r ? n.child == null && t.parent !== null && (n.child = t) : n.next === null && (n.next = t, t.prev = n));
}
function cd(e6, t, n, r, o, i) {
  let s = t ? t.injectorIndex : -1, a = 0;
  return is() && (a |= 128), { type: n, index: r, insertBeforeIndex: null, injectorIndex: s, directiveStart: -1, directiveEnd: -1, directiveStylingLast: -1, componentOffset: -1, controlDirectiveIndex: -1, customControlIndex: -1, propertyBindings: null, flags: a, providerIndexes: 0, value: o, attrs: i, mergedAttrs: null, localNames: null, initialInputs: null, inputs: null, hostDirectiveInputs: null, outputs: null, hostDirectiveOutputs: null, directiveToIndex: null, tView: null, next: null, prev: null, projectionNext: null, child: null, parent: t, projection: null, styles: null, stylesWithoutHost: null, residualStyles: void 0, classes: null, classesWithoutHost: null, residualClasses: void 0, classBindings: 0, styleBindings: 0 };
}
var Ha = class {
};
var An = class {
};
var To = class {
  resolveComponentFactory(t) {
    throw new g(917, false);
  }
};
var xn = class {
  static NULL = new To();
};
var we = class {
};
var $a = (() => {
  class e6 {
    static \u0275prov = _({ token: e6, providedIn: "root", factory: () => null });
  }
  return e6;
})();
var Dn = {};
var Mo = class {
  injector;
  parentInjector;
  constructor(t, n) {
    this.injector = t, this.parentInjector = n;
  }
  get(t, n, r) {
    let o = this.injector.get(t, Dn, r);
    return o !== Dn || n === Dn ? o : this.parentInjector.get(t, n, r);
  }
};
function Cn(e6, t, n) {
  let r = n ? e6.styles : null, o = n ? e6.classes : null, i = 0;
  if (t !== null)
    for (let s = 0; s < t.length; s++) {
      let a = t[s];
      if (typeof a == "number")
        i = a;
      else if (i == 1)
        o = _r(o, a);
      else if (i == 2) {
        let c = a, u = t[++s];
        r = _r(r, c + ": " + u + ";");
      }
    }
  n ? e6.styles = r : e6.stylesWithoutHost = r, n ? e6.classes = o : e6.classesWithoutHost = o;
}
function Tt(e6, t = 0) {
  let n = Y();
  if (n === null)
    return E(e6, t);
  let r = He();
  return ra(r, n, R(e6), t);
}
function ud(e6, t, n, r, o) {
  let i = r === null ? null : { "": -1 }, s = o(e6, n);
  if (s !== null) {
    let a = s, c = null, u = null;
    for (let l of s)
      if (l.resolveHostDirectives !== null) {
        [a, c, u] = l.resolveHostDirectives(s);
        break;
      }
    fd(e6, t, n, a, i, c, u);
  }
  i !== null && r !== null && ld(n, r, i);
}
function ld(e6, t, n) {
  let r = e6.localNames = [];
  for (let o = 0; o < t.length; o += 2) {
    let i = n[t[o + 1]];
    if (i == null)
      throw new g(-301, false);
    r.push(t[o], i);
  }
}
function dd(e6, t, n) {
  t.componentOffset = n, (e6.components ??= []).push(t.index);
}
function fd(e6, t, n, r, o, i, s) {
  let a = r.length, c = null;
  for (let p = 0; p < a; p++) {
    let f = r[p];
    c === null && je(f) && (c = f, dd(e6, n, p)), Pu(Js(n, t), e6, f.type);
  }
  Dd(n, e6.data.length, a), c?.viewProvidersResolver && c.viewProvidersResolver(c);
  for (let p = 0; p < a; p++) {
    let f = r[p];
    f.providersResolver && f.providersResolver(f);
  }
  let u = false, l = false, d = Ia(e6, t, a, null);
  a > 0 && (n.directiveToIndex = /* @__PURE__ */ new Map());
  for (let p = 0; p < a; p++) {
    let f = r[p];
    if (n.mergedAttrs = No(n.mergedAttrs, f.hostAttrs), hd(e6, n, t, d, f), yd(d, f, o), s !== null && s.has(f)) {
      let [zn, lc] = s.get(f);
      n.directiveToIndex.set(f.type, [d, zn + n.directiveStart, lc + n.directiveStart]);
    } else
      (i === null || !i.has(f)) && n.directiveToIndex.set(f.type, d);
    f.contentQueries !== null && (n.flags |= 4), (f.hostBindings !== null || f.hostAttrs !== null || f.hostVars !== 0) && (n.flags |= 64);
    let T = f.type.prototype;
    !u && (T.ngOnChanges || T.ngOnInit || T.ngDoCheck) && ((e6.preOrderHooks ??= []).push(n.index), u = true), !l && (T.ngOnChanges || T.ngDoCheck) && ((e6.preOrderCheckHooks ??= []).push(n.index), l = true), d++;
  }
  pd(e6, n, i);
}
function pd(e6, t, n) {
  for (let r = t.directiveStart; r < t.directiveEnd; r++) {
    let o = e6.data[r];
    if (n === null || !n.has(o))
      Vs(0, t, o, r), Vs(1, t, o, r), $s(t, r, false);
    else {
      let i = n.get(o);
      Hs(0, t, i, r), Hs(1, t, i, r), $s(t, r, true);
    }
  }
}
function Vs(e6, t, n, r) {
  let o = e6 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s;
      e6 === 0 ? s = t.inputs ??= {} : s = t.outputs ??= {}, s[i] ??= [], s[i].push(r), Ua(t, i);
    }
}
function Hs(e6, t, n, r) {
  let o = e6 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s = o[i], a;
      e6 === 0 ? a = t.hostDirectiveInputs ??= {} : a = t.hostDirectiveOutputs ??= {}, a[s] ??= [], a[s].push(r, i), Ua(t, s);
    }
}
function Ua(e6, t) {
  t === "class" ? e6.flags |= 8 : t === "style" && (e6.flags |= 16);
}
function $s(e6, t, n) {
  let { attrs: r, inputs: o, hostDirectiveInputs: i } = e6;
  if (r === null || !n && o === null || n && i === null || ol(e6)) {
    e6.initialInputs ??= [], e6.initialInputs.push(null);
    return;
  }
  let s = null, a = 0;
  for (; a < r.length; ) {
    let c = r[a];
    if (c === 0) {
      a += 4;
      continue;
    } else if (c === 5) {
      a += 2;
      continue;
    } else if (typeof c == "number")
      break;
    if (!n && o.hasOwnProperty(c)) {
      let u = o[c];
      for (let l of u)
        if (l === t) {
          s ??= [], s.push(c, r[a + 1]);
          break;
        }
    } else if (n && i.hasOwnProperty(c)) {
      let u = i[c];
      for (let l = 0; l < u.length; l += 2)
        if (u[l] === t) {
          s ??= [], s.push(u[l + 1], r[a + 1]);
          break;
        }
    }
    a += 2;
  }
  e6.initialInputs ??= [], e6.initialInputs.push(s);
}
function hd(e6, t, n, r, o) {
  e6.data[r] = o;
  let i = o.factory || (o.factory = Re(o.type, true)), s = new vt(i, je(o), Tt, null);
  e6.blueprint[r] = s, n[r] = s, gd(e6, t, r, Ia(e6, n, o.hostVars, qe), o);
}
function gd(e6, t, n, r, o) {
  let i = o.hostBindings;
  if (i) {
    let s = e6.hostBindingOpCodes;
    s === null && (s = e6.hostBindingOpCodes = []);
    let a = ~t.index;
    md(s) != a && s.push(a), s.push(n, r, i);
  }
}
function md(e6) {
  let t = e6.length;
  for (; t > 0; ) {
    let n = e6[--t];
    if (typeof n == "number" && n < 0)
      return n;
  }
  return 0;
}
function yd(e6, t, n) {
  if (n) {
    if (t.exportAs)
      for (let r = 0; r < t.exportAs.length; r++)
        n[t.exportAs[r]] = e6;
    je(t) && (n[""] = e6);
  }
}
function Dd(e6, t, n) {
  e6.flags |= 1, e6.directiveStart = t, e6.directiveEnd = t + n, e6.providerIndexes = t;
}
function vd(e6, t, n, r, o, i, s, a) {
  let c = t[m], u = c.consts, l = dt(u, s), d = Bo(c, e6, n, r, l);
  return i && ud(c, t, d, dt(u, a), o), d.mergedAttrs = No(d.mergedAttrs, d.attrs), d.attrs !== null && Cn(d, d.attrs, false), d.mergedAttrs !== null && Cn(d, d.mergedAttrs, true), c.queries !== null && c.queries.elementStart(c, d), d;
}
function Ed(e6, t) {
  bu(e6, t), $r(t) && e6.queries.elementEnd(t);
}
function Id(e6, t, n, r, o, i) {
  let s = t.consts, a = dt(s, o), c = Bo(t, e6, n, r, a);
  if (c.mergedAttrs = No(c.mergedAttrs, c.attrs), i != null) {
    let u = dt(s, i);
    c.localNames = [];
    for (let l = 0; l < u.length; l += 2)
      c.localNames.push(u[l], -1);
  }
  return c.attrs !== null && Cn(c, c.attrs, false), c.mergedAttrs !== null && Cn(c, c.mergedAttrs, true), t.queries !== null && t.queries.elementStart(t, c), c;
}
function Cd(e6, t, n) {
  if (n === qe)
    return false;
  let r = e6[t];
  return Object.is(r, n) ? false : (e6[t] = n, true);
}
var _o = Symbol("BINDING");
function wd(e6) {
  return e6.debugInfo?.className || e6.type.name || null;
}
var So = class extends xn {
  ngModule;
  constructor(t) {
    super(), this.ngModule = t;
  }
  resolveComponentFactory(t) {
    let n = ot(t);
    return new wn(n, this.ngModule);
  }
};
function Td(e6) {
  return Object.keys(e6).map((t) => {
    let [n, r, o] = e6[t], i = { propName: n, templateName: t, isSignal: (r & Nn.SignalBased) !== 0 };
    return o && (i.transform = o), i;
  });
}
function Md(e6) {
  return Object.keys(e6).map((t) => ({ propName: e6[t], templateName: t }));
}
function _d(e6, t, n) {
  let r = t instanceof $ ? t : t?.injector;
  return r && e6.getStandaloneInjector !== null && (r = e6.getStandaloneInjector(r) || r), r ? new Mo(n, r) : n;
}
function Sd(e6) {
  let t = e6.get(we, null);
  if (t === null)
    throw new g(407, false);
  let n = e6.get($a, null), r = e6.get(Oe, null), o = e6.get(Ze, null, { optional: true });
  return { rendererFactory: t, sanitizer: n, changeDetectionScheduler: r, ngReflect: false, tracingService: o };
}
function bd(e6, t) {
  let n = za(e6);
  return ga(t, n, n === "svg" ? Ki : n === "math" ? Ji : null);
}
function za(e6) {
  return (e6.selectors[0][0] || "div").toLowerCase();
}
var wn = class extends An {
  componentDef;
  ngModule;
  selector;
  componentType;
  ngContentSelectors;
  isBoundToModule;
  cachedInputs = null;
  cachedOutputs = null;
  get inputs() {
    return this.cachedInputs ??= Td(this.componentDef.inputs), this.cachedInputs;
  }
  get outputs() {
    return this.cachedOutputs ??= Md(this.componentDef.outputs), this.cachedOutputs;
  }
  constructor(t, n) {
    super(), this.componentDef = t, this.ngModule = n, this.componentType = t.type, this.selector = sl(t.selectors), this.ngContentSelectors = t.ngContentSelectors ?? [], this.isBoundToModule = !!n;
  }
  create(t, n, r, o, i, s) {
    M(I.DynamicComponentStart);
    let a = y(null);
    try {
      let c = this.componentDef, u = _d(c, o || this.ngModule, t), l = Sd(u), d = l.tracingService;
      return d && d.componentCreate ? d.componentCreate(wd(c), () => this.createComponentRef(l, u, n, r, i, s)) : this.createComponentRef(l, u, n, r, i, s);
    } finally {
      y(a);
    }
  }
  createComponentRef(t, n, r, o, i, s) {
    let a = this.componentDef, c = Nd(o, a, s, i), u = t.rendererFactory.createRenderer(null, a), l = o ? Ol(u, o, a.encapsulation, n) : bd(a, u), d = s?.some(Us) || i?.some((T) => typeof T != "function" && T.bindings.some(Us)), p = va(null, c, null, 512 | Ea(a), null, null, t, u, n, null, pa(l, n, true));
    p[U] = l, fn(p);
    let f = null;
    try {
      let T = vd(U, p, 2, "#host", () => c.directiveRegistry, true, 0);
      ya(u, l, T), Et(l, p), xl(c, p, T), Ku(c, T, p), Ed(c, T), r !== void 0 && xd(T, this.ngContentSelectors, r), f = ue(T.index, p), p[k] = f[k], Aa(c, p, null);
    } catch (T) {
      throw f !== null && yo(f), yo(p), T;
    } finally {
      M(I.DynamicComponentEnd), pn();
    }
    return new Tn(this.componentType, p, !!d);
  }
};
function Nd(e6, t, n, r) {
  let o = e6 ? ["ng-version", "21.2.11"] : al(t.selectors[0]), i = null, s = null, a = 0;
  if (n)
    for (let l of n)
      a += l[_o].requiredVars, l.create && (l.targetIdx = 0, (i ??= []).push(l)), l.update && (l.targetIdx = 0, (s ??= []).push(l));
  if (r)
    for (let l = 0; l < r.length; l++) {
      let d = r[l];
      if (typeof d != "function")
        for (let p of d.bindings) {
          a += p[_o].requiredVars;
          let f = l + 1;
          p.create && (p.targetIdx = f, (i ??= []).push(p)), p.update && (p.targetIdx = f, (s ??= []).push(p));
        }
    }
  let c = [t];
  if (r)
    for (let l of r) {
      let d = typeof l == "function" ? l : l.type, p = xr(d);
      c.push(p);
    }
  return Da(0, null, Ad(i, s), 1, a, c, null, null, null, [o], null);
}
function Ad(e6, t) {
  return !e6 && !t ? null : (n) => {
    if (n & 1 && e6)
      for (let r of e6)
        r.create();
    if (n & 2 && t)
      for (let r of t)
        r.update();
  };
}
function Us(e6) {
  let t = e6[_o].kind;
  return t === "input" || t === "twoWay";
}
var Tn = class extends Ha {
  _rootLView;
  _hasInputBindings;
  instance;
  hostView;
  changeDetectorRef;
  componentType;
  location;
  previousInputValues = null;
  _tNode;
  constructor(t, n, r) {
    super(), this._rootLView = n, this._hasInputBindings = r, this._tNode = es(n[m], U), this.location = sa(this._tNode, n), this.instance = ue(this._tNode.index, n)[k], this.hostView = this.changeDetectorRef = new In(n, void 0), this.componentType = t;
  }
  setInput(t, n) {
    this._hasInputBindings;
    let r = this._tNode;
    if (this.previousInputValues ??= /* @__PURE__ */ new Map(), this.previousInputValues.has(t) && Object.is(this.previousInputValues.get(t), n))
      return;
    let o = this._rootLView, i = $l(r, o[m], o, t, n);
    this.previousInputValues.set(t, n);
    let s = ue(r.index, o);
    Va(s, 1);
  }
  get injector() {
    return new En(this._tNode, this._rootLView);
  }
  destroy() {
    this.hostView.destroy();
  }
  onDestroy(t) {
    this.hostView.onDestroy(t);
  }
};
function xd(e6, t, n) {
  let r = e6.projection = [];
  for (let o = 0; o < t.length; o++) {
    let i = n[o];
    r.push(i != null && i.length ? Array.from(i) : null);
  }
}
var Mn = class {
};
var Ct = class extends Mn {
  injector;
  componentFactoryResolver = new So(this);
  instance = null;
  constructor(t) {
    super();
    let n = new ge([...t.providers, { provide: Mn, useValue: this }, { provide: xn, useValue: this.componentFactoryResolver }], t.parent || st(), t.debugName, /* @__PURE__ */ new Set(["environment"]));
    this.injector = n, t.runEnvironmentInitializers && n.resolveInjectorInitializers();
  }
  destroy() {
    this.injector.destroy();
  }
  onDestroy(t) {
    this.injector.onDestroy(t);
  }
};
function Ga(e6, t, n = null) {
  return new Ct({ providers: e6, parent: t, debugName: n, runEnvironmentInitializers: true }).injector;
}
var Rd = (() => {
  class e6 {
    _injector;
    cachedInjectors = /* @__PURE__ */ new Map();
    constructor(n) {
      this._injector = n;
    }
    getOrCreateStandaloneInjector(n) {
      if (!n.standalone)
        return null;
      if (!this.cachedInjectors.has(n)) {
        let r = jr(false, n.type), o = r.length > 0 ? Ga([r], this._injector, "") : null;
        this.cachedInjectors.set(n, o);
      }
      return this.cachedInjectors.get(n);
    }
    ngOnDestroy() {
      try {
        for (let n of this.cachedInjectors.values())
          n !== null && n.destroy();
      } finally {
        this.cachedInjectors.clear();
      }
    }
    static \u0275prov = _({ token: e6, providedIn: "environment", factory: () => new e6(E($)) });
  }
  return e6;
})();
function Vo(e6) {
  return bo(() => {
    let t = Ld(e6), n = B(A({}, t), { decls: e6.decls, vars: e6.vars, template: e6.template, consts: e6.consts || null, ngContentSelectors: e6.ngContentSelectors, onPush: e6.changeDetection === xo.OnPush, directiveDefs: null, pipeDefs: null, dependencies: t.standalone && e6.dependencies || null, getStandaloneInjector: t.standalone ? (o) => o.get(Rd).getOrCreateStandaloneInjector(n) : null, getExternalStyles: null, signals: e6.signals ?? false, data: e6.data || {}, encapsulation: e6.encapsulation || z.Emulated, styles: e6.styles || H, _: null, schemas: e6.schemas || null, tView: null, id: "" });
    t.standalone && Ta("NgStandalone"), Pd(n);
    let r = e6.dependencies;
    return n.directiveDefs = zs(r, Od), n.pipeDefs = zs(r, Pi), n.id = jd(n), n;
  });
}
function Od(e6) {
  return ot(e6) || xr(e6);
}
function Rn(e6) {
  return bo(() => ({ type: e6.type, bootstrap: e6.bootstrap || H, declarations: e6.declarations || H, imports: e6.imports || H, exports: e6.exports || H, transitiveCompileScopes: null, schemas: e6.schemas || null, id: e6.id || null }));
}
function kd(e6, t) {
  if (e6 == null)
    return ve;
  let n = {};
  for (let r in e6)
    if (e6.hasOwnProperty(r)) {
      let o = e6[r], i, s, a, c;
      Array.isArray(o) ? (a = o[0], i = o[1], s = o[2] ?? i, c = o[3] || null) : (i = o, s = o, a = Nn.None, c = null), n[i] = [r, a, c], t[i] = s;
    }
  return n;
}
function Fd(e6) {
  if (e6 == null)
    return ve;
  let t = {};
  for (let n in e6)
    e6.hasOwnProperty(n) && (t[e6[n]] = n);
  return t;
}
function Ld(e6) {
  let t = {};
  return { type: e6.type, providersResolver: null, viewProvidersResolver: null, factory: null, hostBindings: e6.hostBindings || null, hostVars: e6.hostVars || 0, hostAttrs: e6.hostAttrs || null, contentQueries: e6.contentQueries || null, declaredInputs: t, inputConfig: e6.inputs || ve, exportAs: e6.exportAs || null, standalone: e6.standalone ?? true, signals: e6.signals === true, selectors: e6.selectors || H, viewQuery: e6.viewQuery || null, features: e6.features || null, setInput: null, resolveHostDirectives: null, hostDirectives: null, controlDef: null, inputs: kd(e6.inputs, t), outputs: Fd(e6.outputs), debugInfo: null };
}
function Pd(e6) {
  e6.features?.forEach((t) => t(e6));
}
function zs(e6, t) {
  return e6 ? () => {
    let n = typeof e6 == "function" ? e6() : e6, r = [];
    for (let o of n) {
      let i = t(o);
      i !== null && r.push(i);
    }
    return r;
  } : null;
}
function jd(e6) {
  let t = 0, n = typeof e6.consts == "function" ? "" : e6.consts, r = [e6.selectors, e6.ngContentSelectors, e6.hostVars, e6.hostAttrs, n, e6.vars, e6.decls, e6.encapsulation, e6.standalone, e6.signals, e6.exportAs, JSON.stringify(e6.inputs), JSON.stringify(e6.outputs), Object.getOwnPropertyNames(e6.type.prototype), !!e6.contentQueries, !!e6.viewQuery];
  for (let i of r.join("|"))
    t = Math.imul(31, t) + i.charCodeAt(0) << 0;
  return t += 2147483648, "c" + t;
}
var Ho = new D("");
function $o(e6) {
  return !!e6 && typeof e6.then == "function";
}
function Wa(e6) {
  return !!e6 && typeof e6.subscribe == "function";
}
var qa = new D("");
var Uo = (() => {
  class e6 {
    resolve;
    reject;
    initialized = false;
    done = false;
    donePromise = new Promise((n, r) => {
      this.resolve = n, this.reject = r;
    });
    appInits = v(qa, { optional: true }) ?? [];
    injector = v(ye);
    constructor() {
    }
    runInitializers() {
      if (this.initialized)
        return;
      let n = [];
      for (let o of this.appInits) {
        let i = nn(this.injector, o);
        if ($o(i))
          n.push(i);
        else if (Wa(i)) {
          let s = new Promise((a, c) => {
            i.subscribe({ complete: a, error: c });
          });
          n.push(s);
        }
      }
      let r = () => {
        this.done = true, this.resolve();
      };
      Promise.all(n).then(() => {
        r();
      }).catch((o) => {
        this.reject(o);
      }), n.length === 0 && r(), this.initialized = true;
    }
    static \u0275fac = function(r) {
      return new (r || e6)();
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac, providedIn: "root" });
  }
  return e6;
})();
var Za = new D("");
function Ya() {
  Jn(() => {
    let e6 = "";
    throw new g(600, e6);
  });
}
function Qa(e6) {
  return e6.isBoundToModule;
}
var Bd = 10;
var On = (() => {
  class e6 {
    _runningTick = false;
    _destroyed = false;
    _destroyListeners = [];
    _views = [];
    internalErrorHandler = v(Ue);
    afterRenderManager = v(Ma);
    zonelessEnabled = v(mt);
    rootEffectScheduler = v(co);
    dirtyFlags = 0;
    tracingSnapshot = null;
    allTestViews = /* @__PURE__ */ new Set();
    autoDetectTestViews = /* @__PURE__ */ new Set();
    includeAllTestViews = false;
    afterTick = new oe();
    get allViews() {
      return [...(this.includeAllTestViews ? this.allTestViews : this.autoDetectTestViews).keys(), ...this._views];
    }
    get destroyed() {
      return this._destroyed;
    }
    componentTypes = [];
    components = [];
    internalPendingTask = v($e);
    get isStable() {
      return this.internalPendingTask.hasPendingTasksObservable.pipe(cr((n) => !n));
    }
    constructor() {
      v(Ze, { optional: true });
    }
    whenStable() {
      let n;
      return new Promise((r) => {
        n = this.isStable.subscribe({ next: (o) => {
          o && r();
        } });
      }).finally(() => {
        n.unsubscribe();
      });
    }
    _injector = v($);
    _rendererFactory = null;
    get injector() {
      return this._injector;
    }
    bootstrap(n, r) {
      return this.bootstrapImpl(n, r);
    }
    bootstrapImpl(n, r, o = ye.NULL) {
      return this._injector.get(L).run(() => {
        M(I.BootstrapComponentStart);
        let s = n instanceof An;
        if (!this._injector.get(Uo).done) {
          let T = "";
          throw new g(405, T);
        }
        let c;
        s ? c = n : c = this._injector.get(xn).resolveComponentFactory(n), this.componentTypes.push(c.componentType);
        let u = Qa(c) ? void 0 : this._injector.get(Mn), l = r || c.selector, d = c.create(o, [], l, u), p = d.location.nativeElement, f = d.injector.get(Ho, null);
        return f?.registerApplication(p), d.onDestroy(() => {
          this.detachView(d.hostView), Dt(this.components, d), f?.unregisterApplication(p);
        }), this._loadComponent(d), M(I.BootstrapComponentEnd, d), d;
      });
    }
    tick() {
      this.zonelessEnabled || (this.dirtyFlags |= 1), this._tick();
    }
    _tick() {
      M(I.ChangeDetectionStart), this.tracingSnapshot !== null ? this.tracingSnapshot.run(Fo.CHANGE_DETECTION, this.tickImpl) : this.tickImpl();
    }
    tickImpl = () => {
      if (this._runningTick)
        throw M(I.ChangeDetectionEnd), new g(101, false);
      let n = y(null);
      try {
        this._runningTick = true, this.synchronize();
      } finally {
        this._runningTick = false, this.tracingSnapshot?.dispose(), this.tracingSnapshot = null, y(n), this.afterTick.next(), M(I.ChangeDetectionEnd);
      }
    };
    synchronize() {
      this._rendererFactory === null && !this._injector.destroyed && (this._rendererFactory = this._injector.get(we, null, { optional: true }));
      let n = 0;
      for (; this.dirtyFlags !== 0 && n++ < Bd; ) {
        M(I.ChangeDetectionSyncStart);
        try {
          this.synchronizeOnce();
        } finally {
          M(I.ChangeDetectionSyncEnd);
        }
      }
    }
    synchronizeOnce() {
      this.dirtyFlags & 16 && (this.dirtyFlags &= -17, this.rootEffectScheduler.flush());
      let n = false;
      if (this.dirtyFlags & 7) {
        let r = !!(this.dirtyFlags & 1);
        this.dirtyFlags &= -8, this.dirtyFlags |= 8;
        for (let { _lView: o } of this.allViews) {
          if (!r && !ft(o))
            continue;
          let i = r && !this.zonelessEnabled ? 0 : 1;
          La(o, i), n = true;
        }
        if (this.dirtyFlags &= -5, this.syncDirtyFlagsWithViews(), this.dirtyFlags & 23)
          return;
      }
      n || (this._rendererFactory?.begin?.(), this._rendererFactory?.end?.()), this.dirtyFlags & 8 && (this.dirtyFlags &= -9, this.afterRenderManager.execute()), this.syncDirtyFlagsWithViews();
    }
    syncDirtyFlagsWithViews() {
      if (this.allViews.some(({ _lView: n }) => ft(n))) {
        this.dirtyFlags |= 2;
        return;
      } else
        this.dirtyFlags &= -8;
    }
    attachView(n) {
      let r = n;
      this._views.push(r), r.attachToAppRef(this);
    }
    detachView(n) {
      let r = n;
      Dt(this._views, r), r.detachFromAppRef();
    }
    _loadComponent(n) {
      this.attachView(n.hostView);
      try {
        this.tick();
      } catch (o) {
        this.internalErrorHandler(o);
      }
      this.components.push(n), this._injector.get(Za, []).forEach((o) => o(n));
    }
    ngOnDestroy() {
      if (!this._destroyed)
        try {
          this._destroyListeners.forEach((n) => n()), this._views.slice().forEach((n) => n.destroy());
        } finally {
          this._destroyed = true, this._views = [], this._destroyListeners = [];
        }
    }
    onDestroy(n) {
      return this._destroyListeners.push(n), () => Dt(this._destroyListeners, n);
    }
    destroy() {
      if (this._destroyed)
        throw new g(406, false);
      let n = this._injector;
      n.destroy && !n.destroyed && n.destroy();
    }
    get viewCount() {
      return this._views.length;
    }
    static \u0275fac = function(r) {
      return new (r || e6)();
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac, providedIn: "root" });
  }
  return e6;
})();
function Dt(e6, t) {
  let n = e6.indexOf(t);
  n > -1 && e6.splice(n, 1);
}
function Ye(e6, t, n, r) {
  let o = Y(), i = o[m], s = e6 + U, a = i.firstCreatePass ? Id(s, i, 2, t, n, r) : i.data[s];
  return Vl(a, o, e6, t, Vd), r != null && Rl(o, a), Ye;
}
function Qe() {
  let e6 = He(), t = Hl(e6);
  return ss(t) && as(), os(), Qe;
}
var Vd = (e6, t, n, r, o) => (no(true), ga(t[P], r, Ds()));
var Mt = "en-US";
var Hd = Mt;
function Ka(e6) {
  typeof e6 == "string" && (Hd = e6.toLowerCase().replace(/_/g, "-"));
}
function _t(e6, t = "") {
  let n = Y(), r = qr(), o = e6 + U, i = r.firstCreatePass ? Bo(r, o, 1, t, null) : r.data[o], s = $d(r, n, i, t);
  n[o] = s, to() && ba(r, n, s, i), ht(i, false);
}
var $d = (e6, t, n, r) => (no(true), Ju(t[P], r));
function Ud(e6, t, n, r = "") {
  return Cd(e6, ds(), n) ? t + ji(n) + r : qe;
}
function kn(e6, t, n) {
  let r = Y(), o = Ud(r, e6, t, n);
  return o !== qe && zd(r, hn(), o), kn;
}
function zd(e6, t, n) {
  let r = Xi(t, e6);
  Xu(e6[P], r, n);
}
var Ja = (() => {
  class e6 {
    applicationErrorHandler = v(Ue);
    appRef = v(On);
    taskService = v($e);
    ngZone = v(L);
    zonelessEnabled = v(mt);
    tracing = v(Ze, { optional: true });
    zoneIsDefined = typeof Zone < "u" && !!Zone.root.run;
    schedulerTickApplyArgs = [{ data: { __scheduler_tick__: true } }];
    subscriptions = new b();
    angularZoneId = this.zoneIsDefined ? this.ngZone._inner?.get(tt) : null;
    scheduleInRootZone = !this.zonelessEnabled && this.zoneIsDefined && (v(ao, { optional: true }) ?? false);
    cancelScheduledCallback = null;
    useMicrotaskScheduler = false;
    runningTick = false;
    pendingRenderTaskId = null;
    constructor() {
      this.subscriptions.add(this.appRef.afterTick.subscribe(() => {
        let n = this.taskService.add();
        if (!this.runningTick && (this.cleanup(), !this.zonelessEnabled || this.appRef.includeAllTestViews)) {
          this.taskService.remove(n);
          return;
        }
        this.switchToMicrotaskScheduler(), this.taskService.remove(n);
      })), this.subscriptions.add(this.ngZone.onUnstable.subscribe(() => {
        this.runningTick || this.cleanup();
      }));
    }
    switchToMicrotaskScheduler() {
      this.ngZone.runOutsideAngular(() => {
        let n = this.taskService.add();
        this.useMicrotaskScheduler = true, queueMicrotask(() => {
          this.useMicrotaskScheduler = false, this.taskService.remove(n);
        });
      });
    }
    notify(n) {
      if (!this.zonelessEnabled && n === 5)
        return;
      switch (n) {
        case 0: {
          this.appRef.dirtyFlags |= 2;
          break;
        }
        case 3:
        case 2:
        case 4:
        case 5:
        case 1: {
          this.appRef.dirtyFlags |= 4;
          break;
        }
        case 6: {
          this.appRef.dirtyFlags |= 2;
          break;
        }
        case 12: {
          this.appRef.dirtyFlags |= 16;
          break;
        }
        case 13: {
          this.appRef.dirtyFlags |= 2;
          break;
        }
        case 11:
          break;
        default:
          this.appRef.dirtyFlags |= 8;
      }
      if (this.appRef.tracingSnapshot = this.tracing?.snapshot(this.appRef.tracingSnapshot) ?? null, !this.shouldScheduleTick())
        return;
      let r = this.useMicrotaskScheduler ? ws : ro;
      this.pendingRenderTaskId = this.taskService.add(), this.scheduleInRootZone ? this.cancelScheduledCallback = Zone.root.run(() => r(() => this.tick())) : this.cancelScheduledCallback = this.ngZone.runOutsideAngular(() => r(() => this.tick()));
    }
    shouldScheduleTick() {
      return !(this.appRef.destroyed || this.pendingRenderTaskId !== null || this.runningTick || this.appRef._runningTick || !this.zonelessEnabled && this.zoneIsDefined && Zone.current.get(tt + this.angularZoneId));
    }
    tick() {
      if (this.runningTick || this.appRef.destroyed)
        return;
      if (this.appRef.dirtyFlags === 0) {
        this.cleanup();
        return;
      }
      !this.zonelessEnabled && this.appRef.dirtyFlags & 7 && (this.appRef.dirtyFlags |= 1);
      let n = this.taskService.add();
      try {
        this.ngZone.run(() => {
          this.runningTick = true, this.appRef._tick();
        }, void 0, this.schedulerTickApplyArgs);
      } catch (r) {
        this.applicationErrorHandler(r);
      } finally {
        this.taskService.remove(n), this.cleanup();
      }
    }
    ngOnDestroy() {
      this.subscriptions.unsubscribe(), this.cleanup();
    }
    cleanup() {
      if (this.runningTick = false, this.cancelScheduledCallback?.(), this.cancelScheduledCallback = null, this.pendingRenderTaskId !== null) {
        let n = this.pendingRenderTaskId;
        this.pendingRenderTaskId = null, this.taskService.remove(n);
      }
    }
    static \u0275fac = function(r) {
      return new (r || e6)();
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac, providedIn: "root" });
  }
  return e6;
})();
function Xa() {
  return [{ provide: Oe, useExisting: Ja }, { provide: L, useClass: nt }, { provide: mt, useValue: true }];
}
function Gd() {
  return typeof $localize < "u" && $localize.locale || Mt;
}
var zo = new D("", { factory: () => v(zo, { optional: true, skipSelf: true }) || Gd() });
var Go = new D("");
var of = new D("");
function St(e6) {
  return !e6.moduleRef;
}
function sf(e6) {
  let t = St(e6) ? e6.r3Injector : e6.moduleRef.injector, n = t.get(L);
  return n.run(() => {
    St(e6) ? e6.r3Injector.resolveInjectorInitializers() : e6.moduleRef.resolveInjectorInitializers();
    let r = t.get(Ue), o;
    if (n.runOutsideAngular(() => {
      o = n.onError.subscribe({ next: r });
    }), St(e6)) {
      let i = () => t.destroy(), s = e6.platformInjector.get(Go);
      s.add(i), t.onDestroy(() => {
        o.unsubscribe(), s.delete(i);
      });
    } else {
      let i = () => e6.moduleRef.destroy(), s = e6.platformInjector.get(Go);
      s.add(i), e6.moduleRef.onDestroy(() => {
        Dt(e6.allPlatformModules, e6.moduleRef), o.unsubscribe(), s.delete(i);
      });
    }
    return cf(r, n, () => {
      let i = t.get($e), s = i.add(), a = t.get(Uo);
      return a.runInitializers(), a.donePromise.then(() => {
        let c = t.get(zo, Mt);
        if (Ka(c || Mt), !t.get(of, true))
          return St(e6) ? t.get(On) : (e6.allPlatformModules.push(e6.moduleRef), e6.moduleRef);
        if (St(e6)) {
          let l = t.get(On);
          return e6.rootComponent !== void 0 && l.bootstrap(e6.rootComponent), l;
        } else
          return af?.(e6.moduleRef, e6.allPlatformModules), e6.moduleRef;
      }).finally(() => {
        i.remove(s);
      });
    });
  });
}
var af;
function cf(e6, t, n) {
  try {
    let r = n();
    return $o(r) ? r.catch((o) => {
      throw t.runOutsideAngular(() => e6(o)), o;
    }) : r;
  } catch (r) {
    throw t.runOutsideAngular(() => e6(r)), r;
  }
}
var Fn = null;
function uf(e6 = [], t) {
  return ye.create({ name: t, providers: [{ provide: it, useValue: "platform" }, { provide: Go, useValue: /* @__PURE__ */ new Set([() => Fn = null]) }, ...e6] });
}
function lf(e6 = []) {
  if (Fn)
    return Fn;
  let t = uf(e6);
  return Fn = t, Ya(), df(t), t;
}
function df(e6) {
  let t = e6.get(Sn, null);
  nn(e6, () => {
    t?.forEach((n) => n());
  });
}
var ff = 1e4;
var Iw = ff - 1e3;
function ec(e6) {
  let { rootComponent: t, appProviders: n, platformProviders: r, platformRef: o } = e6;
  M(I.BootstrapApplicationStart);
  try {
    let i = o?.injector ?? lf(r), s = [Xa(), Ms, ...n || []], a = new Ct({ providers: s, parent: i, debugName: "", runEnvironmentInitializers: false });
    return sf({ r3Injector: a.injector, platformInjector: i, rootComponent: t });
  } catch (i) {
    return Promise.reject(i);
  } finally {
    M(I.BootstrapApplicationEnd);
  }
}
var tc = null;
function Nt() {
  return tc;
}
function Wo(e6) {
  tc ??= e6;
}
var bt = class {
};
var Pn = (() => {
  class e6 {
    static \u0275fac = function(r) {
      return new (r || e6)();
    };
    static \u0275mod = Rn({ type: e6 });
    static \u0275inj = rt({});
  }
  return e6;
})();
function qo(e6, t) {
  t = encodeURIComponent(t);
  for (let n of e6.split(";")) {
    let r = n.indexOf("="), [o, i] = r == -1 ? [n, ""] : [n.slice(0, r), n.slice(r + 1)];
    if (o.trim() === t)
      return decodeURIComponent(i);
  }
  return null;
}
var At = class {
};
var nc = "browser";
var xt = class {
  _doc;
  constructor(t) {
    this._doc = t;
  }
  manager;
};
var jn = (() => {
  class e6 extends xt {
    constructor(n) {
      super(n);
    }
    supports(n) {
      return true;
    }
    addEventListener(n, r, o, i) {
      return n.addEventListener(r, o, i), () => this.removeEventListener(n, r, o, i);
    }
    removeEventListener(n, r, o, i) {
      return n.removeEventListener(r, o, i);
    }
    static \u0275fac = function(r) {
      return new (r || e6)(E(j));
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var Hn = new D("");
var Ko = (() => {
  class e6 {
    _zone;
    _plugins;
    _eventNameToPlugin = /* @__PURE__ */ new Map();
    constructor(n, r) {
      this._zone = r, n.forEach((s) => {
        s.manager = this;
      });
      let o = n.filter((s) => !(s instanceof jn));
      this._plugins = o.slice().reverse();
      let i = n.find((s) => s instanceof jn);
      i && this._plugins.push(i);
    }
    addEventListener(n, r, o, i) {
      return this._findPluginFor(r).addEventListener(n, r, o, i);
    }
    getZone() {
      return this._zone;
    }
    _findPluginFor(n) {
      let r = this._eventNameToPlugin.get(n);
      if (r)
        return r;
      if (r = this._plugins.find((i) => i.supports(n)), !r)
        throw new g(5101, false);
      return this._eventNameToPlugin.set(n, r), r;
    }
    static \u0275fac = function(r) {
      return new (r || e6)(E(Hn), E(L));
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var Zo = "ng-app-id";
function rc(e6) {
  for (let t of e6)
    t.remove();
}
function oc(e6, t) {
  let n = t.createElement("style");
  return n.textContent = e6, n;
}
function hf(e6, t, n, r) {
  let o = e6.head?.querySelectorAll(`style[${Zo}="${t}"],link[${Zo}="${t}"]`);
  if (o)
    for (let i of o)
      i.removeAttribute(Zo), i instanceof HTMLLinkElement ? r.set(i.href.slice(i.href.lastIndexOf("/") + 1), { usage: 0, elements: [i] }) : i.textContent && n.set(i.textContent, { usage: 0, elements: [i] });
}
function Qo(e6, t) {
  let n = t.createElement("link");
  return n.setAttribute("rel", "stylesheet"), n.setAttribute("href", e6), n;
}
var Jo = (() => {
  class e6 {
    doc;
    appId;
    nonce;
    inline = /* @__PURE__ */ new Map();
    external = /* @__PURE__ */ new Map();
    hosts = /* @__PURE__ */ new Set();
    constructor(n, r, o, i = {}) {
      this.doc = n, this.appId = r, this.nonce = o, hf(n, r, this.inline, this.external), this.hosts.add(n.head);
    }
    addStyles(n, r) {
      for (let o of n)
        this.addUsage(o, this.inline, oc);
      r?.forEach((o) => this.addUsage(o, this.external, Qo));
    }
    removeStyles(n, r) {
      for (let o of n)
        this.removeUsage(o, this.inline);
      r?.forEach((o) => this.removeUsage(o, this.external));
    }
    addUsage(n, r, o) {
      let i = r.get(n);
      i ? i.usage++ : r.set(n, { usage: 1, elements: [...this.hosts].map((s) => this.addElement(s, o(n, this.doc))) });
    }
    removeUsage(n, r) {
      let o = r.get(n);
      o && (o.usage--, o.usage <= 0 && (rc(o.elements), r.delete(n)));
    }
    ngOnDestroy() {
      for (let [, { elements: n }] of [...this.inline, ...this.external])
        rc(n);
      this.hosts.clear();
    }
    addHost(n) {
      this.hosts.add(n);
      for (let [r, { elements: o }] of this.inline)
        o.push(this.addElement(n, oc(r, this.doc)));
      for (let [r, { elements: o }] of this.external)
        o.push(this.addElement(n, Qo(r, this.doc)));
    }
    removeHost(n) {
      this.hosts.delete(n);
    }
    addElement(n, r) {
      return this.nonce && r.setAttribute("nonce", this.nonce), n.appendChild(r);
    }
    static \u0275fac = function(r) {
      return new (r || e6)(E(j), E(_n), E(bn, 8), E(wt));
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var Yo = { svg: "http://www.w3.org/2000/svg", xhtml: "http://www.w3.org/1999/xhtml", xlink: "http://www.w3.org/1999/xlink", xml: "http://www.w3.org/XML/1998/namespace", xmlns: "http://www.w3.org/2000/xmlns/", math: "http://www.w3.org/1998/Math/MathML" };
var Xo = /%COMP%/g;
var sc = "%COMP%";
var gf = `_nghost-${sc}`;
var mf = `_ngcontent-${sc}`;
var yf = true;
var Df = new D("", { factory: () => yf });
function vf(e6) {
  return mf.replace(Xo, e6);
}
function Ef(e6) {
  return gf.replace(Xo, e6);
}
function ac(e6, t) {
  return t.map((n) => n.replace(Xo, e6));
}
var ei = (() => {
  class e6 {
    eventManager;
    sharedStylesHost;
    appId;
    removeStylesOnCompDestroy;
    doc;
    ngZone;
    nonce;
    tracingService;
    rendererByCompId = /* @__PURE__ */ new Map();
    defaultRenderer;
    constructor(n, r, o, i, s, a, c = null, u = null) {
      this.eventManager = n, this.sharedStylesHost = r, this.appId = o, this.removeStylesOnCompDestroy = i, this.doc = s, this.ngZone = a, this.nonce = c, this.tracingService = u, this.defaultRenderer = new Rt(n, s, a, this.tracingService);
    }
    createRenderer(n, r) {
      if (!n || !r)
        return this.defaultRenderer;
      let o = this.getOrCreateRenderer(n, r);
      return o instanceof Vn ? o.applyToHost(n) : o instanceof Ot && o.applyStyles(), o;
    }
    getOrCreateRenderer(n, r) {
      let o = this.rendererByCompId, i = o.get(r.id);
      if (!i) {
        let s = this.doc, a = this.ngZone, c = this.eventManager, u = this.sharedStylesHost, l = this.removeStylesOnCompDestroy, d = this.tracingService;
        switch (r.encapsulation) {
          case z.Emulated:
            i = new Vn(c, u, r, this.appId, l, s, a, d);
            break;
          case z.ShadowDom:
            return new Bn(c, n, r, s, a, this.nonce, d, u);
          case z.ExperimentalIsolatedShadowDom:
            return new Bn(c, n, r, s, a, this.nonce, d);
          default:
            i = new Ot(c, u, r, l, s, a, d);
            break;
        }
        o.set(r.id, i);
      }
      return i;
    }
    ngOnDestroy() {
      this.rendererByCompId.clear();
    }
    componentReplaced(n) {
      this.rendererByCompId.delete(n);
    }
    static \u0275fac = function(r) {
      return new (r || e6)(E(Ko), E(Jo), E(_n), E(Df), E(j), E(L), E(bn), E(Ze, 8));
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var Rt = class {
  eventManager;
  doc;
  ngZone;
  tracingService;
  data = /* @__PURE__ */ Object.create(null);
  throwOnSyntheticProps = true;
  constructor(t, n, r, o) {
    this.eventManager = t, this.doc = n, this.ngZone = r, this.tracingService = o;
  }
  destroy() {
  }
  destroyNode = null;
  createElement(t, n) {
    return n ? this.doc.createElementNS(Yo[n] || n, t) : this.doc.createElement(t);
  }
  createComment(t) {
    return this.doc.createComment(t);
  }
  createText(t) {
    return this.doc.createTextNode(t);
  }
  appendChild(t, n) {
    (ic(t) ? t.content : t).appendChild(n);
  }
  insertBefore(t, n, r) {
    t && (ic(t) ? t.content : t).insertBefore(n, r);
  }
  removeChild(t, n) {
    n.remove();
  }
  selectRootElement(t, n) {
    let r = typeof t == "string" ? this.doc.querySelector(t) : t;
    if (!r)
      throw new g(-5104, false);
    return n || (r.textContent = ""), r;
  }
  parentNode(t) {
    return t.parentNode;
  }
  nextSibling(t) {
    return t.nextSibling;
  }
  setAttribute(t, n, r, o) {
    if (o) {
      n = o + ":" + n;
      let i = Yo[o];
      i ? t.setAttributeNS(i, n, r) : t.setAttribute(n, r);
    } else
      t.setAttribute(n, r);
  }
  removeAttribute(t, n, r) {
    if (r) {
      let o = Yo[r];
      o ? t.removeAttributeNS(o, n) : t.removeAttribute(`${r}:${n}`);
    } else
      t.removeAttribute(n);
  }
  addClass(t, n) {
    t.classList.add(n);
  }
  removeClass(t, n) {
    t.classList.remove(n);
  }
  setStyle(t, n, r, o) {
    o & (Te.DashCase | Te.Important) ? t.style.setProperty(n, r, o & Te.Important ? "important" : "") : t.style[n] = r;
  }
  removeStyle(t, n, r) {
    r & Te.DashCase ? t.style.removeProperty(n) : t.style[n] = "";
  }
  setProperty(t, n, r) {
    t != null && (t[n] = r);
  }
  setValue(t, n) {
    t.nodeValue = n;
  }
  listen(t, n, r, o) {
    if (typeof t == "string" && (t = Nt().getGlobalEventTarget(this.doc, t), !t))
      throw new g(5102, false);
    let i = this.decoratePreventDefault(r);
    return this.tracingService?.wrapEventListener && (i = this.tracingService.wrapEventListener(t, n, i)), this.eventManager.addEventListener(t, n, i, o);
  }
  decoratePreventDefault(t) {
    return (n) => {
      if (n === "__ngUnwrap__")
        return t;
      t(n) === false && n.preventDefault();
    };
  }
};
function ic(e6) {
  return e6.tagName === "TEMPLATE" && e6.content !== void 0;
}
var Bn = class extends Rt {
  hostEl;
  sharedStylesHost;
  shadowRoot;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, o, i, a), this.hostEl = n, this.sharedStylesHost = c, this.shadowRoot = n.attachShadow({ mode: "open" }), this.sharedStylesHost && this.sharedStylesHost.addHost(this.shadowRoot);
    let u = r.styles;
    u = ac(r.id, u);
    for (let d of u) {
      let p = document.createElement("style");
      s && p.setAttribute("nonce", s), p.textContent = d, this.shadowRoot.appendChild(p);
    }
    let l = r.getExternalStyles?.();
    if (l)
      for (let d of l) {
        let p = Qo(d, o);
        s && p.setAttribute("nonce", s), this.shadowRoot.appendChild(p);
      }
  }
  nodeOrShadowRoot(t) {
    return t === this.hostEl ? this.shadowRoot : t;
  }
  appendChild(t, n) {
    return super.appendChild(this.nodeOrShadowRoot(t), n);
  }
  insertBefore(t, n, r) {
    return super.insertBefore(this.nodeOrShadowRoot(t), n, r);
  }
  removeChild(t, n) {
    return super.removeChild(null, n);
  }
  parentNode(t) {
    return this.nodeOrShadowRoot(super.parentNode(this.nodeOrShadowRoot(t)));
  }
  destroy() {
    this.sharedStylesHost && this.sharedStylesHost.removeHost(this.shadowRoot);
  }
};
var Ot = class extends Rt {
  sharedStylesHost;
  removeStylesOnCompDestroy;
  styles;
  styleUrls;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, i, s, a), this.sharedStylesHost = n, this.removeStylesOnCompDestroy = o;
    let u = r.styles;
    this.styles = c ? ac(c, u) : u, this.styleUrls = r.getExternalStyles?.(c);
  }
  applyStyles() {
    this.sharedStylesHost.addStyles(this.styles, this.styleUrls);
  }
  destroy() {
    this.removeStylesOnCompDestroy && We.size === 0 && this.sharedStylesHost.removeStyles(this.styles, this.styleUrls);
  }
};
var Vn = class extends Ot {
  contentAttr;
  hostAttr;
  constructor(t, n, r, o, i, s, a, c) {
    let u = o + "-" + r.id;
    super(t, n, r, i, s, a, c, u), this.contentAttr = vf(u), this.hostAttr = Ef(u);
  }
  applyToHost(t) {
    this.applyStyles(), this.setAttribute(t, this.hostAttr, "");
  }
  createElement(t, n) {
    let r = super.createElement(t, n);
    return super.setAttribute(r, this.contentAttr, ""), r;
  }
};
var $n = class e4 extends bt {
  supportsDOMEvents = true;
  static makeCurrent() {
    Wo(new e4());
  }
  onAndCancel(t, n, r, o) {
    return t.addEventListener(n, r, o), () => {
      t.removeEventListener(n, r, o);
    };
  }
  dispatchEvent(t, n) {
    t.dispatchEvent(n);
  }
  remove(t) {
    t.remove();
  }
  createElement(t, n) {
    return n = n || this.getDefaultDocument(), n.createElement(t);
  }
  createHtmlDocument() {
    return document.implementation.createHTMLDocument("fakeTitle");
  }
  getDefaultDocument() {
    return document;
  }
  isElementNode(t) {
    return t.nodeType === Node.ELEMENT_NODE;
  }
  isShadowRoot(t) {
    return t instanceof DocumentFragment;
  }
  getGlobalEventTarget(t, n) {
    return n === "window" ? window : n === "document" ? t : n === "body" ? t.body : null;
  }
  getBaseHref(t) {
    let n = If();
    return n == null ? null : Cf(n);
  }
  resetBaseElement() {
    kt = null;
  }
  getUserAgent() {
    return window.navigator.userAgent;
  }
  getCookie(t) {
    return qo(document.cookie, t);
  }
};
var kt = null;
function If() {
  return kt = kt || document.head.querySelector("base"), kt ? kt.getAttribute("href") : null;
}
function Cf(e6) {
  return new URL(e6, document.baseURI).pathname;
}
var wf = (() => {
  class e6 {
    build() {
      return new XMLHttpRequest();
    }
    static \u0275fac = function(r) {
      return new (r || e6)();
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var cc = ["alt", "control", "meta", "shift"];
var Tf = { "\b": "Backspace", "	": "Tab", "\x7F": "Delete", "\x1B": "Escape", Del: "Delete", Esc: "Escape", Left: "ArrowLeft", Right: "ArrowRight", Up: "ArrowUp", Down: "ArrowDown", Menu: "ContextMenu", Scroll: "ScrollLock", Win: "OS" };
var Mf = { alt: (e6) => e6.altKey, control: (e6) => e6.ctrlKey, meta: (e6) => e6.metaKey, shift: (e6) => e6.shiftKey };
var uc = (() => {
  class e6 extends xt {
    constructor(n) {
      super(n);
    }
    supports(n) {
      return e6.parseEventName(n) != null;
    }
    addEventListener(n, r, o, i) {
      let s = e6.parseEventName(r), a = e6.eventCallback(s.fullKey, o, this.manager.getZone());
      return this.manager.getZone().runOutsideAngular(() => Nt().onAndCancel(n, s.domEventName, a, i));
    }
    static parseEventName(n) {
      let r = n.toLowerCase().split("."), o = r.shift();
      if (r.length === 0 || !(o === "keydown" || o === "keyup"))
        return null;
      let i = e6._normalizeKey(r.pop()), s = "", a = r.indexOf("code");
      if (a > -1 && (r.splice(a, 1), s = "code."), cc.forEach((u) => {
        let l = r.indexOf(u);
        l > -1 && (r.splice(l, 1), s += u + ".");
      }), s += i, r.length != 0 || i.length === 0)
        return null;
      let c = {};
      return c.domEventName = o, c.fullKey = s, c;
    }
    static matchEventFullKeyCode(n, r) {
      let o = Tf[n.key] || n.key, i = "";
      return r.indexOf("code.") > -1 && (o = n.code, i = "code."), o == null || !o ? false : (o = o.toLowerCase(), o === " " ? o = "space" : o === "." && (o = "dot"), cc.forEach((s) => {
        if (s !== o) {
          let a = Mf[s];
          a(n) && (i += s + ".");
        }
      }), i += o, i === r);
    }
    static eventCallback(n, r, o) {
      return (i) => {
        e6.matchEventFullKeyCode(i, n) && o.runGuarded(() => r(i));
      };
    }
    static _normalizeKey(n) {
      return n === "esc" ? "escape" : n;
    }
    static \u0275fac = function(r) {
      return new (r || e6)(E(j));
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
async function ti(e6, t, n) {
  let r = A({ rootComponent: e6 }, _f(t, n));
  return ec(r);
}
function _f(e6, t) {
  return { platformRef: t?.platformRef, appProviders: [...xf, ...e6?.providers ?? []], platformProviders: Af };
}
function Sf() {
  $n.makeCurrent();
}
function bf() {
  return new X();
}
function Nf() {
  return Ro(document), document;
}
var Af = [{ provide: wt, useValue: nc }, { provide: Sn, useValue: Sf, multi: true }, { provide: j, useFactory: Nf }];
var xf = [{ provide: it, useValue: "root" }, { provide: X, useFactory: bf }, { provide: Hn, useClass: jn, multi: true }, { provide: Hn, useClass: uc, multi: true }, ei, Jo, Ko, { provide: we, useExisting: ei }, { provide: At, useClass: wf }, []];
var Un = class e5 {
  constructor(t) {
    this.model = t;
    t && (this.message.set(t.get("message") || "Model loaded, no message."), t.on("change:message", () => {
      this.message.set(t.get("message"));
    }));
  }
  message = gn("Waiting for model...");
  static \u0275fac = function(n) {
    return new (n || e5)(Tt("ANYWIDGET_MODEL"));
  };
  static \u0275cmp = Vo({ type: e5, selectors: [["app-root"]], decls: 7, vars: 1, consts: [[1, "angular-widget"]], template: function(n, r) {
    n & 1 && (Ye(0, "div", 0)(1, "h3"), _t(2, "Angular Hybrid Widget"), Qe(), Ye(3, "p"), _t(4, "Status: Infrastructure Loaded"), Qe(), Ye(5, "p"), _t(6), Qe()()), n & 2 && (ko(6), kn("Message from Python: ", r.message()));
  }, dependencies: [Pn], styles: [".angular-widget[_ngcontent-%COMP%]{padding:10px;border:1px solid #ccc;border-radius:4px;background-color:#f9f9f9}"] });
};
function Rf({ model: e6, el: t }) {
  let n = document.createElement("app-root");
  t.appendChild(n);
  let r = { providers: [so(), { provide: "ANYWIDGET_MODEL", useValue: e6 }] };
  ti(Un, r).catch((o) => console.error(o));
}
var NM = { render: Rf };
export {
  NM as default
};
