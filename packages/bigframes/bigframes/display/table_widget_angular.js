// dist/table-widget-angular/browser/main.js
var nu = Object.defineProperty;
var ru = Object.defineProperties;
var ou = Object.getOwnPropertyDescriptors;
var Pi = Object.getOwnPropertySymbols;
var iu = Object.prototype.hasOwnProperty;
var su = Object.prototype.propertyIsEnumerable;
var ji = (e6, t, n) => t in e6 ? nu(e6, t, { enumerable: true, configurable: true, writable: true, value: n }) : e6[t] = n;
var x = (e6, t) => {
  for (var n in t ||= {})
    iu.call(t, n) && ji(e6, n, t[n]);
  if (Pi)
    for (var n of Pi(t))
      su.call(t, n) && ji(e6, n, t[n]);
  return e6;
};
var V = (e6, t) => ru(e6, ou(t));
var S = null;
var qt = false;
var dr = 1;
var au = null;
var W = Symbol("SIGNAL");
function D(e6) {
  let t = S;
  return S = e6, t;
}
function Zt() {
  return S;
}
var Yt = { version: 0, lastCleanEpoch: 0, dirty: false, producers: void 0, producersTail: void 0, consumers: void 0, consumersTail: void 0, recomputing: false, consumerAllowSignalWrites: false, consumerIsAlwaysLive: false, kind: "unknown", producerMustRecompute: () => false, producerRecomputeValue: () => {
}, consumerMarkedDirty: () => {
}, consumerOnSignalRead: () => {
} };
function Bi(e6) {
  if (qt)
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
  if (o !== void 0 && o.consumer === S && (!r || uu(o, S)))
    return;
  let i = Fe(S), s = { producer: e6, consumer: S, nextProducer: n, prevConsumer: o, lastReadVersion: e6.version, nextConsumer: void 0 };
  S.producersTail = s, t !== void 0 ? t.nextProducer = s : S.producers = s, i && Gi(e6, s);
}
function Vi() {
  dr++;
}
function Hi(e6) {
  if (!(Fe(e6) && !e6.dirty) && !(!e6.dirty && e6.lastCleanEpoch === dr)) {
    if (!e6.producerMustRecompute(e6) && !gr(e6)) {
      lr(e6);
      return;
    }
    e6.producerRecomputeValue(e6), lr(e6);
  }
}
function fr(e6) {
  if (e6.consumers === void 0)
    return;
  let t = qt;
  qt = true;
  try {
    for (let n = e6.consumers; n !== void 0; n = n.nextConsumer) {
      let r = n.consumer;
      r.dirty || cu(r);
    }
  } finally {
    qt = t;
  }
}
function pr() {
  return S?.consumerAllowSignalWrites !== false;
}
function cu(e6) {
  e6.dirty = true, fr(e6), e6.consumerMarkedDirty?.(e6);
}
function lr(e6) {
  e6.dirty = false, e6.lastCleanEpoch = dr;
}
function hr(e6) {
  return e6 && $i(e6), D(e6);
}
function $i(e6) {
  e6.producersTail = void 0, e6.recomputing = true;
}
function Ui(e6, t) {
  D(t), e6 && zi(e6);
}
function zi(e6) {
  e6.recomputing = false;
  let t = e6.producersTail, n = t !== void 0 ? t.nextProducer : e6.producers;
  if (n !== void 0) {
    if (Fe(e6))
      do
        n = mr(n);
      while (n !== void 0);
    t !== void 0 ? t.nextProducer = void 0 : e6.producers = void 0;
  }
}
function gr(e6) {
  for (let t = e6.producers; t !== void 0; t = t.nextProducer) {
    let n = t.producer, r = t.lastReadVersion;
    if (r !== n.version || (Hi(n), r !== n.version))
      return true;
  }
  return false;
}
function Qt(e6) {
  if (Fe(e6)) {
    let t = e6.producers;
    for (; t !== void 0; )
      t = mr(t);
  }
  e6.producers = void 0, e6.producersTail = void 0, e6.consumers = void 0, e6.consumersTail = void 0;
}
function Gi(e6, t) {
  let n = e6.consumersTail, r = Fe(e6);
  if (n !== void 0 ? (t.nextConsumer = n.nextConsumer, n.nextConsumer = t) : (t.nextConsumer = void 0, e6.consumers = t), t.prevConsumer = n, e6.consumersTail = t, !r)
    for (let o = e6.producers; o !== void 0; o = o.nextProducer)
      Gi(o.producer, o);
}
function mr(e6) {
  let t = e6.producer, n = e6.nextProducer, r = e6.nextConsumer, o = e6.prevConsumer;
  if (e6.nextConsumer = void 0, e6.prevConsumer = void 0, r !== void 0 ? r.prevConsumer = o : t.consumersTail = o, o !== void 0)
    o.nextConsumer = r;
  else if (t.consumers = r, !Fe(t)) {
    let i = t.producers;
    for (; i !== void 0; )
      i = mr(i);
  }
  return n;
}
function Fe(e6) {
  return e6.consumerIsAlwaysLive || e6.consumers !== void 0;
}
function Wi(e6) {
  au?.(e6);
}
function uu(e6, t) {
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
function qi(e6, t) {
  return Object.is(e6, t);
}
function lu() {
  throw new Error();
}
var Zi = lu;
function Yi(e6) {
  Zi(e6);
}
function yr(e6) {
  Zi = e6;
}
var du = null;
function Dr(e6, t) {
  let n = Object.create(Ji);
  n.value = e6, t !== void 0 && (n.equal = t);
  let r = () => Qi(n);
  return r[W] = n, Wi(n), [r, (s) => vr(n, s), (s) => Ki(n, s)];
}
function Qi(e6) {
  return Bi(e6), e6.value;
}
function vr(e6, t) {
  pr() || Yi(e6), e6.equal(e6.value, t) || (e6.value = t, fu(e6));
}
function Ki(e6, t) {
  pr() || Yi(e6), vr(e6, t(e6.value));
}
var Ji = V(x({}, Yt), { equal: qi, value: void 0, kind: "signal" });
function fu(e6) {
  e6.version++, Vi(), fr(e6), du?.(e6);
}
function N(e6) {
  return typeof e6 == "function";
}
function Kt(e6) {
  let n = e6((r) => {
    Error.call(r), r.stack = new Error().stack;
  });
  return n.prototype = Object.create(Error.prototype), n.prototype.constructor = n, n;
}
var Jt = Kt((e6) => function(n) {
  e6(this), this.message = n ? `${n.length} errors occurred during unsubscription:
${n.map((r, o) => `${o + 1}) ${r.toString()}`).join(`
  `)}` : "", this.name = "UnsubscriptionError", this.errors = n;
});
function st(e6, t) {
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
          t = i instanceof Jt ? i.errors : [i];
        }
      let { _finalizers: o } = this;
      if (o) {
        this._finalizers = null;
        for (let i of o)
          try {
            Xi(i);
          } catch (s) {
            t = t ?? [], s instanceof Jt ? t = [...t, ...s.errors] : t.push(s);
          }
      }
      if (t)
        throw new Jt(t);
    }
  }
  add(t) {
    var n;
    if (t && t !== this)
      if (this.closed)
        Xi(t);
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
    n === t ? this._parentage = null : Array.isArray(n) && st(n, t);
  }
  remove(t) {
    let { _finalizers: n } = this;
    n && st(n, t), t instanceof e && t._removeParent(this);
  }
};
b.EMPTY = (() => {
  let e6 = new b();
  return e6.closed = true, e6;
})();
var Er = b.EMPTY;
function Xt(e6) {
  return e6 instanceof b || e6 && "closed" in e6 && N(e6.remove) && N(e6.add) && N(e6.unsubscribe);
}
function Xi(e6) {
  N(e6) ? e6() : e6.unsubscribe();
}
var H = { onUnhandledError: null, onStoppedNotification: null, Promise: void 0, useDeprecatedSynchronousErrorHandling: false, useDeprecatedNextContext: false };
var Le = { setTimeout(e6, t, ...n) {
  let { delegate: r } = Le;
  return r?.setTimeout ? r.setTimeout(e6, t, ...n) : setTimeout(e6, t, ...n);
}, clearTimeout(e6) {
  let { delegate: t } = Le;
  return (t?.clearTimeout || clearTimeout)(e6);
}, delegate: void 0 };
function es(e6) {
  Le.setTimeout(() => {
    let { onUnhandledError: t } = H;
    if (t)
      t(e6);
    else
      throw e6;
  });
}
function Ir() {
}
var ts = Cr("C", void 0, void 0);
function ns(e6) {
  return Cr("E", void 0, e6);
}
function rs(e6) {
  return Cr("N", e6, void 0);
}
function Cr(e6, t, n) {
  return { kind: e6, value: t, error: n };
}
var ve = null;
function Pe(e6) {
  if (H.useDeprecatedSynchronousErrorHandling) {
    let t = !ve;
    if (t && (ve = { errorThrown: false, error: null }), e6(), t) {
      let { errorThrown: n, error: r } = ve;
      if (ve = null, n)
        throw r;
    }
  } else
    e6();
}
function os(e6) {
  H.useDeprecatedSynchronousErrorHandling && ve && (ve.errorThrown = true, ve.error = e6);
}
var Ee = class extends b {
  constructor(t) {
    super(), this.isStopped = false, t ? (this.destination = t, Xt(t) && t.add(this)) : this.destination = gu;
  }
  static create(t, n, r) {
    return new je(t, n, r);
  }
  next(t) {
    this.isStopped ? Tr(rs(t), this) : this._next(t);
  }
  error(t) {
    this.isStopped ? Tr(ns(t), this) : (this.isStopped = true, this._error(t));
  }
  complete() {
    this.isStopped ? Tr(ts, this) : (this.isStopped = true, this._complete());
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
var pu = Function.prototype.bind;
function wr(e6, t) {
  return pu.call(e6, t);
}
var Mr = class {
  constructor(t) {
    this.partialObserver = t;
  }
  next(t) {
    let { partialObserver: n } = this;
    if (n.next)
      try {
        n.next(t);
      } catch (r) {
        en(r);
      }
  }
  error(t) {
    let { partialObserver: n } = this;
    if (n.error)
      try {
        n.error(t);
      } catch (r) {
        en(r);
      }
    else
      en(t);
  }
  complete() {
    let { partialObserver: t } = this;
    if (t.complete)
      try {
        t.complete();
      } catch (n) {
        en(n);
      }
  }
};
var je = class extends Ee {
  constructor(t, n, r) {
    super();
    let o;
    if (N(t) || !t)
      o = { next: t ?? void 0, error: n ?? void 0, complete: r ?? void 0 };
    else {
      let i;
      this && H.useDeprecatedNextContext ? (i = Object.create(t), i.unsubscribe = () => this.unsubscribe(), o = { next: t.next && wr(t.next, i), error: t.error && wr(t.error, i), complete: t.complete && wr(t.complete, i) }) : o = t;
    }
    this.destination = new Mr(o);
  }
};
function en(e6) {
  H.useDeprecatedSynchronousErrorHandling ? os(e6) : es(e6);
}
function hu(e6) {
  throw e6;
}
function Tr(e6, t) {
  let { onStoppedNotification: n } = H;
  n && Le.setTimeout(() => n(e6, t));
}
var gu = { closed: true, next: Ir, error: hu, complete: Ir };
var is = typeof Symbol == "function" && Symbol.observable || "@@observable";
function ss(e6) {
  return e6;
}
function as(e6) {
  return e6.length === 0 ? ss : e6.length === 1 ? e6[0] : function(n) {
    return e6.reduce((r, o) => o(r), n);
  };
}
var Be = (() => {
  class e6 {
    constructor(n) {
      n && (this._subscribe = n);
    }
    lift(n) {
      let r = new e6();
      return r.source = this, r.operator = n, r;
    }
    subscribe(n, r, o) {
      let i = yu(n) ? n : new je(n, r, o);
      return Pe(() => {
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
      return r = cs(r), new r((o, i) => {
        let s = new je({ next: (a) => {
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
    [is]() {
      return this;
    }
    pipe(...n) {
      return as(n)(this);
    }
    toPromise(n) {
      return n = cs(n), new n((r, o) => {
        let i;
        this.subscribe((s) => i = s, (s) => o(s), () => r(i));
      });
    }
  }
  return e6.create = (t) => new e6(t), e6;
})();
function cs(e6) {
  var t;
  return (t = e6 ?? H.Promise) !== null && t !== void 0 ? t : Promise;
}
function mu(e6) {
  return e6 && N(e6.next) && N(e6.error) && N(e6.complete);
}
function yu(e6) {
  return e6 && e6 instanceof Ee || mu(e6) && Xt(e6);
}
function Du(e6) {
  return N(e6?.lift);
}
function us(e6) {
  return (t) => {
    if (Du(t))
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
function ls(e6, t, n, r, o) {
  return new _r(e6, t, n, r, o);
}
var _r = class extends Ee {
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
var ds = Kt((e6) => function() {
  e6(this), this.name = "ObjectUnsubscribedError", this.message = "object unsubscribed";
});
var ce = (() => {
  class e6 extends Be {
    constructor() {
      super(), this.closed = false, this.currentObservers = null, this.observers = [], this.isStopped = false, this.hasError = false, this.thrownError = null;
    }
    lift(n) {
      let r = new tn(this, this);
      return r.operator = n, r;
    }
    _throwIfClosed() {
      if (this.closed)
        throw new ds();
    }
    next(n) {
      Pe(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.currentObservers || (this.currentObservers = Array.from(this.observers));
          for (let r of this.currentObservers)
            r.next(n);
        }
      });
    }
    error(n) {
      Pe(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.hasError = this.isStopped = true, this.thrownError = n;
          let { observers: r } = this;
          for (; r.length; )
            r.shift().error(n);
        }
      });
    }
    complete() {
      Pe(() => {
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
      return r || o ? Er : (this.currentObservers = null, i.push(n), new b(() => {
        this.currentObservers = null, st(i, n);
      }));
    }
    _checkFinalizedStatuses(n) {
      let { hasError: r, thrownError: o, isStopped: i } = this;
      r ? n.error(o) : i && n.complete();
    }
    asObservable() {
      let n = new Be();
      return n.source = this, n;
    }
  }
  return e6.create = (t, n) => new tn(t, n), e6;
})();
var tn = class extends ce {
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
    return (r = (n = this.source) === null || n === void 0 ? void 0 : n.subscribe(t)) !== null && r !== void 0 ? r : Er;
  }
};
var at = class extends ce {
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
function Sr(e6, t) {
  return us((n, r) => {
    let o = 0;
    n.subscribe(ls(r, (i) => {
      r.next(e6.call(t, i, o++));
    }));
  });
}
var br;
function nn() {
  return br;
}
function q(e6) {
  let t = br;
  return br = e6, t;
}
var fs = Symbol("NotFound");
function Ve(e6) {
  return e6 === fs || e6?.name === "\u0275NotFound";
}
var un = "https://angular.dev/best-practices/security#preventing-cross-site-scripting-xss";
var g = class extends Error {
  code;
  constructor(t, n) {
    super(ln(t, n)), this.code = t;
  }
};
function Cu(e6) {
  return `NG0${Math.abs(e6)}`;
}
function ln(e6, t) {
  return `${Cu(e6)}${t ? ": " + t : ""}`;
}
var ue = globalThis;
function w(e6) {
  for (let t in e6)
    if (e6[t] === w)
      return t;
  throw Error("");
}
function zr(e6, t) {
  return e6 ? t ? `${e6} ${t}` : e6 : t || "";
}
var wu = w({ __forward_ref__: w });
function dn(e6) {
  return e6.__forward_ref__ = dn, e6;
}
function O(e6) {
  return ys(e6) ? e6() : e6;
}
function ys(e6) {
  return typeof e6 == "function" && e6.hasOwnProperty(wu) && e6.__forward_ref__ === dn;
}
function _(e6) {
  return { token: e6.token, providedIn: e6.providedIn || null, factory: e6.factory, value: void 0 };
}
function ze(e6) {
  return { providers: e6.providers || [], imports: e6.imports || [] };
}
function fn(e6) {
  return Tu(e6, pn);
}
function Tu(e6, t) {
  return e6.hasOwnProperty(t) && e6[t] || null;
}
function Mu(e6) {
  let t = e6?.[pn] ?? null;
  return t || null;
}
function Ar(e6) {
  return e6 && e6.hasOwnProperty(on) ? e6[on] : null;
}
var pn = w({ \u0275prov: w });
var on = w({ \u0275inj: w });
var m = class {
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
function Gr(e6) {
  return e6 && !!e6.\u0275providers;
}
var Wr = w({ \u0275cmp: w });
var qr = w({ \u0275dir: w });
var Zr = w({ \u0275pipe: w });
var xr = w({ \u0275fac: w });
var Me = w({ __NG_ELEMENT_ID__: w });
var ps = w({ __NG_ENV_ID__: w });
function ft(e6) {
  return Qr(e6, "@Component"), e6[Wr] || null;
}
function Yr(e6) {
  return Qr(e6, "@Directive"), e6[qr] || null;
}
function Ds(e6) {
  return Qr(e6, "@Pipe"), e6[Zr] || null;
}
function Qr(e6, t) {
  if (e6 == null)
    throw new g(-919, false);
}
function Kr(e6) {
  return typeof e6 == "string" ? e6 : e6 == null ? "" : String(e6);
}
var vs = w({ ngErrorCode: w });
var _u = w({ ngErrorMessage: w });
var Su = w({ ngTokenPath: w });
function Jr(e6, t) {
  return Es("", -200, t);
}
function hn(e6, t) {
  throw new g(-201, false);
}
function Es(e6, t, n) {
  let r = new g(t, e6);
  return r[vs] = t, r[_u] = e6, n && (r[Su] = n), r;
}
function bu(e6) {
  return e6[vs];
}
var Rr;
function Is() {
  return Rr;
}
function R(e6) {
  let t = Rr;
  return Rr = e6, t;
}
function Xr(e6, t, n) {
  let r = fn(e6);
  if (r && r.providedIn == "root")
    return r.value === void 0 ? r.value = r.factory() : r.value;
  if (n & 8)
    return null;
  if (t !== void 0)
    return t;
  hn(e6, "");
}
var Nu = {};
var Ie = Nu;
var Au = "__NG_DI_FLAG__";
var Or = class {
  injector;
  constructor(t) {
    this.injector = t;
  }
  retrieve(t, n) {
    let r = Ce(n) || 0;
    try {
      return this.injector.get(t, r & 8 ? null : Ie, r);
    } catch (o) {
      if (Ve(o))
        return o;
      throw o;
    }
  }
};
function xu(e6, t = 0) {
  let n = nn();
  if (n === void 0)
    throw new g(-203, false);
  if (n === null)
    return Xr(e6, void 0, t);
  {
    let r = Ru(t), o = n.retrieve(e6, r);
    if (Ve(o)) {
      if (r.optional)
        return null;
      throw o;
    }
    return o;
  }
}
function E(e6, t = 0) {
  return (Is() || xu)(O(e6), t);
}
function v(e6, t) {
  return E(e6, Ce(t));
}
function Ce(e6) {
  return typeof e6 > "u" || typeof e6 == "number" ? e6 : 0 | (e6.optional && 8) | (e6.host && 1) | (e6.self && 2) | (e6.skipSelf && 4);
}
function Ru(e6) {
  return { optional: !!(e6 & 8), host: !!(e6 & 1), self: !!(e6 & 2), skipSelf: !!(e6 & 4) };
}
function kr(e6) {
  let t = [];
  for (let n = 0; n < e6.length; n++) {
    let r = O(e6[n]);
    if (Array.isArray(r)) {
      if (r.length === 0)
        throw new g(900, false);
      let o, i = 0;
      for (let s = 0; s < r.length; s++) {
        let a = r[s], c = Ou(a);
        typeof c == "number" ? c === -1 ? o = a.token : i |= c : o = a;
      }
      t.push(E(o, i));
    } else
      t.push(E(r));
  }
  return t;
}
function Ou(e6) {
  return e6[Au];
}
function $e(e6, t) {
  let n = e6.hasOwnProperty(xr);
  return n ? e6[xr] : null;
}
function gn(e6, t) {
  e6.forEach((n) => Array.isArray(n) ? gn(n, t) : t(n));
}
function eo(e6, t) {
  return t >= e6.length - 1 ? e6.pop() : e6.splice(t, 1)[0];
}
var _e = {};
var $ = [];
var Se = new m("");
var to = new m("", -1);
var no = new m("");
var ut = class {
  get(t, n = Ie) {
    if (n === Ie) {
      let o = Es("", -201);
      throw o.name = "\u0275NotFound", o;
    }
    return n;
  }
};
function pt(e6) {
  return { \u0275providers: e6 };
}
function Cs(e6) {
  return pt([{ provide: Se, multi: true, useValue: e6 }]);
}
function ws(...e6) {
  return { \u0275providers: ro(true, e6), \u0275fromNgModule: true };
}
function ro(e6, ...t) {
  let n = [], r = /* @__PURE__ */ new Set(), o, i = (s) => {
    n.push(s);
  };
  return gn(t, (s) => {
    let a = s;
    sn(a, i, [], r) && (o ||= [], o.push(a));
  }), o !== void 0 && Ts(o, i), n;
}
function Ts(e6, t) {
  for (let n = 0; n < e6.length; n++) {
    let { ngModule: r, providers: o } = e6[n];
    oo(o, (i) => {
      t(i, r);
    });
  }
}
function sn(e6, t, n, r) {
  if (e6 = O(e6), !e6)
    return false;
  let o = null, i = Ar(e6), s = !i && ft(e6);
  if (!i && !s) {
    let c = e6.ngModule;
    if (i = Ar(c), i)
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
        sn(u, t, n, r);
    }
  } else if (i) {
    if (i.imports != null && !a) {
      r.add(o);
      let u;
      gn(i.imports, (l) => {
        sn(l, t, n, r) && (u ||= [], u.push(l));
      }), u !== void 0 && Ts(u, t);
    }
    if (!a) {
      let u = $e(o) || (() => new o());
      t({ provide: o, useFactory: u, deps: $ }, o), t({ provide: no, useValue: o, multi: true }, o), t({ provide: Se, useValue: () => E(o), multi: true }, o);
    }
    let c = i.providers;
    if (c != null && !a) {
      let u = e6;
      oo(c, (l) => {
        t(l, u);
      });
    }
  } else
    return false;
  return o !== e6 && e6.providers !== void 0;
}
function oo(e6, t) {
  for (let n of e6)
    Gr(n) && (n = n.\u0275providers), Array.isArray(n) ? oo(n, t) : t(n);
}
var ku = w({ provide: String, useValue: w });
function Ms(e6) {
  return e6 !== null && typeof e6 == "object" && ku in e6;
}
function Fu(e6) {
  return !!(e6 && e6.useExisting);
}
function Lu(e6) {
  return !!(e6 && e6.useFactory);
}
function an(e6) {
  return typeof e6 == "function";
}
var ht = new m("");
var rn = {};
var hs = {};
var Nr;
function gt() {
  return Nr === void 0 && (Nr = new ut()), Nr;
}
var U = class {
};
var we = class extends U {
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
    super(), this.parent = n, this.source = r, this.scopes = o, Lr(t, (s) => this.processProvider(s)), this.records.set(to, He(void 0, this)), o.has("environment") && this.records.set(U, He(void 0, this));
    let i = this.records.get(ht);
    i != null && typeof i.value == "string" && this.scopes.add(i.value), this.injectorDefTypes = new Set(this.get(no, $, { self: true }));
  }
  retrieve(t, n) {
    let r = Ce(n) || 0;
    try {
      return this.get(t, Ie, r);
    } catch (o) {
      if (Ve(o))
        return o;
      throw o;
    }
  }
  destroy() {
    ct(this), this._destroyed = true;
    let t = D(null);
    try {
      for (let r of this._ngOnDestroyHooks)
        r.ngOnDestroy();
      let n = this._onDestroyHooks;
      this._onDestroyHooks = [];
      for (let r of n)
        r();
    } finally {
      this.records.clear(), this._ngOnDestroyHooks.clear(), this.injectorDefTypes.clear(), D(t);
    }
  }
  onDestroy(t) {
    return ct(this), this._onDestroyHooks.push(t), () => this.removeOnDestroy(t);
  }
  runInContext(t) {
    ct(this);
    let n = q(this), r = R(void 0), o;
    try {
      return t();
    } finally {
      q(n), R(r);
    }
  }
  get(t, n = Ie, r) {
    if (ct(this), t.hasOwnProperty(ps))
      return t[ps](this);
    let o = Ce(r), i, s = q(this), a = R(void 0);
    try {
      if (!(o & 4)) {
        let u = this.records.get(t);
        if (u === void 0) {
          let l = Hu(t) && fn(t);
          l && this.injectableDefInScope(l) ? u = He(Fr(t), rn) : u = null, this.records.set(t, u);
        }
        if (u != null)
          return this.hydrate(t, u, o);
      }
      let c = o & 2 ? gt() : this.parent;
      return n = o & 8 && n === Ie ? null : n, c.get(t, n);
    } catch (c) {
      let u = bu(c);
      throw u === -200 || u === -201 ? new g(u, null) : c;
    } finally {
      R(a), q(s);
    }
  }
  resolveInjectorInitializers() {
    let t = D(null), n = q(this), r = R(void 0), o;
    try {
      let i = this.get(Se, $, { self: true });
      for (let s of i)
        s();
    } finally {
      q(n), R(r), D(t);
    }
  }
  toString() {
    return "R3Injector[...]";
  }
  processProvider(t) {
    t = O(t);
    let n = an(t) ? t : O(t && t.provide), r = ju(t);
    if (!an(t) && t.multi === true) {
      let o = this.records.get(n);
      o || (o = He(void 0, rn, true), o.factory = () => kr(o.multi), this.records.set(n, o)), n = t, o.multi.push(t);
    }
    this.records.set(n, r);
  }
  hydrate(t, n, r) {
    let o = D(null);
    try {
      if (n.value === hs)
        throw Jr("");
      return n.value === rn && (n.value = hs, n.value = n.factory(void 0, r)), typeof n.value == "object" && n.value && Vu(n.value) && this._ngOnDestroyHooks.add(n.value), n.value;
    } finally {
      D(o);
    }
  }
  injectableDefInScope(t) {
    if (!t.providedIn)
      return false;
    let n = O(t.providedIn);
    return typeof n == "string" ? n === "any" || this.scopes.has(n) : this.injectorDefTypes.has(n);
  }
  removeOnDestroy(t) {
    let n = this._onDestroyHooks.indexOf(t);
    n !== -1 && this._onDestroyHooks.splice(n, 1);
  }
};
function Fr(e6) {
  let t = fn(e6), n = t !== null ? t.factory : $e(e6);
  if (n !== null)
    return n;
  if (e6 instanceof m)
    throw new g(-204, false);
  if (e6 instanceof Function)
    return Pu(e6);
  throw new g(-204, false);
}
function Pu(e6) {
  if (e6.length > 0)
    throw new g(-204, false);
  let n = Mu(e6);
  return n !== null ? () => n.factory(e6) : () => new e6();
}
function ju(e6) {
  if (Ms(e6))
    return He(void 0, e6.useValue);
  {
    let t = _s(e6);
    return He(t, rn);
  }
}
function _s(e6, t, n) {
  let r;
  if (an(e6)) {
    let o = O(e6);
    return $e(o) || Fr(o);
  } else if (Ms(e6))
    r = () => O(e6.useValue);
  else if (Lu(e6))
    r = () => e6.useFactory(...kr(e6.deps || []));
  else if (Fu(e6))
    r = (o, i) => E(O(e6.useExisting), i !== void 0 && i & 8 ? 8 : void 0);
  else {
    let o = O(e6 && (e6.useClass || e6.provide));
    if (Bu(e6))
      r = () => new o(...kr(e6.deps));
    else
      return $e(o) || Fr(o);
  }
  return r;
}
function ct(e6) {
  if (e6.destroyed)
    throw new g(-205, false);
}
function He(e6, t, n = false) {
  return { factory: e6, value: t, multi: n ? [] : void 0 };
}
function Bu(e6) {
  return !!e6.deps;
}
function Vu(e6) {
  return e6 !== null && typeof e6 == "object" && typeof e6.ngOnDestroy == "function";
}
function Hu(e6) {
  return typeof e6 == "function" || typeof e6 == "object" && e6.ngMetadataName === "InjectionToken";
}
function Lr(e6, t) {
  for (let n of e6)
    Array.isArray(n) ? Lr(n, t) : n && Gr(n) ? Lr(n.\u0275providers, t) : t(n);
}
function mn(e6, t) {
  let n;
  e6 instanceof we ? (ct(e6), n = e6) : n = new Or(e6);
  let r, o = q(n), i = R(void 0);
  try {
    return t();
  } finally {
    q(o), R(i);
  }
}
function Ss() {
  return Is() !== void 0 || nn() != null;
}
var Z = 0;
var y = 1;
var h = 2;
var k = 3;
var re = 4;
var oe = 5;
var yn = 6;
var Dn = 7;
var F = 8;
var be = 9;
var Y = 10;
var L = 11;
var Ge = 12;
var io = 13;
var We = 14;
var Q = 15;
var mt = 16;
var Ne = 17;
var vn = 18;
var le = 19;
var so = 20;
var ee = 21;
var En = 22;
var yt = 23;
var P = 24;
var In = 25;
var qe = 26;
var z = 27;
var bs = 1;
var Cn = 7;
var Ns = 8;
var Dt = 9;
var ie = 10;
function de(e6) {
  return Array.isArray(e6) && typeof e6[bs] == "object";
}
function fe(e6) {
  return Array.isArray(e6) && e6[bs] === true;
}
function ao(e6) {
  return (e6.flags & 4) !== 0;
}
function vt(e6) {
  return e6.componentOffset > -1;
}
function As(e6) {
  return (e6.flags & 1) === 1;
}
function Ze(e6) {
  return !!e6.template;
}
function Ye(e6) {
  return (e6[h] & 512) !== 0;
}
function Ae(e6) {
  return (e6[h] & 256) === 256;
}
var xs = "svg";
var Rs = "math";
function pe(e6) {
  for (; Array.isArray(e6); )
    e6 = e6[Z];
  return e6;
}
function Os(e6, t) {
  return pe(t[e6]);
}
function xe(e6, t) {
  return pe(t[e6.index]);
}
function co(e6, t) {
  return e6.data[t];
}
function he(e6, t) {
  let n = t[e6];
  return de(n) ? n : n[Z];
}
function wn(e6) {
  return (e6[h] & 128) === 128;
}
function Et(e6, t) {
  return t == null ? null : e6[t];
}
function uo(e6) {
  e6[Ne] = 0;
}
function lo(e6) {
  e6[h] & 1024 || (e6[h] |= 1024, wn(e6) && Ct(e6));
}
function It(e6) {
  return !!(e6[h] & 9216 || e6[P]?.dirty);
}
function fo(e6) {
  e6[Y].changeDetectionScheduler?.notify(8), e6[h] & 64 && (e6[h] |= 1024), It(e6) && Ct(e6);
}
function Ct(e6) {
  e6[Y].changeDetectionScheduler?.notify(0);
  let t = Te(e6);
  for (; t !== null && !(t[h] & 8192 || (t[h] |= 8192, !wn(t))); )
    t = Te(t);
}
function po(e6, t) {
  if (Ae(e6))
    throw new g(911, false);
  e6[ee] === null && (e6[ee] = []), e6[ee].push(t);
}
function ks(e6, t) {
  if (e6[ee] === null)
    return;
  let n = e6[ee].indexOf(t);
  n !== -1 && e6[ee].splice(n, 1);
}
function Te(e6) {
  let t = e6[k];
  return fe(t) ? t[k] : t;
}
var I = { lFrame: Zs(null), bindingsEnabled: true, skipHydrationRootTNode: null };
var Pr = false;
function Fs() {
  return I.lFrame.elementDepthCount;
}
function Ls() {
  I.lFrame.elementDepthCount++;
}
function Ps() {
  I.lFrame.elementDepthCount--;
}
function js() {
  return I.skipHydrationRootTNode !== null;
}
function Bs(e6) {
  return I.skipHydrationRootTNode === e6;
}
function Vs() {
  I.skipHydrationRootTNode = null;
}
function B() {
  return I.lFrame.lView;
}
function Tn() {
  return I.lFrame.tView;
}
function Qe() {
  let e6 = ho();
  for (; e6 !== null && e6.type === 64; )
    e6 = e6.parent;
  return e6;
}
function ho() {
  return I.lFrame.currentTNode;
}
function Hs() {
  let e6 = I.lFrame, t = e6.currentTNode;
  return e6.isParent ? t : t.parent;
}
function wt(e6, t) {
  let n = I.lFrame;
  n.currentTNode = e6, n.isParent = t;
}
function go() {
  return I.lFrame.isParent;
}
function $s() {
  I.lFrame.isParent = false;
}
function mo() {
  return Pr;
}
function yo(e6) {
  let t = Pr;
  return Pr = e6, t;
}
function Us(e6) {
  return I.lFrame.bindingIndex = e6;
}
function Do() {
  return I.lFrame.bindingIndex++;
}
function zs() {
  return I.lFrame.inI18n;
}
function Gs(e6, t) {
  let n = I.lFrame;
  n.bindingIndex = n.bindingRootIndex = e6, Mn(t);
}
function Ws() {
  return I.lFrame.currentDirectiveIndex;
}
function Mn(e6) {
  I.lFrame.currentDirectiveIndex = e6;
}
function vo(e6) {
  I.lFrame.currentQueryIndex = e6;
}
function $u(e6) {
  let t = e6[y];
  return t.type === 2 ? t.declTNode : t.type === 1 ? e6[oe] : null;
}
function Eo(e6, t, n) {
  if (n & 4) {
    let o = t, i = e6;
    for (; o = o.parent, o === null && !(n & 1); )
      if (o = $u(i), o === null || (i = i[We], o.type & 10))
        break;
    if (o === null)
      return false;
    t = o, e6 = i;
  }
  let r = I.lFrame = qs();
  return r.currentTNode = t, r.lView = e6, true;
}
function _n(e6) {
  let t = qs(), n = e6[y];
  I.lFrame = t, t.currentTNode = n.firstChild, t.lView = e6, t.tView = n, t.contextLView = e6, t.bindingIndex = n.bindingStartIndex, t.inI18n = false;
}
function qs() {
  let e6 = I.lFrame, t = e6 === null ? null : e6.child;
  return t === null ? Zs(e6) : t;
}
function Zs(e6) {
  let t = { currentTNode: null, isParent: true, lView: null, tView: null, selectedIndex: -1, contextLView: null, elementDepthCount: 0, currentNamespace: null, currentDirectiveIndex: -1, bindingRootIndex: -1, bindingIndex: -1, currentQueryIndex: 0, parent: e6, child: null, inI18n: false };
  return e6 !== null && (e6.child = t), t;
}
function Ys() {
  let e6 = I.lFrame;
  return I.lFrame = e6.parent, e6.currentTNode = null, e6.lView = null, e6;
}
var Io = Ys;
function Sn() {
  let e6 = Ys();
  e6.isParent = true, e6.tView = null, e6.selectedIndex = -1, e6.contextLView = null, e6.elementDepthCount = 0, e6.currentDirectiveIndex = -1, e6.currentNamespace = null, e6.bindingRootIndex = -1, e6.bindingIndex = -1, e6.currentQueryIndex = 0;
}
function bn() {
  return I.lFrame.selectedIndex;
}
function ge(e6) {
  I.lFrame.selectedIndex = e6;
}
function Qs() {
  let e6 = I.lFrame;
  return co(e6.tView, e6.selectedIndex);
}
function Ks() {
  return I.lFrame.currentNamespace;
}
var Js = true;
function Co() {
  return Js;
}
function wo(e6) {
  Js = e6;
}
function jr(e6, t = null, n = null, r) {
  let o = Xs(e6, t, n, r);
  return o.resolveInjectorInitializers(), o;
}
function Xs(e6, t = null, n = null, r, o = /* @__PURE__ */ new Set()) {
  let i = [n || $, ws(e6)], s;
  return new we(i, t || gt(), s || null, o);
}
var te = class e2 {
  static THROW_IF_NOT_FOUND = Ie;
  static NULL = new ut();
  static create(t, n) {
    if (Array.isArray(t))
      return jr({ name: "" }, n, t, "");
    {
      let r = t.name ?? "";
      return jr({ name: r }, t.parent, t.providers, r);
    }
  }
  static \u0275prov = _({ token: e2, providedIn: "any", factory: () => E(to) });
  static __NG_ELEMENT_ID__ = -1;
};
var A = new m("");
var Tt = /* @__PURE__ */ (() => {
  class e6 {
    static __NG_ELEMENT_ID__ = Uu;
    static __NG_ENV_ID__ = (n) => n;
  }
  return e6;
})();
var Br = class extends Tt {
  _lView;
  constructor(t) {
    super(), this._lView = t;
  }
  get destroyed() {
    return Ae(this._lView);
  }
  onDestroy(t) {
    let n = this._lView;
    return po(n, t), () => ks(n, t);
  }
};
function Uu() {
  return new Br(B());
}
var ea = false;
var ta = new m("");
var Ke = (() => {
  class e6 {
    taskId = 0;
    pendingTasks = /* @__PURE__ */ new Set();
    destroyed = false;
    pendingTask = new at(false);
    debugTaskTracker = v(ta, { optional: true });
    get hasPendingTasks() {
      return this.destroyed ? false : this.pendingTask.value;
    }
    get hasPendingTasksObservable() {
      return this.destroyed ? new Be((n) => {
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
var Vr = class extends ce {
  __isAsync;
  destroyRef = void 0;
  pendingTasks = void 0;
  constructor(t = false) {
    super(), this.__isAsync = t, Ss() && (this.destroyRef = v(Tt, { optional: true }) ?? void 0, this.pendingTasks = v(Ke, { optional: true }) ?? void 0);
  }
  emit(t) {
    let n = D(null);
    try {
      super.next(t);
    } finally {
      D(n);
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
var X = Vr;
function cn(...e6) {
}
function To(e6) {
  let t, n;
  function r() {
    e6 = cn;
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
function na(e6) {
  return queueMicrotask(() => e6()), () => {
    e6 = cn;
  };
}
var Mo = "isAngularZone";
var lt = Mo + "_ID";
var zu = 0;
var j = class e3 {
  hasPendingMacrotasks = false;
  hasPendingMicrotasks = false;
  isStable = true;
  onUnstable = new X(false);
  onMicrotaskEmpty = new X(false);
  onStable = new X(false);
  onError = new X(false);
  constructor(t) {
    let { enableLongStackTrace: n = false, shouldCoalesceEventChangeDetection: r = false, shouldCoalesceRunChangeDetection: o = false, scheduleInRootZone: i = ea } = t;
    if (typeof Zone > "u")
      throw new g(908, false);
    Zone.assertZonePatched();
    let s = this;
    s._nesting = 0, s._outer = s._inner = Zone.current, Zone.TaskTrackingZoneSpec && (s._inner = s._inner.fork(new Zone.TaskTrackingZoneSpec())), n && Zone.longStackTraceZoneSpec && (s._inner = s._inner.fork(Zone.longStackTraceZoneSpec)), s.shouldCoalesceEventChangeDetection = !o && r, s.shouldCoalesceRunChangeDetection = o, s.callbackScheduled = false, s.scheduleInRootZone = i, qu(s);
  }
  static isInAngularZone() {
    return typeof Zone < "u" && Zone.current.get(Mo) === true;
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
    let i = this._inner, s = i.scheduleEventTask("NgZoneEvent: " + o, t, Gu, cn, cn);
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
var Gu = {};
function _o(e6) {
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
function Wu(e6) {
  if (e6.isCheckStableRunning || e6.callbackScheduled)
    return;
  e6.callbackScheduled = true;
  function t() {
    To(() => {
      e6.callbackScheduled = false, Hr(e6), e6.isCheckStableRunning = true, _o(e6), e6.isCheckStableRunning = false;
    });
  }
  e6.scheduleInRootZone ? Zone.root.run(() => {
    t();
  }) : e6._outer.run(() => {
    t();
  }), Hr(e6);
}
function qu(e6) {
  let t = () => {
    Wu(e6);
  }, n = zu++;
  e6._inner = e6._inner.fork({ name: "angular", properties: { [Mo]: true, [lt]: n, [lt + n]: true }, onInvokeTask: (r, o, i, s, a, c) => {
    if (Zu(c))
      return r.invokeTask(i, s, a, c);
    try {
      return gs(e6), r.invokeTask(i, s, a, c);
    } finally {
      (e6.shouldCoalesceEventChangeDetection && s.type === "eventTask" || e6.shouldCoalesceRunChangeDetection) && t(), ms(e6);
    }
  }, onInvoke: (r, o, i, s, a, c, u) => {
    try {
      return gs(e6), r.invoke(i, s, a, c, u);
    } finally {
      e6.shouldCoalesceRunChangeDetection && !e6.callbackScheduled && !Yu(c) && t(), ms(e6);
    }
  }, onHasTask: (r, o, i, s) => {
    r.hasTask(i, s), o === i && (s.change == "microTask" ? (e6._hasPendingMicrotasks = s.microTask, Hr(e6), _o(e6)) : s.change == "macroTask" && (e6.hasPendingMacrotasks = s.macroTask));
  }, onHandleError: (r, o, i, s) => (r.handleError(i, s), e6.runOutsideAngular(() => e6.onError.emit(s)), false) });
}
function Hr(e6) {
  e6._hasPendingMicrotasks || (e6.shouldCoalesceEventChangeDetection || e6.shouldCoalesceRunChangeDetection) && e6.callbackScheduled === true ? e6.hasPendingMicrotasks = true : e6.hasPendingMicrotasks = false;
}
function gs(e6) {
  e6._nesting++, e6.isStable && (e6.isStable = false, e6.onUnstable.emit(null));
}
function ms(e6) {
  e6._nesting--, _o(e6);
}
var dt = class {
  hasPendingMicrotasks = false;
  hasPendingMacrotasks = false;
  isStable = true;
  onUnstable = new X();
  onMicrotaskEmpty = new X();
  onStable = new X();
  onError = new X();
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
function Zu(e6) {
  return ra(e6, "__ignore_ng_zone__");
}
function Yu(e6) {
  return ra(e6, "__scheduler_tick__");
}
function ra(e6, t) {
  return !Array.isArray(e6) || e6.length !== 1 ? false : e6[0]?.data?.[t] === true;
}
var ne = class {
  _console = console;
  handleError(t) {
    this._console.error("ERROR", t);
  }
};
var Je = new m("", { factory: () => {
  let e6 = v(j), t = v(U), n;
  return (r) => {
    e6.runOutsideAngular(() => {
      t.destroyed && !n ? setTimeout(() => {
        throw r;
      }) : (n ??= t.get(ne), n.handleError(r));
    });
  };
} });
var oa = { provide: Se, useValue: () => {
  let e6 = v(ne, { optional: true });
}, multi: true };
var Qu = new m("", { factory: () => {
  let e6 = v(A).defaultView;
  if (!e6)
    return;
  let t = v(Je), n = (i) => {
    t(i.reason), i.preventDefault();
  }, r = (i) => {
    i.error ? t(i.error) : t(new Error(i.message, { cause: i })), i.preventDefault();
  }, o = () => {
    e6.addEventListener("unhandledrejection", n), e6.addEventListener("error", r);
  };
  typeof Zone < "u" ? Zone.root.run(o) : o(), v(Tt).onDestroy(() => {
    e6.removeEventListener("error", r), e6.removeEventListener("unhandledrejection", n);
  });
} });
function So() {
  return pt([Cs(() => {
    v(Qu);
  })]);
}
function Mt(e6, t) {
  let [n, r, o] = Dr(e6, t?.equal), i = n, s = i[W];
  return i.set = r, i.update = o, i.asReadonly = ia.bind(i), i;
}
function ia() {
  let e6 = this[W];
  if (e6.readonlyFn === void 0) {
    let t = () => this();
    t[W] = e6, e6.readonlyFn = t;
  }
  return e6.readonlyFn;
}
var Ue = class {
};
var _t = new m("", { factory: () => true });
var bo = new m("");
var No = (() => {
  class e6 {
    static \u0275prov = _({ token: e6, providedIn: "root", factory: () => new $r() });
  }
  return e6;
})();
var $r = class {
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
var Ur = class {
  [W];
  constructor(t) {
    this[W] = t;
  }
  destroy() {
    this[W].destroy();
  }
};
function ri(e6) {
  return { toString: e6 }.toString();
}
function Na(e6, t, n, r) {
  t !== null ? t.applyValueToInputSignal(t, r) : e6[n] = r;
}
var Fn = class {
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
function pl(e6) {
  return e6.type.prototype.ngOnChanges && (e6.setInput = gl), hl;
}
function hl() {
  let e6 = xa(this), t = e6?.current;
  if (t) {
    let n = e6.previous;
    if (n === _e)
      e6.previous = t;
    else
      for (let r in t)
        n[r] = t[r];
    e6.current = null, this.ngOnChanges(t);
  }
}
function gl(e6, t, n, r, o) {
  let i = this.declaredInputs[r], s = xa(e6) || ml(e6, { previous: _e, current: null }), a = s.current || (s.current = {}), c = s.previous, u = c[i];
  a[i] = new Fn(u && u.currentValue, n, c === _e), Na(e6, t, o, n);
}
var Aa = "__ngSimpleChanges__";
function xa(e6) {
  return e6[Aa] || null;
}
function ml(e6, t) {
  return e6[Aa] = t;
}
var sa = [];
var M = function(e6, t = null, n) {
  for (let r = 0; r < sa.length; r++) {
    let o = sa[r];
    o(e6, t, n);
  }
};
var C = function(e6) {
  return e6[e6.TemplateCreateStart = 0] = "TemplateCreateStart", e6[e6.TemplateCreateEnd = 1] = "TemplateCreateEnd", e6[e6.TemplateUpdateStart = 2] = "TemplateUpdateStart", e6[e6.TemplateUpdateEnd = 3] = "TemplateUpdateEnd", e6[e6.LifecycleHookStart = 4] = "LifecycleHookStart", e6[e6.LifecycleHookEnd = 5] = "LifecycleHookEnd", e6[e6.OutputStart = 6] = "OutputStart", e6[e6.OutputEnd = 7] = "OutputEnd", e6[e6.BootstrapApplicationStart = 8] = "BootstrapApplicationStart", e6[e6.BootstrapApplicationEnd = 9] = "BootstrapApplicationEnd", e6[e6.BootstrapComponentStart = 10] = "BootstrapComponentStart", e6[e6.BootstrapComponentEnd = 11] = "BootstrapComponentEnd", e6[e6.ChangeDetectionStart = 12] = "ChangeDetectionStart", e6[e6.ChangeDetectionEnd = 13] = "ChangeDetectionEnd", e6[e6.ChangeDetectionSyncStart = 14] = "ChangeDetectionSyncStart", e6[e6.ChangeDetectionSyncEnd = 15] = "ChangeDetectionSyncEnd", e6[e6.AfterRenderHooksStart = 16] = "AfterRenderHooksStart", e6[e6.AfterRenderHooksEnd = 17] = "AfterRenderHooksEnd", e6[e6.ComponentStart = 18] = "ComponentStart", e6[e6.ComponentEnd = 19] = "ComponentEnd", e6[e6.DeferBlockStateStart = 20] = "DeferBlockStateStart", e6[e6.DeferBlockStateEnd = 21] = "DeferBlockStateEnd", e6[e6.DynamicComponentStart = 22] = "DynamicComponentStart", e6[e6.DynamicComponentEnd = 23] = "DynamicComponentEnd", e6[e6.HostBindingsUpdateStart = 24] = "HostBindingsUpdateStart", e6[e6.HostBindingsUpdateEnd = 25] = "HostBindingsUpdateEnd", e6;
}(C || {});
function yl(e6, t, n) {
  let { ngOnChanges: r, ngOnInit: o, ngDoCheck: i } = t.type.prototype;
  if (r) {
    let s = pl(t);
    (n.preOrderHooks ??= []).push(e6, s), (n.preOrderCheckHooks ??= []).push(e6, s);
  }
  o && (n.preOrderHooks ??= []).push(0 - e6, o), i && ((n.preOrderHooks ??= []).push(e6, i), (n.preOrderCheckHooks ??= []).push(e6, i));
}
function Dl(e6, t) {
  for (let n = t.directiveStart, r = t.directiveEnd; n < r; n++) {
    let i = e6.data[n].type.prototype, { ngAfterContentInit: s, ngAfterContentChecked: a, ngAfterViewInit: c, ngAfterViewChecked: u, ngOnDestroy: l } = i;
    s && (e6.contentHooks ??= []).push(-n, s), a && ((e6.contentHooks ??= []).push(n, a), (e6.contentCheckHooks ??= []).push(n, a)), c && (e6.viewHooks ??= []).push(-n, c), u && ((e6.viewHooks ??= []).push(n, u), (e6.viewCheckHooks ??= []).push(n, u)), l != null && (e6.destroyHooks ??= []).push(n, l);
  }
}
function Rn(e6, t, n) {
  Ra(e6, t, 3, n);
}
function On(e6, t, n, r) {
  (e6[h] & 3) === n && Ra(e6, t, n, r);
}
function Ao(e6, t) {
  let n = e6[h];
  (n & 3) === t && (n &= 16383, n += 1, e6[h] = n);
}
function Ra(e6, t, n, r) {
  let o = r !== void 0 ? e6[Ne] & 65535 : 0, i = r ?? -1, s = t.length - 1, a = 0;
  for (let c = o; c < s; c++)
    if (typeof t[c + 1] == "number") {
      if (a = t[c], r != null && a >= r)
        break;
    } else
      t[c] < 0 && (e6[Ne] += 65536), (a < i || i == -1) && (vl(e6, n, t, c), e6[Ne] = (e6[Ne] & 4294901760) + c + 2), c++;
}
function aa(e6, t) {
  M(C.LifecycleHookStart, e6, t);
  let n = D(null);
  try {
    t.call(e6);
  } finally {
    D(n), M(C.LifecycleHookEnd, e6, t);
  }
}
function vl(e6, t, n, r) {
  let o = n[r] < 0, i = n[r + 1], s = o ? -n[r] : n[r], a = e6[s];
  o ? e6[h] >> 14 < e6[Ne] >> 16 && (e6[h] & 3) === t && (e6[h] += 16384, aa(a, i)) : aa(a, i);
}
var et = -1;
var Nt = class {
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
function El(e6, t, n) {
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
      Il(i) ? e6.setProperty(t, i, s) : e6.setAttribute(t, i, s), r++;
    }
  }
  return r;
}
function Il(e6) {
  return e6.charCodeAt(0) === 64;
}
function oi(e6, t) {
  if (!(t === null || t.length === 0))
    if (e6 === null || e6.length === 0)
      e6 = t.slice();
    else {
      let n = -1;
      for (let r = 0; r < t.length; r++) {
        let o = t[r];
        typeof o == "number" ? n = o : n === 0 || (n === -1 || n === 2 ? ca(e6, n, o, null, t[++r]) : ca(e6, n, o, null, null));
      }
    }
  return e6;
}
function ca(e6, t, n, r, o) {
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
function Cl(e6) {
  return e6 !== et;
}
function Oo(e6) {
  return e6 & 32767;
}
function wl(e6) {
  return e6 >> 16;
}
function ko(e6, t) {
  let n = wl(e6), r = t;
  for (; n > 0; )
    r = r[We], n--;
  return r;
}
var Fo = true;
function ua(e6) {
  let t = Fo;
  return Fo = e6, t;
}
var Tl = 256;
var Oa = Tl - 1;
var ka = 5;
var Ml = 0;
var K = {};
function _l(e6, t, n) {
  let r;
  typeof n == "string" ? r = n.charCodeAt(0) || 0 : n.hasOwnProperty(Me) && (r = n[Me]), r == null && (r = n[Me] = Ml++);
  let o = r & Oa, i = 1 << o;
  t.data[e6 + (o >> ka)] |= i;
}
function Fa(e6, t) {
  let n = La(e6, t);
  if (n !== -1)
    return n;
  let r = t[y];
  r.firstCreatePass && (e6.injectorIndex = t.length, xo(r.data, e6), xo(t, null), xo(r.blueprint, null));
  let o = Pa(e6, t), i = e6.injectorIndex;
  if (Cl(o)) {
    let s = Oo(o), a = ko(o, t), c = a[y].data;
    for (let u = 0; u < 8; u++)
      t[i + u] = a[s + u] | c[s + u];
  }
  return t[i + 8] = o, i;
}
function xo(e6, t) {
  e6.push(0, 0, 0, 0, 0, 0, 0, 0, t);
}
function La(e6, t) {
  return e6.injectorIndex === -1 || e6.parent && e6.parent.injectorIndex === e6.injectorIndex || t[e6.injectorIndex + 8] === null ? -1 : e6.injectorIndex;
}
function Pa(e6, t) {
  if (e6.parent && e6.parent.injectorIndex !== -1)
    return e6.parent.injectorIndex;
  let n = 0, r = null, o = t;
  for (; o !== null; ) {
    if (r = $a(o), r === null)
      return et;
    if (n++, o = o[We], r.injectorIndex !== -1)
      return r.injectorIndex | n << 16;
  }
  return et;
}
function Sl(e6, t, n) {
  _l(e6, t, n);
}
function ja(e6, t, n) {
  if (n & 8 || e6 !== void 0)
    return e6;
  hn(t, "NodeInjector");
}
function Ba(e6, t, n, r) {
  if (n & 8 && r === void 0 && (r = null), (n & 3) === 0) {
    let o = e6[be], i = R(void 0);
    try {
      return o ? o.get(t, r, n & 8) : Xr(t, r, n & 8);
    } finally {
      R(i);
    }
  }
  return ja(r, t, n);
}
function Va(e6, t, n, r = 0, o) {
  if (e6 !== null) {
    if (t[h] & 2048 && !(r & 2)) {
      let s = Rl(e6, t, n, r, K);
      if (s !== K)
        return s;
    }
    let i = Ha(e6, t, n, r, K);
    if (i !== K)
      return i;
  }
  return Ba(t, n, r, o);
}
function Ha(e6, t, n, r, o) {
  let i = Al(n);
  if (typeof i == "function") {
    if (!Eo(t, e6, r))
      return r & 1 ? ja(o, n, r) : Ba(t, n, r, o);
    try {
      let s;
      if (s = i(r), s == null && !(r & 8))
        hn(n);
      else
        return s;
    } finally {
      Io();
    }
  } else if (typeof i == "number") {
    let s = null, a = La(e6, t), c = et, u = r & 1 ? t[Q][oe] : null;
    for ((a === -1 || r & 4) && (c = a === -1 ? Pa(e6, t) : t[a + 8], c === et || !da(r, false) ? a = -1 : (s = t[y], a = Oo(c), t = ko(c, t))); a !== -1; ) {
      let l = t[y];
      if (la(i, a, l.data)) {
        let d = bl(a, t, n, s, r, u);
        if (d !== K)
          return d;
      }
      c = t[a + 8], c !== et && da(r, t[y].data[a + 8] === u) && la(i, a, t) ? (s = l, a = Oo(c), t = ko(c, t)) : a = -1;
    }
  }
  return o;
}
function bl(e6, t, n, r, o, i) {
  let s = t[y], a = s.data[e6 + 8], c = r == null ? vt(a) && Fo : r != s && (a.type & 3) !== 0, u = o & 1 && i === a, l = Nl(a, s, n, c, u);
  return l !== null ? Lo(t, s, l, a, o) : K;
}
function Nl(e6, t, n, r, o) {
  let i = e6.providerIndexes, s = t.data, a = i & 1048575, c = e6.directiveStart, u = e6.directiveEnd, l = i >> 20, d = r ? a : a + l, p = o ? a + l : u;
  for (let f = d; f < p; f++) {
    let T = s[f];
    if (f < c && n === T || f >= c && T.type === n)
      return f;
  }
  if (o) {
    let f = s[c];
    if (f && Ze(f) && f.type === n)
      return c;
  }
  return null;
}
function Lo(e6, t, n, r, o) {
  let i = e6[n], s = t.data;
  if (i instanceof Nt) {
    let a = i;
    if (a.resolving)
      throw Jr("");
    let c = ua(a.canSeeViewProviders);
    a.resolving = true;
    let u = s[n].type || s[n], l, d = a.injectImpl ? R(a.injectImpl) : null, p = Eo(e6, r, 0);
    try {
      i = e6[n] = a.factory(void 0, o, s, e6, r), t.firstCreatePass && n >= r.directiveStart && yl(n, s[n], t);
    } finally {
      d !== null && R(d), ua(c), a.resolving = false, Io();
    }
  }
  return i;
}
function Al(e6) {
  if (typeof e6 == "string")
    return e6.charCodeAt(0) || 0;
  let t = e6.hasOwnProperty(Me) ? e6[Me] : void 0;
  return typeof t == "number" ? t >= 0 ? t & Oa : xl : t;
}
function la(e6, t, n) {
  let r = 1 << e6;
  return !!(n[t + (e6 >> ka)] & r);
}
function da(e6, t) {
  return !(e6 & 2) && !(e6 & 1 && t);
}
var Ln = class {
  _tNode;
  _lView;
  constructor(t, n) {
    this._tNode = t, this._lView = n;
  }
  get(t, n, r) {
    return Va(this._tNode, this._lView, t, Ce(r), n);
  }
};
function xl() {
  return new Ln(Qe(), B());
}
function Rl(e6, t, n, r, o) {
  let i = e6, s = t;
  for (; i !== null && s !== null && s[h] & 2048 && !Ye(s); ) {
    let a = Ha(i, s, n, r | 2, K);
    if (a !== K)
      return a;
    let c = i.parent;
    if (!c) {
      let u = s[so];
      if (u) {
        let l = u.get(n, K, r & -5);
        if (l !== K)
          return l;
      }
      c = $a(s), s = s[We];
    }
    i = c;
  }
  return o;
}
function $a(e6) {
  let t = e6[y], n = t.type;
  return n === 2 ? t.declTNode : n === 1 ? e6[oe] : null;
}
function Ol() {
  return Ua(Qe(), B());
}
function Ua(e6, t) {
  return new ii(xe(e6, t));
}
var ii = /* @__PURE__ */ (() => {
  class e6 {
    nativeElement;
    constructor(n) {
      this.nativeElement = n;
    }
    static __NG_ELEMENT_ID__ = Ol;
  }
  return e6;
})();
function kl(e6) {
  return (e6.flags & 128) === 128;
}
var si = function(e6) {
  return e6[e6.OnPush = 0] = "OnPush", e6[e6.Eager = 1] = "Eager", e6[e6.Default = 1] = "Default", e6;
}(si || {});
var za = /* @__PURE__ */ new Map();
var Fl = 0;
function Ll() {
  return Fl++;
}
function Pl(e6) {
  za.set(e6[le], e6);
}
function Po(e6) {
  za.delete(e6[le]);
}
var fa = "__ngContext__";
function At(e6, t) {
  de(t) ? (e6[fa] = t[le], Pl(t)) : e6[fa] = t;
}
function Ga(e6) {
  return qa(e6[Ge]);
}
function Wa(e6) {
  return qa(e6[re]);
}
function qa(e6) {
  for (; e6 !== null && !fe(e6); )
    e6 = e6[re];
  return e6;
}
var jo;
function ai(e6) {
  jo = e6;
}
function Za() {
  if (jo !== void 0)
    return jo;
  if (typeof document < "u")
    return document;
  throw new g(210, false);
}
var $n = new m("", { factory: () => jl });
var jl = "ng";
var Un = new m("");
var Ot = new m("", { providedIn: "platform", factory: () => "unknown" });
var zn = new m("", { factory: () => v(A).body?.querySelector("[ngCspNonce]")?.getAttribute("ngCspNonce") || null });
var Ya = false;
var Qa = new m("", { factory: () => Ya });
function ci(e6) {
  return (e6.flags & 32) === 32;
}
var Bl = () => null;
function Ka(e6, t, n = false) {
  return Bl(e6, t, n);
}
function Ja(e6, t) {
  let n = e6.contentQueries;
  if (n !== null) {
    let r = D(null);
    try {
      for (let o = 0; o < n.length; o += 2) {
        let i = n[o], s = n[o + 1];
        if (s !== -1) {
          let a = e6.data[s];
          vo(i), a.contentQueries(2, t[s], s);
        }
      }
    } finally {
      D(r);
    }
  }
}
function Bo(e6, t, n) {
  vo(0);
  let r = D(null);
  try {
    t(e6, n);
  } finally {
    D(r);
  }
}
function Vl(e6, t, n) {
  if (ao(t)) {
    let r = D(null);
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
      D(r);
    }
  }
}
var G = function(e6) {
  return e6[e6.Emulated = 0] = "Emulated", e6[e6.None = 2] = "None", e6[e6.ShadowDom = 3] = "ShadowDom", e6[e6.ExperimentalIsolatedShadowDom = 4] = "ExperimentalIsolatedShadowDom", e6;
}(G || {});
var Nn;
function Hl() {
  if (Nn === void 0 && (Nn = null, ue.trustedTypes))
    try {
      Nn = ue.trustedTypes.createPolicy("angular", { createHTML: (e6) => e6, createScript: (e6) => e6, createScriptURL: (e6) => e6 });
    } catch {
    }
  return Nn;
}
function Gn(e6) {
  return Hl()?.createHTML(e6) || e6;
}
var An;
function $l() {
  if (An === void 0 && (An = null, ue.trustedTypes))
    try {
      An = ue.trustedTypes.createPolicy("angular#unsafe-bypass", { createHTML: (e6) => e6, createScript: (e6) => e6, createScriptURL: (e6) => e6 });
    } catch {
    }
  return An;
}
function pa(e6) {
  return $l()?.createHTML(e6) || e6;
}
var se = class {
  changingThisBreaksApplicationSecurity;
  constructor(t) {
    this.changingThisBreaksApplicationSecurity = t;
  }
  toString() {
    return `SafeValue must use [property]=binding: ${this.changingThisBreaksApplicationSecurity} (see ${un})`;
  }
};
var Vo = class extends se {
  getTypeName() {
    return "HTML";
  }
};
var Ho = class extends se {
  getTypeName() {
    return "Style";
  }
};
var $o = class extends se {
  getTypeName() {
    return "Script";
  }
};
var Uo = class extends se {
  getTypeName() {
    return "URL";
  }
};
var zo = class extends se {
  getTypeName() {
    return "ResourceURL";
  }
};
function me(e6) {
  return e6 instanceof se ? e6.changingThisBreaksApplicationSecurity : e6;
}
function ye(e6, t) {
  let n = Xa(e6);
  if (n != null && n !== t) {
    if (n === "ResourceURL" && t === "URL")
      return true;
    throw new Error(`Required a safe ${t}, got a ${n} (see ${un})`);
  }
  return n === t;
}
function Xa(e6) {
  return e6 instanceof se && e6.getTypeName() || null;
}
function ui(e6) {
  return new Vo(e6);
}
function li(e6) {
  return new Ho(e6);
}
function di(e6) {
  return new $o(e6);
}
function fi(e6) {
  return new Uo(e6);
}
function pi(e6) {
  return new zo(e6);
}
function Ul(e6) {
  let t = new Wo(e6);
  return zl() ? new Go(t) : t;
}
var Go = class {
  inertDocumentHelper;
  constructor(t) {
    this.inertDocumentHelper = t;
  }
  getInertBodyElement(t) {
    t = "<body><remove></remove>" + t;
    try {
      let n = new window.DOMParser().parseFromString(Gn(t), "text/html").body;
      return n === null ? this.inertDocumentHelper.getInertBodyElement(t) : (n.firstChild?.remove(), n);
    } catch {
      return null;
    }
  }
};
var Wo = class {
  defaultDoc;
  inertDocument;
  constructor(t) {
    this.defaultDoc = t, this.inertDocument = this.defaultDoc.implementation.createHTMLDocument("sanitization-inert");
  }
  getInertBodyElement(t) {
    let n = this.inertDocument.createElement("template");
    return n.innerHTML = Gn(t), n;
  }
};
function zl() {
  try {
    return !!new window.DOMParser().parseFromString(Gn(""), "text/html");
  } catch {
    return false;
  }
}
var Gl = /^(?!javascript:)(?:[a-z0-9+.-]+:|[^&:\/?#]*(?:[\/?#]|$))/i;
function Wn(e6) {
  return e6 = String(e6), e6.match(Gl) ? e6 : "unsafe:" + e6;
}
function ae(e6) {
  let t = {};
  for (let n of e6.split(","))
    t[n] = true;
  return t;
}
function kt(...e6) {
  let t = {};
  for (let n of e6)
    for (let r in n)
      n.hasOwnProperty(r) && (t[r] = true);
  return t;
}
var ec = ae("area,br,col,hr,img,wbr");
var tc = ae("colgroup,dd,dt,li,p,tbody,td,tfoot,th,thead,tr");
var nc = ae("rp,rt");
var Wl = kt(nc, tc);
var ql = kt(tc, ae("address,article,aside,blockquote,caption,center,del,details,dialog,dir,div,dl,figure,figcaption,footer,h1,h2,h3,h4,h5,h6,header,hgroup,hr,ins,main,map,menu,nav,ol,pre,section,summary,table,ul"));
var Zl = kt(nc, ae("a,abbr,acronym,audio,b,bdi,bdo,big,br,cite,code,del,dfn,em,font,i,img,ins,kbd,label,map,mark,picture,q,ruby,rp,rt,s,samp,small,source,span,strike,strong,sub,sup,time,track,tt,u,var,video"));
var ha = kt(ec, ql, Zl, Wl);
var rc = ae("background,cite,href,itemtype,longdesc,poster,src,xlink:href");
var Yl = ae("abbr,accesskey,align,alt,autoplay,axis,bgcolor,border,cellpadding,cellspacing,class,clear,color,cols,colspan,compact,controls,coords,datetime,default,dir,download,face,headers,height,hidden,hreflang,hspace,ismap,itemscope,itemprop,kind,label,lang,language,loop,media,muted,nohref,nowrap,open,preload,rel,rev,role,rows,rowspan,rules,scope,scrolling,shape,size,sizes,span,srclang,srcset,start,summary,tabindex,target,title,translate,type,usemap,valign,value,vspace,width");
var Ql = ae("aria-activedescendant,aria-atomic,aria-autocomplete,aria-busy,aria-checked,aria-colcount,aria-colindex,aria-colspan,aria-controls,aria-current,aria-describedby,aria-details,aria-disabled,aria-dropeffect,aria-errormessage,aria-expanded,aria-flowto,aria-grabbed,aria-haspopup,aria-hidden,aria-invalid,aria-keyshortcuts,aria-label,aria-labelledby,aria-level,aria-live,aria-modal,aria-multiline,aria-multiselectable,aria-orientation,aria-owns,aria-placeholder,aria-posinset,aria-pressed,aria-readonly,aria-relevant,aria-required,aria-roledescription,aria-rowcount,aria-rowindex,aria-rowspan,aria-selected,aria-setsize,aria-sort,aria-valuemax,aria-valuemin,aria-valuenow,aria-valuetext");
var Kl = kt(rc, Yl, Ql);
var Jl = ae("script,style,template");
var qo = class {
  sanitizedSomething = false;
  buf = [];
  sanitizeChildren(t) {
    let n = t.firstChild, r = true, o = [];
    for (; n; ) {
      if (n.nodeType === Node.ELEMENT_NODE ? r = this.startElement(n) : n.nodeType === Node.TEXT_NODE ? this.chars(n.nodeValue) : this.sanitizedSomething = true, r && n.firstChild) {
        o.push(n), n = td(n);
        continue;
      }
      for (; n; ) {
        n.nodeType === Node.ELEMENT_NODE && this.endElement(n);
        let i = ed(n);
        if (i) {
          n = i;
          break;
        }
        n = o.pop();
      }
    }
    return this.buf.join("");
  }
  startElement(t) {
    let n = ga(t).toLowerCase();
    if (!ha.hasOwnProperty(n))
      return this.sanitizedSomething = true, !Jl.hasOwnProperty(n);
    this.buf.push("<"), this.buf.push(n);
    let r = t.attributes;
    for (let o = 0; o < r.length; o++) {
      let i = r.item(o), s = i.name, a = s.toLowerCase();
      if (!Kl.hasOwnProperty(a)) {
        this.sanitizedSomething = true;
        continue;
      }
      let c = i.value;
      rc[a] && (c = Wn(c)), this.buf.push(" ", s, '="', ma(c), '"');
    }
    return this.buf.push(">"), true;
  }
  endElement(t) {
    let n = ga(t).toLowerCase();
    ha.hasOwnProperty(n) && !ec.hasOwnProperty(n) && (this.buf.push("</"), this.buf.push(n), this.buf.push(">"));
  }
  chars(t) {
    this.buf.push(ma(t));
  }
};
function Xl(e6, t) {
  return (e6.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_CONTAINED_BY) !== Node.DOCUMENT_POSITION_CONTAINED_BY;
}
function ed(e6) {
  let t = e6.nextSibling;
  if (t && e6 !== t.previousSibling)
    throw oc(t);
  return t;
}
function td(e6) {
  let t = e6.firstChild;
  if (t && Xl(e6, t))
    throw oc(t);
  return t;
}
function ga(e6) {
  let t = e6.nodeName;
  return typeof t == "string" ? t : "FORM";
}
function oc(e6) {
  return new Error(`Failed to sanitize html because the element is clobbered: ${e6.outerHTML}`);
}
var nd = /[\uD800-\uDBFF][\uDC00-\uDFFF]/g;
var rd = /([^\#-~ |!])/g;
function ma(e6) {
  return e6.replace(/&/g, "&amp;").replace(nd, function(t) {
    let n = t.charCodeAt(0), r = t.charCodeAt(1);
    return "&#" + ((n - 55296) * 1024 + (r - 56320) + 65536) + ";";
  }).replace(rd, function(t) {
    return "&#" + t.charCodeAt(0) + ";";
  }).replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
var xn;
function qn(e6, t) {
  let n = null;
  try {
    xn = xn || Ul(e6);
    let r = t ? String(t) : "";
    n = xn.getInertBodyElement(r);
    let o = 5, i = r;
    do {
      if (o === 0)
        throw new Error("Failed to sanitize html because the input is unstable");
      o--, r = i, i = n.innerHTML, n = xn.getInertBodyElement(r);
    } while (r !== i);
    let a = new qo().sanitizeChildren(ya(n) || n);
    return Gn(a);
  } finally {
    if (n) {
      let r = ya(n) || n;
      for (; r.firstChild; )
        r.firstChild.remove();
    }
  }
}
function ya(e6) {
  return "content" in e6 && od(e6) ? e6.content : null;
}
function od(e6) {
  return e6.nodeType === Node.ELEMENT_NODE && e6.nodeName === "TEMPLATE";
}
function id(e6, t) {
  return e6.createText(t);
}
function sd(e6, t, n) {
  e6.setValue(t, n);
}
function ic(e6, t, n) {
  return e6.createElement(t, n);
}
function Zo(e6, t, n, r, o) {
  e6.insertBefore(t, n, r, o);
}
function sc(e6, t, n) {
  e6.appendChild(t, n);
}
function Da(e6, t, n, r, o) {
  r !== null ? Zo(e6, t, n, r, o) : sc(e6, t, n);
}
function ad(e6, t, n, r) {
  e6.removeChild(null, t, n, r);
}
function cd(e6, t, n) {
  e6.setAttribute(t, "style", n);
}
function ud(e6, t, n) {
  n === "" ? e6.removeAttribute(t, "class") : e6.setAttribute(t, "class", n);
}
function ac(e6, t, n) {
  let { mergedAttrs: r, classes: o, styles: i } = n;
  r !== null && El(e6, t, r), o !== null && ud(e6, t, o), i !== null && cd(e6, t, i);
}
var J = function(e6) {
  return e6[e6.NONE = 0] = "NONE", e6[e6.HTML = 1] = "HTML", e6[e6.STYLE = 2] = "STYLE", e6[e6.SCRIPT = 3] = "SCRIPT", e6[e6.URL = 4] = "URL", e6[e6.RESOURCE_URL = 5] = "RESOURCE_URL", e6;
}(J || {});
function hi(e6) {
  let t = ld();
  return t ? pa(t.sanitize(J.HTML, e6) || "") : ye(e6, "HTML") ? pa(me(e6)) : qn(Za(), Kr(e6));
}
function ld() {
  let e6 = B();
  return e6 && e6[Y].sanitizer;
}
var dd = "ng-template";
function fd(e6) {
  return e6.type === 4 && e6.value !== dd;
}
function Yo(e6) {
  return (e6 & 1) === 0;
}
function va(e6, t) {
  return e6 ? ":not(" + t.trim() + ")" : t;
}
function pd(e6) {
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
      o !== "" && !Yo(s) && (t += va(i, o), o = ""), r = s, i = i || !Yo(r);
    n++;
  }
  return o !== "" && (t += va(i, o)), t;
}
function hd(e6) {
  return e6.map(pd).join(",");
}
function gd(e6) {
  let t = [], n = [], r = 1, o = 2;
  for (; r < e6.length; ) {
    let i = e6[r];
    if (typeof i == "string")
      o === 2 ? i !== "" && t.push(i, e6[++r]) : o === 8 && n.push(i);
    else {
      if (!Yo(o))
        break;
      o = i;
    }
    r++;
  }
  return n.length && t.push(1, ...n), t;
}
var nt = {};
function cc(e6, t, n, r, o, i, s, a, c, u, l) {
  let d = z + r, p = d + o, f = md(d, p), T = typeof u == "function" ? u() : u;
  return f[y] = { type: e6, blueprint: f, template: n, queries: null, viewQuery: a, declTNode: t, data: f.slice().fill(null, d), bindingStartIndex: d, expandoStartIndex: p, hostBindingOpCodes: null, firstCreatePass: true, firstUpdatePass: true, staticViewQueries: false, staticContentQueries: false, preOrderHooks: null, preOrderCheckHooks: null, contentHooks: null, contentCheckHooks: null, viewHooks: null, viewCheckHooks: null, destroyHooks: null, cleanup: null, contentQueries: null, components: null, directiveRegistry: typeof i == "function" ? i() : i, pipeRegistry: typeof s == "function" ? s() : s, firstChild: null, schemas: c, consts: T, incompleteFirstPass: false, ssrId: l };
}
function md(e6, t) {
  let n = [];
  for (let r = 0; r < t; r++)
    n.push(r < e6 ? null : nt);
  return n;
}
function yd(e6) {
  let t = e6.tView;
  return t === null || t.incompleteFirstPass ? e6.tView = cc(1, null, e6.template, e6.decls, e6.vars, e6.directiveDefs, e6.pipeDefs, e6.viewQuery, e6.schemas, e6.consts, e6.id) : t;
}
function uc(e6, t, n, r, o, i, s, a, c, u, l) {
  let d = t.blueprint.slice();
  return d[Z] = o, d[h] = r | 4 | 128 | 8 | 64 | 1024, (u !== null || e6 && e6[h] & 2048) && (d[h] |= 2048), uo(d), d[k] = d[We] = e6, d[F] = n, d[Y] = s || e6 && e6[Y], d[L] = a || e6 && e6[L], d[be] = c || e6 && e6[be] || null, d[oe] = i, d[le] = Ll(), d[yn] = l, d[so] = u, d[Q] = t.type == 2 ? e6[Q] : d, d;
}
function Dd(e6, t, n) {
  let r = xe(t, e6), o = yd(n), i = e6[Y].rendererFactory, s = vd(e6, uc(e6, o, null, lc(n), r, t, null, i.createRenderer(r, n), null, null, null));
  return e6[t.index] = s;
}
function lc(e6) {
  let t = 16;
  return e6.signals ? t = 4096 : e6.onPush && (t = 64), t;
}
function dc(e6, t, n, r) {
  if (n === 0)
    return -1;
  let o = t.length;
  for (let i = 0; i < n; i++)
    t.push(r), e6.blueprint.push(r), e6.data.push(null);
  return o;
}
function vd(e6, t) {
  return e6[Ge] ? e6[io][re] = t : e6[Ge] = t, e6[io] = t, t;
}
function Zn(e6 = 1) {
  fc(Tn(), B(), bn() + e6, false);
}
function fc(e6, t, n, r) {
  if (!r)
    if ((t[h] & 3) === 3) {
      let i = e6.preOrderCheckHooks;
      i !== null && Rn(t, i, n);
    } else {
      let i = e6.preOrderHooks;
      i !== null && On(t, i, 0, n);
    }
  ge(n);
}
var Yn = function(e6) {
  return e6[e6.None = 0] = "None", e6[e6.SignalBased = 1] = "SignalBased", e6[e6.HasDecoratorInputTransform = 2] = "HasDecoratorInputTransform", e6;
}(Yn || {});
function Qo(e6, t, n, r) {
  let o = D(null);
  try {
    let [i, s, a] = e6.inputs[n], c = null;
    (s & Yn.SignalBased) !== 0 && (c = t[i][W]), c !== null && c.transformFn !== void 0 ? r = c.transformFn(r) : a !== null && (r = a.call(t, r)), e6.setInput !== null ? e6.setInput(t, c, r, n, i) : Na(t, c, i, r);
  } finally {
    D(o);
  }
}
var Oe = function(e6) {
  return e6[e6.Important = 1] = "Important", e6[e6.DashCase = 2] = "DashCase", e6;
}(Oe || {});
var Ed;
function pc(e6, t) {
  return Ed(e6, t);
}
var dy = typeof document < "u" && typeof document?.documentElement?.getAnimations == "function";
var Ko = /* @__PURE__ */ new WeakMap();
var St = /* @__PURE__ */ new WeakSet();
function Id(e6, t) {
  let n = Ko.get(e6);
  if (!n || n.length === 0)
    return;
  let r = t.parentNode, o = t.previousSibling;
  for (let i = n.length - 1; i >= 0; i--) {
    let s = n[i], a = s.parentNode;
    s === t ? (n.splice(i, 1), St.add(s), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } }))) : (o && s === o || a && r && a !== r) && (n.splice(i, 1), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } })), s.parentNode?.removeChild(s));
  }
}
function Cd(e6, t) {
  let n = Ko.get(e6);
  n ? n.includes(t) || n.push(t) : Ko.set(e6, [t]);
}
var tt = /* @__PURE__ */ new Set();
var gi = function(e6) {
  return e6[e6.CHANGE_DETECTION = 0] = "CHANGE_DETECTION", e6[e6.AFTER_NEXT_RENDER = 1] = "AFTER_NEXT_RENDER", e6;
}(gi || {});
var rt = new m("");
var Ea = /* @__PURE__ */ new Set();
function hc(e6) {
  Ea.has(e6) || (Ea.add(e6), performance?.mark?.("mark_feature_usage", { detail: { feature: e6 } }));
}
var gc = (() => {
  class e6 {
    impl = null;
    execute() {
      this.impl?.execute();
    }
    static \u0275prov = _({ token: e6, providedIn: "root", factory: () => new e6() });
  }
  return e6;
})();
var wd = new m("", { factory: () => ({ queue: /* @__PURE__ */ new Set(), isScheduled: false, scheduler: null, injector: v(U) }) });
function mc(e6, t, n) {
  let r = e6.get(wd);
  if (Array.isArray(t))
    for (let o of t)
      r.queue.add(o), n?.detachedLeaveAnimationFns?.push(o);
  else
    r.queue.add(t), n?.detachedLeaveAnimationFns?.push(t);
  r.scheduler && r.scheduler(e6);
}
function Td(e6, t) {
  for (let [n, r] of t)
    mc(e6, r.animateFns);
}
function Ia(e6, t, n, r) {
  let o = e6?.[qe]?.enter;
  t !== null && o && o.has(n.index) && Td(r, o);
}
function Xe(e6, t, n, r, o, i, s, a) {
  if (o != null) {
    let c, u = false;
    fe(o) ? c = o : de(o) && (u = true, o = o[Z]);
    let l = pe(o);
    e6 === 0 && r !== null ? (Ia(a, r, i, n), s == null ? sc(t, r, l) : Zo(t, r, l, s || null, true)) : e6 === 1 && r !== null ? (Ia(a, r, i, n), Zo(t, r, l, s || null, true), Id(i, l)) : e6 === 2 ? (a?.[qe]?.leave?.has(i.index) && Cd(i, l), St.delete(l), Ca(a, i, n, (d) => {
      if (St.has(l)) {
        St.delete(l);
        return;
      }
      ad(t, l, u, d);
    })) : e6 === 3 && (St.delete(l), Ca(a, i, n, () => {
      t.destroyNode(l);
    })), c != null && jd(t, e6, n, c, i, r, s);
  }
}
function Md(e6, t) {
  yc(e6, t), t[Z] = null, t[oe] = null;
}
function yc(e6, t) {
  t[Y].changeDetectionScheduler?.notify(9), Di(e6, t, t[L], 2, null, null);
}
function _d(e6) {
  let t = e6[Ge];
  if (!t)
    return Ro(e6[y], e6);
  for (; t; ) {
    let n = null;
    if (de(t))
      n = t[Ge];
    else {
      let r = t[ie];
      r && (n = r);
    }
    if (!n) {
      for (; t && !t[re] && t !== e6; )
        de(t) && Ro(t[y], t), t = t[k];
      t === null && (t = e6), de(t) && Ro(t[y], t), n = t && t[re];
    }
    t = n;
  }
}
function mi(e6, t) {
  let n = e6[Dt], r = n.indexOf(t);
  n.splice(r, 1);
}
function Sd(e6, t) {
  if (Ae(t))
    return;
  let n = t[L];
  n.destroyNode && Di(e6, t, n, 3, null, null), _d(t);
}
function Ro(e6, t) {
  if (Ae(t))
    return;
  let n = D(null);
  try {
    t[h] &= -129, t[h] |= 256, t[P] && Qt(t[P]), Ad(e6, t), Nd(e6, t), t[y].type === 1 && t[L].destroy();
    let r = t[mt];
    if (r !== null && fe(t[k])) {
      r !== t[k] && mi(r, t);
      let o = t[vn];
      o !== null && o.detachView(e6);
    }
    Po(t);
  } finally {
    D(n);
  }
}
function Ca(e6, t, n, r) {
  let o = e6?.[qe];
  if (o == null || o.leave == null || !o.leave.has(t.index))
    return r(false);
  e6 && tt.add(e6[le]), mc(n, () => {
    if (o.leave && o.leave.has(t.index)) {
      let s = o.leave.get(t.index), a = [];
      if (s) {
        for (let c = 0; c < s.animateFns.length; c++) {
          let u = s.animateFns[c], { promise: l } = u();
          a.push(l);
        }
        o.detachedLeaveAnimationFns = void 0;
      }
      o.running = Promise.allSettled(a), bd(e6, r);
    } else
      e6 && tt.delete(e6[le]), r(false);
  }, o);
}
function bd(e6, t) {
  let n = e6[qe]?.running;
  if (n) {
    n.then(() => {
      e6[qe].running = void 0, tt.delete(e6[le]), t(true);
    });
    return;
  }
  t(false);
}
function Nd(e6, t) {
  let n = e6.cleanup, r = t[Dn];
  if (n !== null)
    for (let s = 0; s < n.length - 1; s += 2)
      if (typeof n[s] == "string") {
        let a = n[s + 3];
        a >= 0 ? r[a]() : r[-a].unsubscribe(), s += 2;
      } else {
        let a = r[n[s + 1]];
        n[s].call(a);
      }
  r !== null && (t[Dn] = null);
  let o = t[ee];
  if (o !== null) {
    t[ee] = null;
    for (let s = 0; s < o.length; s++) {
      let a = o[s];
      a();
    }
  }
  let i = t[yt];
  if (i !== null) {
    t[yt] = null;
    for (let s of i)
      s.destroy();
  }
}
function Ad(e6, t) {
  let n;
  if (e6 != null && (n = e6.destroyHooks) != null)
    for (let r = 0; r < n.length; r += 2) {
      let o = t[n[r]];
      if (!(o instanceof Nt)) {
        let i = n[r + 1];
        if (Array.isArray(i))
          for (let s = 0; s < i.length; s += 2) {
            let a = o[i[s]], c = i[s + 1];
            M(C.LifecycleHookStart, a, c);
            try {
              c.call(a);
            } finally {
              M(C.LifecycleHookEnd, a, c);
            }
          }
        else {
          M(C.LifecycleHookStart, o, i);
          try {
            i.call(o);
          } finally {
            M(C.LifecycleHookEnd, o, i);
          }
        }
      }
    }
}
function xd(e6, t, n) {
  return Rd(e6, t.parent, n);
}
function Rd(e6, t, n) {
  let r = t;
  for (; r !== null && r.type & 168; )
    t = r, r = t.parent;
  if (r === null)
    return n[Z];
  if (vt(r)) {
    let { encapsulation: o } = e6.data[r.directiveStart + r.componentOffset];
    if (o === G.None || o === G.Emulated)
      return null;
  }
  return xe(r, n);
}
function Od(e6, t, n) {
  return Fd(e6, t, n);
}
function kd(e6, t, n) {
  return e6.type & 40 ? xe(e6, n) : null;
}
var Fd = kd;
var wa;
function Dc(e6, t, n, r) {
  let o = xd(e6, r, t), i = t[L], s = r.parent || t[oe], a = Od(s, r, t);
  if (o != null)
    if (Array.isArray(n))
      for (let c = 0; c < n.length; c++)
        Da(i, o, n[c], a, false);
    else
      Da(i, o, n, a, false);
  wa !== void 0 && wa(i, r, t, n, o);
}
function Ld(e6, t) {
  if (t !== null) {
    let r = e6[Q][oe], o = t.projection;
    return r.projection[o];
  }
  return null;
}
function yi(e6, t, n, r, o, i, s) {
  for (; n != null; ) {
    let a = r[be];
    if (n.type === 128) {
      n = n.next;
      continue;
    }
    let c = r[n.index], u = n.type;
    if (s && t === 0 && (c && At(pe(c), r), n.flags |= 2), !ci(n))
      if (u & 8)
        yi(e6, t, n.child, r, o, i, false), Xe(t, e6, a, o, c, n, i, r);
      else if (u & 32) {
        let l = pc(n, r), d;
        for (; d = l(); )
          Xe(t, e6, a, o, d, n, i, r);
        Xe(t, e6, a, o, c, n, i, r);
      } else
        u & 16 ? Pd(e6, t, r, n, o, i) : Xe(t, e6, a, o, c, n, i, r);
    n = s ? n.projectionNext : n.next;
  }
}
function Di(e6, t, n, r, o, i) {
  yi(n, r, e6.firstChild, t, o, i, false);
}
function Pd(e6, t, n, r, o, i) {
  let s = n[Q], c = s[oe].projection[r.projection];
  if (Array.isArray(c))
    for (let u = 0; u < c.length; u++) {
      let l = c[u];
      Xe(t, e6, n[be], o, l, r, i, n);
    }
  else {
    let u = c, l = s[k];
    kl(r) && (u.flags |= 128), yi(e6, t, u, l, o, i, true);
  }
}
function jd(e6, t, n, r, o, i, s) {
  let a = r[Cn], c = pe(r);
  a !== c && Xe(t, e6, n, i, a, o, s);
  for (let u = ie; u < r.length; u++) {
    let l = r[u];
    Di(l[y], l, e6, t, i, a);
  }
}
function vc(e6, t, n, r, o) {
  let i = bn(), s = r & 2;
  try {
    ge(-1), s && t.length > z && fc(e6, t, z, false);
    let a = s ? C.TemplateUpdateStart : C.TemplateCreateStart;
    M(a, o, n), n(r, o);
  } finally {
    ge(i);
    let a = s ? C.TemplateUpdateEnd : C.TemplateCreateEnd;
    M(a, o, n);
  }
}
function Bd(e6, t, n) {
  Gd(e6, t, n), (n.flags & 64) === 64 && Wd(e6, t, n);
}
function Vd(e6, t, n = xe) {
  let r = t.localNames;
  if (r !== null) {
    let o = t.index + 1;
    for (let i = 0; i < r.length; i += 2) {
      let s = r[i + 1], a = s === -1 ? n(t, e6) : e6[s];
      e6[o++] = a;
    }
  }
}
function Hd(e6, t, n, r) {
  let i = r.get(Qa, Ya) || n === G.ShadowDom || n === G.ExperimentalIsolatedShadowDom, s = e6.selectRootElement(t, i);
  return $d(s), s;
}
function $d(e6) {
  Ud(e6);
}
var Ud = () => null;
function zd(e6, t, n, r, o, i) {
  if (e6.type & 3) {
    let s = xe(e6, t);
    r = i != null ? i(r, e6.value || "", n) : r, o.setProperty(s, n, r);
  } else
    e6.type & 12;
}
function Gd(e6, t, n) {
  let r = n.directiveStart, o = n.directiveEnd;
  vt(n) && Dd(t, n, e6.data[r + n.componentOffset]), e6.firstCreatePass || Fa(n, t);
  let i = n.initialInputs;
  for (let s = r; s < o; s++) {
    let a = e6.data[s], c = Lo(t, e6, s, n);
    if (At(c, t), i !== null && Zd(t, s - r, c, a, n, i), Ze(a)) {
      let u = he(n.index, t);
      u[F] = Lo(t, e6, s, n);
    }
  }
}
function Wd(e6, t, n) {
  let r = n.directiveStart, o = n.directiveEnd, i = n.index, s = Ws();
  try {
    ge(i);
    for (let a = r; a < o; a++) {
      let c = e6.data[a], u = t[a];
      Mn(a), (c.hostBindings !== null || c.hostVars !== 0 || c.hostAttrs !== null) && qd(c, u);
    }
  } finally {
    ge(-1), Mn(s);
  }
}
function qd(e6, t) {
  e6.hostBindings !== null && e6.hostBindings(1, t);
}
function Zd(e6, t, n, r, o, i) {
  let s = i[t];
  if (s !== null)
    for (let a = 0; a < s.length; a += 2) {
      let c = s[a], u = s[a + 1];
      Qo(r, n, c, u);
    }
}
function Yd(e6, t, n, r, o) {
  let i = z + n, s = t[y], a = o(s, t, e6, r, n);
  t[i] = a, wt(e6, true);
  let c = e6.type === 2;
  return c ? (ac(t[L], a, e6), (Fs() === 0 || As(e6)) && At(a, t), Ls()) : At(a, t), Co() && (!c || !ci(e6)) && Dc(s, t, a, e6), e6;
}
function Qd(e6) {
  let t = e6;
  return go() ? $s() : (t = t.parent, wt(t, false)), t;
}
function Kd(e6, t, n, r, o) {
  let i = e6.inputs?.[r], s = e6.hostDirectiveInputs?.[r], a = false;
  if (s)
    for (let c = 0; c < s.length; c += 2) {
      let u = s[c], l = s[c + 1], d = t.data[u];
      Qo(d, n[u], l, o), a = true;
    }
  if (i)
    for (let c of i) {
      let u = n[c], l = t.data[c];
      Qo(l, u, r, o), a = true;
    }
  return a;
}
function Jd(e6, t) {
  let n = he(t, e6), r = n[y];
  Xd(r, n);
  let o = n[Z];
  o !== null && n[yn] === null && (n[yn] = Ka(o, n[be])), M(C.ComponentStart);
  try {
    Ec(r, n, n[F]);
  } finally {
    M(C.ComponentEnd, n[F]);
  }
}
function Xd(e6, t) {
  for (let n = t.length; n < e6.blueprint.length; n++)
    t.push(e6.blueprint[n]);
}
function Ec(e6, t, n) {
  _n(t);
  try {
    let r = e6.viewQuery;
    r !== null && Bo(1, r, n);
    let o = e6.template;
    o !== null && vc(e6, t, o, 1, n), e6.firstCreatePass && (e6.firstCreatePass = false), t[vn]?.finishViewCreation(e6), e6.staticContentQueries && Ja(e6, t), e6.staticViewQueries && Bo(2, e6.viewQuery, n);
    let i = e6.components;
    i !== null && ef(t, i);
  } catch (r) {
    throw e6.firstCreatePass && (e6.incompleteFirstPass = true, e6.firstCreatePass = false), r;
  } finally {
    t[h] &= -5, Sn();
  }
}
function ef(e6, t) {
  for (let n = 0; n < t.length; n++)
    Jd(e6, t[n]);
}
function xt(e6, t, n, r, o = false) {
  for (; n !== null; ) {
    if (n.type === 128) {
      n = o ? n.projectionNext : n.next;
      continue;
    }
    let i = t[n.index];
    i !== null && r.push(pe(i)), fe(i) && Ic(i, r);
    let s = n.type;
    if (s & 8)
      xt(e6, t, n.child, r);
    else if (s & 32) {
      let a = pc(n, t), c;
      for (; c = a(); )
        r.push(c);
    } else if (s & 16) {
      let a = Ld(t, n);
      if (Array.isArray(a))
        r.push(...a);
      else {
        let c = Te(t[Q]);
        xt(c[y], c, a, r, true);
      }
    }
    n = o ? n.projectionNext : n.next;
  }
  return r;
}
function Ic(e6, t) {
  for (let n = ie; n < e6.length; n++) {
    let r = e6[n], o = r[y].firstChild;
    o !== null && xt(r[y], r, o, t);
  }
  e6[Cn] !== e6[Z] && t.push(e6[Cn]);
}
function Cc(e6) {
  if (e6[In] !== null) {
    for (let t of e6[In])
      t.impl.addSequence(t);
    e6[In].length = 0;
  }
}
var wc = [];
function tf(e6) {
  return e6[P] ?? nf(e6);
}
function nf(e6) {
  let t = wc.pop() ?? Object.create(of);
  return t.lView = e6, t;
}
function rf(e6) {
  e6.lView[P] !== e6 && (e6.lView = null, wc.push(e6));
}
var of = V(x({}, Yt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e6) => {
  Ct(e6.lView);
}, consumerOnSignalRead() {
  this.lView[P] = this;
} });
function sf(e6) {
  let t = e6[P] ?? Object.create(af);
  return t.lView = e6, t;
}
var af = V(x({}, Yt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e6) => {
  let t = Te(e6.lView);
  for (; t && !Tc(t[y]); )
    t = Te(t);
  t && lo(t);
}, consumerOnSignalRead() {
  this.lView[P] = this;
} });
function Tc(e6) {
  return e6.type !== 2;
}
function Mc(e6) {
  if (e6[yt] === null)
    return;
  let t = true;
  for (; t; ) {
    let n = false;
    for (let r of e6[yt])
      r.dirty && (n = true, r.zone === null || Zone.current === r.zone ? r.run() : r.zone.run(() => r.run()));
    t = n && !!(e6[h] & 8192);
  }
}
var cf = 100;
function _c(e6, t = 0) {
  let r = e6[Y].rendererFactory, o = false;
  o || r.begin?.();
  try {
    uf(e6, t);
  } finally {
    o || r.end?.();
  }
}
function uf(e6, t) {
  let n = mo();
  try {
    yo(true), Jo(e6, t);
    let r = 0;
    for (; It(e6); ) {
      if (r === cf)
        throw new g(103, false);
      r++, Jo(e6, 1);
    }
  } finally {
    yo(n);
  }
}
function lf(e6, t, n, r) {
  if (Ae(t))
    return;
  let o = t[h], i = false, s = false;
  _n(t);
  let a = true, c = null, u = null;
  i || (Tc(e6) ? (u = tf(t), c = hr(u)) : Zt() === null ? (a = false, u = sf(t), c = hr(u)) : t[P] && (Qt(t[P]), t[P] = null));
  try {
    uo(t), Us(e6.bindingStartIndex), n !== null && vc(e6, t, n, 2, r);
    let l = (o & 3) === 3;
    if (!i)
      if (l) {
        let f = e6.preOrderCheckHooks;
        f !== null && Rn(t, f, null);
      } else {
        let f = e6.preOrderHooks;
        f !== null && On(t, f, 0, null), Ao(t, 0);
      }
    if (s || df(t), Mc(t), Sc(t, 0), e6.contentQueries !== null && Ja(e6, t), !i)
      if (l) {
        let f = e6.contentCheckHooks;
        f !== null && Rn(t, f);
      } else {
        let f = e6.contentHooks;
        f !== null && On(t, f, 1), Ao(t, 1);
      }
    pf(e6, t);
    let d = e6.components;
    d !== null && Nc(t, d, 0);
    let p = e6.viewQuery;
    if (p !== null && Bo(2, p, r), !i)
      if (l) {
        let f = e6.viewCheckHooks;
        f !== null && Rn(t, f);
      } else {
        let f = e6.viewHooks;
        f !== null && On(t, f, 2), Ao(t, 2);
      }
    if (e6.firstUpdatePass === true && (e6.firstUpdatePass = false), t[En]) {
      for (let f of t[En])
        f();
      t[En] = null;
    }
    i || (Cc(t), t[h] &= -73);
  } catch (l) {
    throw i || Ct(t), l;
  } finally {
    u !== null && (Ui(u, c), a && rf(u)), Sn();
  }
}
function Sc(e6, t) {
  for (let n = Ga(e6); n !== null; n = Wa(n))
    for (let r = ie; r < n.length; r++) {
      let o = n[r];
      bc(o, t);
    }
}
function df(e6) {
  for (let t = Ga(e6); t !== null; t = Wa(t)) {
    if (!(t[h] & 2))
      continue;
    let n = t[Dt];
    for (let r = 0; r < n.length; r++) {
      let o = n[r];
      lo(o);
    }
  }
}
function ff(e6, t, n) {
  M(C.ComponentStart);
  let r = he(t, e6);
  try {
    bc(r, n);
  } finally {
    M(C.ComponentEnd, r[F]);
  }
}
function bc(e6, t) {
  wn(e6) && Jo(e6, t);
}
function Jo(e6, t) {
  let r = e6[y], o = e6[h], i = e6[P], s = !!(t === 0 && o & 16);
  if (s ||= !!(o & 64 && t === 0), s ||= !!(o & 1024), s ||= !!(i?.dirty && gr(i)), s ||= false, i && (i.dirty = false), e6[h] &= -9217, s)
    lf(r, e6, r.template, e6[F]);
  else if (o & 8192) {
    let a = D(null);
    try {
      Mc(e6), Sc(e6, 1);
      let c = r.components;
      c !== null && Nc(e6, c, 1), Cc(e6);
    } finally {
      D(a);
    }
  }
}
function Nc(e6, t, n) {
  for (let r = 0; r < t.length; r++)
    ff(e6, t[r], n);
}
function pf(e6, t) {
  let n = e6.hostBindingOpCodes;
  if (n !== null)
    try {
      for (let r = 0; r < n.length; r++) {
        let o = n[r];
        if (o < 0)
          ge(~o);
        else {
          let i = o, s = n[++r], a = n[++r];
          Gs(s, i);
          let c = t[i];
          M(C.HostBindingsUpdateStart, c);
          try {
            a(2, c);
          } finally {
            M(C.HostBindingsUpdateEnd, c);
          }
        }
      }
    } finally {
      ge(-1);
    }
}
function Ac(e6, t) {
  let n = mo() ? 64 : 1088;
  for (e6[Y].changeDetectionScheduler?.notify(t); e6; ) {
    e6[h] |= n;
    let r = Te(e6);
    if (Ye(e6) && !r)
      return e6;
    e6 = r;
  }
  return null;
}
function hf(e6, t) {
  if (e6.length <= ie)
    return;
  let n = ie + t, r = e6[n];
  if (r) {
    let o = r[mt];
    o !== null && o !== e6 && mi(o, r), t > 0 && (e6[n - 1][re] = r[re]);
    let i = eo(e6, ie + t);
    Md(r[y], r);
    let s = i[vn];
    s !== null && s.detachView(i[y]), r[k] = null, r[re] = null, r[h] &= -129;
  }
  return r;
}
function gf(e6, t) {
  let n = e6[Dt], r = t[k];
  if (de(r))
    e6[h] |= 2;
  else {
    let o = r[k][Q];
    t[Q] !== o && (e6[h] |= 2);
  }
  n === null ? e6[Dt] = [t] : n.push(t);
}
var Pn = class {
  _lView;
  _cdRefInjectingView;
  _appRef = null;
  _attachedToViewContainer = false;
  exhaustive;
  get rootNodes() {
    let t = this._lView, n = t[y];
    return xt(n, t, n.firstChild, []);
  }
  constructor(t, n) {
    this._lView = t, this._cdRefInjectingView = n;
  }
  get context() {
    return this._lView[F];
  }
  set context(t) {
    this._lView[F] = t;
  }
  get destroyed() {
    return Ae(this._lView);
  }
  destroy() {
    if (this._appRef)
      this._appRef.detachView(this);
    else if (this._attachedToViewContainer) {
      let t = this._lView[k];
      if (fe(t)) {
        let n = t[Ns], r = n ? n.indexOf(this) : -1;
        r > -1 && (hf(t, r), eo(n, r));
      }
      this._attachedToViewContainer = false;
    }
    Sd(this._lView[y], this._lView);
  }
  onDestroy(t) {
    po(this._lView, t);
  }
  markForCheck() {
    Ac(this._cdRefInjectingView || this._lView, 4);
  }
  detach() {
    this._lView[h] &= -129;
  }
  reattach() {
    fo(this._lView), this._lView[h] |= 128;
  }
  detectChanges() {
    this._lView[h] |= 1024, _c(this._lView);
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
    let t = Ye(this._lView), n = this._lView[mt];
    n !== null && !t && mi(n, this._lView), yc(this._lView[y], this._lView);
  }
  attachToAppRef(t) {
    if (this._attachedToViewContainer)
      throw new g(902, false);
    this._appRef = t;
    let n = Ye(this._lView), r = this._lView[mt];
    r !== null && !n && gf(r, this._lView), fo(this._lView);
  }
};
function vi(e6, t, n, r, o) {
  let i = e6.data[t];
  if (i === null)
    i = mf(e6, t, n, r, o), zs() && (i.flags |= 32);
  else if (i.type & 64) {
    i.type = n, i.value = r, i.attrs = o;
    let s = Hs();
    i.injectorIndex = s === null ? -1 : s.injectorIndex;
  }
  return wt(i, true), i;
}
function mf(e6, t, n, r, o) {
  let i = ho(), s = go(), a = s ? i : i && i.parent, c = e6.data[t] = Df(e6, a, n, t, r, o);
  return yf(e6, c, i, s), c;
}
function yf(e6, t, n, r) {
  e6.firstChild === null && (e6.firstChild = t), n !== null && (r ? n.child == null && t.parent !== null && (n.child = t) : n.next === null && (n.next = t, t.prev = n));
}
function Df(e6, t, n, r, o, i) {
  let s = t ? t.injectorIndex : -1, a = 0;
  return js() && (a |= 128), { type: n, index: r, insertBeforeIndex: null, injectorIndex: s, directiveStart: -1, directiveEnd: -1, directiveStylingLast: -1, componentOffset: -1, controlDirectiveIndex: -1, customControlIndex: -1, propertyBindings: null, flags: a, providerIndexes: 0, value: o, attrs: i, mergedAttrs: null, localNames: null, initialInputs: null, inputs: null, hostDirectiveInputs: null, outputs: null, hostDirectiveOutputs: null, directiveToIndex: null, tView: null, next: null, prev: null, projectionNext: null, child: null, parent: t, projection: null, styles: null, stylesWithoutHost: null, residualStyles: void 0, classes: null, classesWithoutHost: null, residualClasses: void 0, classBindings: 0, styleBindings: 0 };
}
var xc = class {
};
var Qn = class {
};
var Xo = class {
  resolveComponentFactory(t) {
    throw new g(917, false);
  }
};
var Kn = class {
  static NULL = new Xo();
};
var Re = class {
};
var Rc = (() => {
  class e6 {
    static \u0275prov = _({ token: e6, providedIn: "root", factory: () => null });
  }
  return e6;
})();
var kn = {};
var ei = class {
  injector;
  parentInjector;
  constructor(t, n) {
    this.injector = t, this.parentInjector = n;
  }
  get(t, n, r) {
    let o = this.injector.get(t, kn, r);
    return o !== kn || n === kn ? o : this.parentInjector.get(t, n, r);
  }
};
function jn(e6, t, n) {
  let r = n ? e6.styles : null, o = n ? e6.classes : null, i = 0;
  if (t !== null)
    for (let s = 0; s < t.length; s++) {
      let a = t[s];
      if (typeof a == "number")
        i = a;
      else if (i == 1)
        o = zr(o, a);
      else if (i == 2) {
        let c = a, u = t[++s];
        r = zr(r, c + ": " + u + ";");
      }
    }
  n ? e6.styles = r : e6.stylesWithoutHost = r, n ? e6.classes = o : e6.classesWithoutHost = o;
}
function ot(e6, t = 0) {
  let n = B();
  if (n === null)
    return E(e6, t);
  let r = Qe();
  return Va(r, n, O(e6), t);
}
function vf(e6, t, n, r, o) {
  let i = r === null ? null : { "": -1 }, s = o(e6, n);
  if (s !== null) {
    let a = s, c = null, u = null;
    for (let l of s)
      if (l.resolveHostDirectives !== null) {
        [a, c, u] = l.resolveHostDirectives(s);
        break;
      }
    Cf(e6, t, n, a, i, c, u);
  }
  i !== null && r !== null && Ef(n, r, i);
}
function Ef(e6, t, n) {
  let r = e6.localNames = [];
  for (let o = 0; o < t.length; o += 2) {
    let i = n[t[o + 1]];
    if (i == null)
      throw new g(-301, false);
    r.push(t[o], i);
  }
}
function If(e6, t, n) {
  t.componentOffset = n, (e6.components ??= []).push(t.index);
}
function Cf(e6, t, n, r, o, i, s) {
  let a = r.length, c = null;
  for (let p = 0; p < a; p++) {
    let f = r[p];
    c === null && Ze(f) && (c = f, If(e6, n, p)), Sl(Fa(n, t), e6, f.type);
  }
  bf(n, e6.data.length, a), c?.viewProvidersResolver && c.viewProvidersResolver(c);
  for (let p = 0; p < a; p++) {
    let f = r[p];
    f.providersResolver && f.providersResolver(f);
  }
  let u = false, l = false, d = dc(e6, t, a, null);
  a > 0 && (n.directiveToIndex = /* @__PURE__ */ new Map());
  for (let p = 0; p < a; p++) {
    let f = r[p];
    if (n.mergedAttrs = oi(n.mergedAttrs, f.hostAttrs), Tf(e6, n, t, d, f), Sf(d, f, o), s !== null && s.has(f)) {
      let [ur, tu] = s.get(f);
      n.directiveToIndex.set(f.type, [d, ur + n.directiveStart, tu + n.directiveStart]);
    } else
      (i === null || !i.has(f)) && n.directiveToIndex.set(f.type, d);
    f.contentQueries !== null && (n.flags |= 4), (f.hostBindings !== null || f.hostAttrs !== null || f.hostVars !== 0) && (n.flags |= 64);
    let T = f.type.prototype;
    !u && (T.ngOnChanges || T.ngOnInit || T.ngDoCheck) && ((e6.preOrderHooks ??= []).push(n.index), u = true), !l && (T.ngOnChanges || T.ngDoCheck) && ((e6.preOrderCheckHooks ??= []).push(n.index), l = true), d++;
  }
  wf(e6, n, i);
}
function wf(e6, t, n) {
  for (let r = t.directiveStart; r < t.directiveEnd; r++) {
    let o = e6.data[r];
    if (n === null || !n.has(o))
      Ta(0, t, o, r), Ta(1, t, o, r), _a(t, r, false);
    else {
      let i = n.get(o);
      Ma(0, t, i, r), Ma(1, t, i, r), _a(t, r, true);
    }
  }
}
function Ta(e6, t, n, r) {
  let o = e6 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s;
      e6 === 0 ? s = t.inputs ??= {} : s = t.outputs ??= {}, s[i] ??= [], s[i].push(r), Oc(t, i);
    }
}
function Ma(e6, t, n, r) {
  let o = e6 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s = o[i], a;
      e6 === 0 ? a = t.hostDirectiveInputs ??= {} : a = t.hostDirectiveOutputs ??= {}, a[s] ??= [], a[s].push(r, i), Oc(t, s);
    }
}
function Oc(e6, t) {
  t === "class" ? e6.flags |= 8 : t === "style" && (e6.flags |= 16);
}
function _a(e6, t, n) {
  let { attrs: r, inputs: o, hostDirectiveInputs: i } = e6;
  if (r === null || !n && o === null || n && i === null || fd(e6)) {
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
function Tf(e6, t, n, r, o) {
  e6.data[r] = o;
  let i = o.factory || (o.factory = $e(o.type, true)), s = new Nt(i, Ze(o), ot, null);
  e6.blueprint[r] = s, n[r] = s, Mf(e6, t, r, dc(e6, n, o.hostVars, nt), o);
}
function Mf(e6, t, n, r, o) {
  let i = o.hostBindings;
  if (i) {
    let s = e6.hostBindingOpCodes;
    s === null && (s = e6.hostBindingOpCodes = []);
    let a = ~t.index;
    _f(s) != a && s.push(a), s.push(n, r, i);
  }
}
function _f(e6) {
  let t = e6.length;
  for (; t > 0; ) {
    let n = e6[--t];
    if (typeof n == "number" && n < 0)
      return n;
  }
  return 0;
}
function Sf(e6, t, n) {
  if (n) {
    if (t.exportAs)
      for (let r = 0; r < t.exportAs.length; r++)
        n[t.exportAs[r]] = e6;
    Ze(t) && (n[""] = e6);
  }
}
function bf(e6, t, n) {
  e6.flags |= 1, e6.directiveStart = t, e6.directiveEnd = t + n, e6.providerIndexes = t;
}
function Nf(e6, t, n, r, o, i, s, a) {
  let c = t[y], u = c.consts, l = Et(u, s), d = vi(c, e6, n, r, l);
  return i && vf(c, t, d, Et(u, a), o), d.mergedAttrs = oi(d.mergedAttrs, d.attrs), d.attrs !== null && jn(d, d.attrs, false), d.mergedAttrs !== null && jn(d, d.mergedAttrs, true), c.queries !== null && c.queries.elementStart(c, d), d;
}
function Af(e6, t) {
  Dl(e6, t), ao(t) && e6.queries.elementEnd(t);
}
function xf(e6, t, n, r, o, i) {
  let s = t.consts, a = Et(s, o), c = vi(t, e6, n, r, a);
  if (c.mergedAttrs = oi(c.mergedAttrs, c.attrs), i != null) {
    let u = Et(s, i);
    c.localNames = [];
    for (let l = 0; l < u.length; l += 2)
      c.localNames.push(u[l], -1);
  }
  return c.attrs !== null && jn(c, c.attrs, false), c.mergedAttrs !== null && jn(c, c.mergedAttrs, true), t.queries !== null && t.queries.elementStart(t, c), c;
}
function kc(e6, t, n) {
  if (n === nt)
    return false;
  let r = e6[t];
  return Object.is(r, n) ? false : (e6[t] = n, true);
}
var ti = Symbol("BINDING");
function Rf(e6) {
  return e6.debugInfo?.className || e6.type.name || null;
}
var ni = class extends Kn {
  ngModule;
  constructor(t) {
    super(), this.ngModule = t;
  }
  resolveComponentFactory(t) {
    let n = ft(t);
    return new Bn(n, this.ngModule);
  }
};
function Of(e6) {
  return Object.keys(e6).map((t) => {
    let [n, r, o] = e6[t], i = { propName: n, templateName: t, isSignal: (r & Yn.SignalBased) !== 0 };
    return o && (i.transform = o), i;
  });
}
function kf(e6) {
  return Object.keys(e6).map((t) => ({ propName: e6[t], templateName: t }));
}
function Ff(e6, t, n) {
  let r = t instanceof U ? t : t?.injector;
  return r && e6.getStandaloneInjector !== null && (r = e6.getStandaloneInjector(r) || r), r ? new ei(n, r) : n;
}
function Lf(e6) {
  let t = e6.get(Re, null);
  if (t === null)
    throw new g(407, false);
  let n = e6.get(Rc, null), r = e6.get(Ue, null), o = e6.get(rt, null, { optional: true });
  return { rendererFactory: t, sanitizer: n, changeDetectionScheduler: r, ngReflect: false, tracingService: o };
}
function Pf(e6, t) {
  let n = Fc(e6);
  return ic(t, n, n === "svg" ? xs : n === "math" ? Rs : null);
}
function Fc(e6) {
  return (e6.selectors[0][0] || "div").toLowerCase();
}
var Bn = class extends Qn {
  componentDef;
  ngModule;
  selector;
  componentType;
  ngContentSelectors;
  isBoundToModule;
  cachedInputs = null;
  cachedOutputs = null;
  get inputs() {
    return this.cachedInputs ??= Of(this.componentDef.inputs), this.cachedInputs;
  }
  get outputs() {
    return this.cachedOutputs ??= kf(this.componentDef.outputs), this.cachedOutputs;
  }
  constructor(t, n) {
    super(), this.componentDef = t, this.ngModule = n, this.componentType = t.type, this.selector = hd(t.selectors), this.ngContentSelectors = t.ngContentSelectors ?? [], this.isBoundToModule = !!n;
  }
  create(t, n, r, o, i, s) {
    M(C.DynamicComponentStart);
    let a = D(null);
    try {
      let c = this.componentDef, u = Ff(c, o || this.ngModule, t), l = Lf(u), d = l.tracingService;
      return d && d.componentCreate ? d.componentCreate(Rf(c), () => this.createComponentRef(l, u, n, r, i, s)) : this.createComponentRef(l, u, n, r, i, s);
    } finally {
      D(a);
    }
  }
  createComponentRef(t, n, r, o, i, s) {
    let a = this.componentDef, c = jf(o, a, s, i), u = t.rendererFactory.createRenderer(null, a), l = o ? Hd(u, o, a.encapsulation, n) : Pf(a, u), d = s?.some(Sa) || i?.some((T) => typeof T != "function" && T.bindings.some(Sa)), p = uc(null, c, null, 512 | lc(a), null, null, t, u, n, null, Ka(l, n, true));
    p[z] = l, _n(p);
    let f = null;
    try {
      let T = Nf(z, p, 2, "#host", () => c.directiveRegistry, true, 0);
      ac(u, l, T), At(l, p), Bd(c, p, T), Vl(c, T, p), Af(c, T), r !== void 0 && Vf(T, this.ngContentSelectors, r), f = he(T.index, p), p[F] = f[F], Ec(c, p, null);
    } catch (T) {
      throw f !== null && Po(f), Po(p), T;
    } finally {
      M(C.DynamicComponentEnd), Sn();
    }
    return new Vn(this.componentType, p, !!d);
  }
};
function jf(e6, t, n, r) {
  let o = e6 ? ["ng-version", "21.2.11"] : gd(t.selectors[0]), i = null, s = null, a = 0;
  if (n)
    for (let l of n)
      a += l[ti].requiredVars, l.create && (l.targetIdx = 0, (i ??= []).push(l)), l.update && (l.targetIdx = 0, (s ??= []).push(l));
  if (r)
    for (let l = 0; l < r.length; l++) {
      let d = r[l];
      if (typeof d != "function")
        for (let p of d.bindings) {
          a += p[ti].requiredVars;
          let f = l + 1;
          p.create && (p.targetIdx = f, (i ??= []).push(p)), p.update && (p.targetIdx = f, (s ??= []).push(p));
        }
    }
  let c = [t];
  if (r)
    for (let l of r) {
      let d = typeof l == "function" ? l : l.type, p = Yr(d);
      c.push(p);
    }
  return cc(0, null, Bf(i, s), 1, a, c, null, null, null, [o], null);
}
function Bf(e6, t) {
  return !e6 && !t ? null : (n) => {
    if (n & 1 && e6)
      for (let r of e6)
        r.create();
    if (n & 2 && t)
      for (let r of t)
        r.update();
  };
}
function Sa(e6) {
  let t = e6[ti].kind;
  return t === "input" || t === "twoWay";
}
var Vn = class extends xc {
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
    super(), this._rootLView = n, this._hasInputBindings = r, this._tNode = co(n[y], z), this.location = Ua(this._tNode, n), this.instance = he(this._tNode.index, n)[F], this.hostView = this.changeDetectorRef = new Pn(n, void 0), this.componentType = t;
  }
  setInput(t, n) {
    this._hasInputBindings;
    let r = this._tNode;
    if (this.previousInputValues ??= /* @__PURE__ */ new Map(), this.previousInputValues.has(t) && Object.is(this.previousInputValues.get(t), n))
      return;
    let o = this._rootLView, i = Kd(r, o[y], o, t, n);
    this.previousInputValues.set(t, n);
    let s = he(r.index, o);
    Ac(s, 1);
  }
  get injector() {
    return new Ln(this._tNode, this._rootLView);
  }
  destroy() {
    this.hostView.destroy();
  }
  onDestroy(t) {
    this.hostView.onDestroy(t);
  }
};
function Vf(e6, t, n) {
  let r = e6.projection = [];
  for (let o = 0; o < t.length; o++) {
    let i = n[o];
    r.push(i != null && i.length ? Array.from(i) : null);
  }
}
var Hn = class {
};
var Rt = class extends Hn {
  injector;
  componentFactoryResolver = new ni(this);
  instance = null;
  constructor(t) {
    super();
    let n = new we([...t.providers, { provide: Hn, useValue: this }, { provide: Kn, useValue: this.componentFactoryResolver }], t.parent || gt(), t.debugName, /* @__PURE__ */ new Set(["environment"]));
    this.injector = n, t.runEnvironmentInitializers && n.resolveInjectorInitializers();
  }
  destroy() {
    this.injector.destroy();
  }
  onDestroy(t) {
    this.injector.onDestroy(t);
  }
};
function Lc(e6, t, n = null) {
  return new Rt({ providers: e6, parent: t, debugName: n, runEnvironmentInitializers: true }).injector;
}
var Hf = (() => {
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
        let r = ro(false, n.type), o = r.length > 0 ? Lc([r], this._injector, "") : null;
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
    static \u0275prov = _({ token: e6, providedIn: "environment", factory: () => new e6(E(U)) });
  }
  return e6;
})();
function Ei(e6) {
  return ri(() => {
    let t = Gf(e6), n = V(x({}, t), { decls: e6.decls, vars: e6.vars, template: e6.template, consts: e6.consts || null, ngContentSelectors: e6.ngContentSelectors, onPush: e6.changeDetection === si.OnPush, directiveDefs: null, pipeDefs: null, dependencies: t.standalone && e6.dependencies || null, getStandaloneInjector: t.standalone ? (o) => o.get(Hf).getOrCreateStandaloneInjector(n) : null, getExternalStyles: null, signals: e6.signals ?? false, data: e6.data || {}, encapsulation: e6.encapsulation || G.Emulated, styles: e6.styles || $, _: null, schemas: e6.schemas || null, tView: null, id: "" });
    t.standalone && hc("NgStandalone"), Wf(n);
    let r = e6.dependencies;
    return n.directiveDefs = ba(r, $f), n.pipeDefs = ba(r, Ds), n.id = qf(n), n;
  });
}
function $f(e6) {
  return ft(e6) || Yr(e6);
}
function Ft(e6) {
  return ri(() => ({ type: e6.type, bootstrap: e6.bootstrap || $, declarations: e6.declarations || $, imports: e6.imports || $, exports: e6.exports || $, transitiveCompileScopes: null, schemas: e6.schemas || null, id: e6.id || null }));
}
function Uf(e6, t) {
  if (e6 == null)
    return _e;
  let n = {};
  for (let r in e6)
    if (e6.hasOwnProperty(r)) {
      let o = e6[r], i, s, a, c;
      Array.isArray(o) ? (a = o[0], i = o[1], s = o[2] ?? i, c = o[3] || null) : (i = o, s = o, a = Yn.None, c = null), n[i] = [r, a, c], t[i] = s;
    }
  return n;
}
function zf(e6) {
  if (e6 == null)
    return _e;
  let t = {};
  for (let n in e6)
    e6.hasOwnProperty(n) && (t[e6[n]] = n);
  return t;
}
function Gf(e6) {
  let t = {};
  return { type: e6.type, providersResolver: null, viewProvidersResolver: null, factory: null, hostBindings: e6.hostBindings || null, hostVars: e6.hostVars || 0, hostAttrs: e6.hostAttrs || null, contentQueries: e6.contentQueries || null, declaredInputs: t, inputConfig: e6.inputs || _e, exportAs: e6.exportAs || null, standalone: e6.standalone ?? true, signals: e6.signals === true, selectors: e6.selectors || $, viewQuery: e6.viewQuery || null, features: e6.features || null, setInput: null, resolveHostDirectives: null, hostDirectives: null, controlDef: null, inputs: Uf(e6.inputs, t), outputs: zf(e6.outputs), debugInfo: null };
}
function Wf(e6) {
  e6.features?.forEach((t) => t(e6));
}
function ba(e6, t) {
  return e6 ? () => {
    let n = typeof e6 == "function" ? e6() : e6, r = [];
    for (let o of n) {
      let i = t(o);
      i !== null && r.push(i);
    }
    return r;
  } : null;
}
function qf(e6) {
  let t = 0, n = typeof e6.consts == "function" ? "" : e6.consts, r = [e6.selectors, e6.ngContentSelectors, e6.hostVars, e6.hostAttrs, n, e6.vars, e6.decls, e6.encapsulation, e6.standalone, e6.signals, e6.exportAs, JSON.stringify(e6.inputs), JSON.stringify(e6.outputs), Object.getOwnPropertyNames(e6.type.prototype), !!e6.contentQueries, !!e6.viewQuery];
  for (let i of r.join("|"))
    t = Math.imul(31, t) + i.charCodeAt(0) << 0;
  return t += 2147483648, "c" + t;
}
var Ii = new m("");
function Ci(e6) {
  return !!e6 && typeof e6.then == "function";
}
function Pc(e6) {
  return !!e6 && typeof e6.subscribe == "function";
}
var jc = new m("");
var wi = (() => {
  class e6 {
    resolve;
    reject;
    initialized = false;
    done = false;
    donePromise = new Promise((n, r) => {
      this.resolve = n, this.reject = r;
    });
    appInits = v(jc, { optional: true }) ?? [];
    injector = v(te);
    constructor() {
    }
    runInitializers() {
      if (this.initialized)
        return;
      let n = [];
      for (let o of this.appInits) {
        let i = mn(this.injector, o);
        if (Ci(i))
          n.push(i);
        else if (Pc(i)) {
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
var Bc = new m("");
function Vc() {
  yr(() => {
    let e6 = "";
    throw new g(600, e6);
  });
}
function Hc(e6) {
  return e6.isBoundToModule;
}
var Zf = 10;
var Lt = (() => {
  class e6 {
    _runningTick = false;
    _destroyed = false;
    _destroyListeners = [];
    _views = [];
    internalErrorHandler = v(Je);
    afterRenderManager = v(gc);
    zonelessEnabled = v(_t);
    rootEffectScheduler = v(No);
    dirtyFlags = 0;
    tracingSnapshot = null;
    allTestViews = /* @__PURE__ */ new Set();
    autoDetectTestViews = /* @__PURE__ */ new Set();
    includeAllTestViews = false;
    afterTick = new ce();
    get allViews() {
      return [...(this.includeAllTestViews ? this.allTestViews : this.autoDetectTestViews).keys(), ...this._views];
    }
    get destroyed() {
      return this._destroyed;
    }
    componentTypes = [];
    components = [];
    internalPendingTask = v(Ke);
    get isStable() {
      return this.internalPendingTask.hasPendingTasksObservable.pipe(Sr((n) => !n));
    }
    constructor() {
      v(rt, { optional: true });
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
    _injector = v(U);
    _rendererFactory = null;
    get injector() {
      return this._injector;
    }
    bootstrap(n, r) {
      return this.bootstrapImpl(n, r);
    }
    bootstrapImpl(n, r, o = te.NULL) {
      return this._injector.get(j).run(() => {
        M(C.BootstrapComponentStart);
        let s = n instanceof Qn;
        if (!this._injector.get(wi).done) {
          let T = "";
          throw new g(405, T);
        }
        let c;
        s ? c = n : c = this._injector.get(Kn).resolveComponentFactory(n), this.componentTypes.push(c.componentType);
        let u = Hc(c) ? void 0 : this._injector.get(Hn), l = r || c.selector, d = c.create(o, [], l, u), p = d.location.nativeElement, f = d.injector.get(Ii, null);
        return f?.registerApplication(p), d.onDestroy(() => {
          this.detachView(d.hostView), bt(this.components, d), f?.unregisterApplication(p);
        }), this._loadComponent(d), M(C.BootstrapComponentEnd, d), d;
      });
    }
    tick() {
      this.zonelessEnabled || (this.dirtyFlags |= 1), this._tick();
    }
    _tick() {
      M(C.ChangeDetectionStart), this.tracingSnapshot !== null ? this.tracingSnapshot.run(gi.CHANGE_DETECTION, this.tickImpl) : this.tickImpl();
    }
    tickImpl = () => {
      if (this._runningTick)
        throw M(C.ChangeDetectionEnd), new g(101, false);
      let n = D(null);
      try {
        this._runningTick = true, this.synchronize();
      } finally {
        this._runningTick = false, this.tracingSnapshot?.dispose(), this.tracingSnapshot = null, D(n), this.afterTick.next(), M(C.ChangeDetectionEnd);
      }
    };
    synchronize() {
      this._rendererFactory === null && !this._injector.destroyed && (this._rendererFactory = this._injector.get(Re, null, { optional: true }));
      let n = 0;
      for (; this.dirtyFlags !== 0 && n++ < Zf; ) {
        M(C.ChangeDetectionSyncStart);
        try {
          this.synchronizeOnce();
        } finally {
          M(C.ChangeDetectionSyncEnd);
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
          if (!r && !It(o))
            continue;
          let i = r && !this.zonelessEnabled ? 0 : 1;
          _c(o, i), n = true;
        }
        if (this.dirtyFlags &= -5, this.syncDirtyFlagsWithViews(), this.dirtyFlags & 23)
          return;
      }
      n || (this._rendererFactory?.begin?.(), this._rendererFactory?.end?.()), this.dirtyFlags & 8 && (this.dirtyFlags &= -9, this.afterRenderManager.execute()), this.syncDirtyFlagsWithViews();
    }
    syncDirtyFlagsWithViews() {
      if (this.allViews.some(({ _lView: n }) => It(n))) {
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
      bt(this._views, r), r.detachFromAppRef();
    }
    _loadComponent(n) {
      this.attachView(n.hostView);
      try {
        this.tick();
      } catch (o) {
        this.internalErrorHandler(o);
      }
      this.components.push(n), this._injector.get(Bc, []).forEach((o) => o(n));
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
      return this._destroyListeners.push(n), () => bt(this._destroyListeners, n);
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
function bt(e6, t) {
  let n = e6.indexOf(t);
  n > -1 && e6.splice(n, 1);
}
function ke(e6, t, n, r) {
  let o = B(), i = o[y], s = e6 + z, a = i.firstCreatePass ? xf(s, i, 2, t, n, r) : i.data[s];
  return Yd(a, o, e6, t, Yf), r != null && Vd(o, a), ke;
}
function De() {
  let e6 = Qe(), t = Qd(e6);
  return Bs(t) && Vs(), Ps(), De;
}
function Jn(e6, t, n, r) {
  return ke(e6, t, n, r), De(), Jn;
}
var Yf = (e6, t, n, r, o) => (wo(true), ic(t[L], r, Ks()));
function Xn(e6, t, n) {
  let r = B(), o = Do();
  if (kc(r, o, t)) {
    let i = Tn(), s = Qs();
    zd(s, r, e6, t, r[L], n);
  }
  return Xn;
}
var Pt = "en-US";
var Qf = Pt;
function $c(e6) {
  typeof e6 == "string" && (Qf = e6.toLowerCase().replace(/_/g, "-"));
}
function jt(e6, t = "") {
  let n = B(), r = Tn(), o = e6 + z, i = r.firstCreatePass ? vi(r, o, 1, t, null) : r.data[o], s = Kf(r, n, i, t);
  n[o] = s, Co() && Dc(r, n, s, i), wt(i, false);
}
var Kf = (e6, t, n, r) => (wo(true), id(t[L], r));
function Jf(e6, t, n, r = "") {
  return kc(e6, Do(), n) ? t + Kr(n) + r : nt;
}
function er(e6, t, n) {
  let r = B(), o = Jf(r, e6, t, n);
  return o !== nt && Xf(r, bn(), o), er;
}
function Xf(e6, t, n) {
  let r = Os(t, e6);
  sd(e6[L], r, n);
}
var Uc = (() => {
  class e6 {
    applicationErrorHandler = v(Je);
    appRef = v(Lt);
    taskService = v(Ke);
    ngZone = v(j);
    zonelessEnabled = v(_t);
    tracing = v(rt, { optional: true });
    zoneIsDefined = typeof Zone < "u" && !!Zone.root.run;
    schedulerTickApplyArgs = [{ data: { __scheduler_tick__: true } }];
    subscriptions = new b();
    angularZoneId = this.zoneIsDefined ? this.ngZone._inner?.get(lt) : null;
    scheduleInRootZone = !this.zonelessEnabled && this.zoneIsDefined && (v(bo, { optional: true }) ?? false);
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
      let r = this.useMicrotaskScheduler ? na : To;
      this.pendingRenderTaskId = this.taskService.add(), this.scheduleInRootZone ? this.cancelScheduledCallback = Zone.root.run(() => r(() => this.tick())) : this.cancelScheduledCallback = this.ngZone.runOutsideAngular(() => r(() => this.tick()));
    }
    shouldScheduleTick() {
      return !(this.appRef.destroyed || this.pendingRenderTaskId !== null || this.runningTick || this.appRef._runningTick || !this.zonelessEnabled && this.zoneIsDefined && Zone.current.get(lt + this.angularZoneId));
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
function zc() {
  return [{ provide: Ue, useExisting: Uc }, { provide: j, useClass: dt }, { provide: _t, useValue: true }];
}
function ep() {
  return typeof $localize < "u" && $localize.locale || Pt;
}
var Ti = new m("", { factory: () => v(Ti, { optional: true, skipSelf: true }) || ep() });
var Mi = new m("");
var yp = new m("");
function Bt(e6) {
  return !e6.moduleRef;
}
function Dp(e6) {
  let t = Bt(e6) ? e6.r3Injector : e6.moduleRef.injector, n = t.get(j);
  return n.run(() => {
    Bt(e6) ? e6.r3Injector.resolveInjectorInitializers() : e6.moduleRef.resolveInjectorInitializers();
    let r = t.get(Je), o;
    if (n.runOutsideAngular(() => {
      o = n.onError.subscribe({ next: r });
    }), Bt(e6)) {
      let i = () => t.destroy(), s = e6.platformInjector.get(Mi);
      s.add(i), t.onDestroy(() => {
        o.unsubscribe(), s.delete(i);
      });
    } else {
      let i = () => e6.moduleRef.destroy(), s = e6.platformInjector.get(Mi);
      s.add(i), e6.moduleRef.onDestroy(() => {
        bt(e6.allPlatformModules, e6.moduleRef), o.unsubscribe(), s.delete(i);
      });
    }
    return Ep(r, n, () => {
      let i = t.get(Ke), s = i.add(), a = t.get(wi);
      return a.runInitializers(), a.donePromise.then(() => {
        let c = t.get(Ti, Pt);
        if ($c(c || Pt), !t.get(yp, true))
          return Bt(e6) ? t.get(Lt) : (e6.allPlatformModules.push(e6.moduleRef), e6.moduleRef);
        if (Bt(e6)) {
          let l = t.get(Lt);
          return e6.rootComponent !== void 0 && l.bootstrap(e6.rootComponent), l;
        } else
          return vp?.(e6.moduleRef, e6.allPlatformModules), e6.moduleRef;
      }).finally(() => {
        i.remove(s);
      });
    });
  });
}
var vp;
function Ep(e6, t, n) {
  try {
    let r = n();
    return Ci(r) ? r.catch((o) => {
      throw t.runOutsideAngular(() => e6(o)), o;
    }) : r;
  } catch (r) {
    throw t.runOutsideAngular(() => e6(r)), r;
  }
}
var tr = null;
function Ip(e6 = [], t) {
  return te.create({ name: t, providers: [{ provide: ht, useValue: "platform" }, { provide: Mi, useValue: /* @__PURE__ */ new Set([() => tr = null]) }, ...e6] });
}
function Cp(e6 = []) {
  if (tr)
    return tr;
  let t = Ip(e6);
  return tr = t, Vc(), wp(t), t;
}
function wp(e6) {
  let t = e6.get(Un, null);
  mn(e6, () => {
    t?.forEach((n) => n());
  });
}
var Tp = 1e4;
var gT = Tp - 1e3;
function Gc(e6) {
  let { rootComponent: t, appProviders: n, platformProviders: r, platformRef: o } = e6;
  M(C.BootstrapApplicationStart);
  try {
    let i = o?.injector ?? Cp(r), s = [zc(), oa, ...n || []], a = new Rt({ providers: s, parent: i, debugName: "", runEnvironmentInitializers: false });
    return Dp({ r3Injector: a.injector, platformInjector: i, rootComponent: t });
  } catch (i) {
    return Promise.reject(i);
  } finally {
    M(C.BootstrapApplicationEnd);
  }
}
var Wc = null;
function it() {
  return Wc;
}
function _i(e6) {
  Wc ??= e6;
}
var Ht = class {
};
var nr = (() => {
  class e6 {
    static \u0275fac = function(r) {
      return new (r || e6)();
    };
    static \u0275mod = Ft({ type: e6 });
    static \u0275inj = ze({});
  }
  return e6;
})();
function Si(e6, t) {
  t = encodeURIComponent(t);
  for (let n of e6.split(";")) {
    let r = n.indexOf("="), [o, i] = r == -1 ? [n, ""] : [n.slice(0, r), n.slice(r + 1)];
    if (o.trim() === t)
      return decodeURIComponent(i);
  }
  return null;
}
var $t = class {
};
var qc = "browser";
var Ut = class {
  _doc;
  constructor(t) {
    this._doc = t;
  }
  manager;
};
var rr = (() => {
  class e6 extends Ut {
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
      return new (r || e6)(E(A));
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var sr = new m("");
var xi = (() => {
  class e6 {
    _zone;
    _plugins;
    _eventNameToPlugin = /* @__PURE__ */ new Map();
    constructor(n, r) {
      this._zone = r, n.forEach((s) => {
        s.manager = this;
      });
      let o = n.filter((s) => !(s instanceof rr));
      this._plugins = o.slice().reverse();
      let i = n.find((s) => s instanceof rr);
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
      return new (r || e6)(E(sr), E(j));
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var bi = "ng-app-id";
function Zc(e6) {
  for (let t of e6)
    t.remove();
}
function Yc(e6, t) {
  let n = t.createElement("style");
  return n.textContent = e6, n;
}
function _p(e6, t, n, r) {
  let o = e6.head?.querySelectorAll(`style[${bi}="${t}"],link[${bi}="${t}"]`);
  if (o)
    for (let i of o)
      i.removeAttribute(bi), i instanceof HTMLLinkElement ? r.set(i.href.slice(i.href.lastIndexOf("/") + 1), { usage: 0, elements: [i] }) : i.textContent && n.set(i.textContent, { usage: 0, elements: [i] });
}
function Ai(e6, t) {
  let n = t.createElement("link");
  return n.setAttribute("rel", "stylesheet"), n.setAttribute("href", e6), n;
}
var Ri = (() => {
  class e6 {
    doc;
    appId;
    nonce;
    inline = /* @__PURE__ */ new Map();
    external = /* @__PURE__ */ new Map();
    hosts = /* @__PURE__ */ new Set();
    constructor(n, r, o, i = {}) {
      this.doc = n, this.appId = r, this.nonce = o, _p(n, r, this.inline, this.external), this.hosts.add(n.head);
    }
    addStyles(n, r) {
      for (let o of n)
        this.addUsage(o, this.inline, Yc);
      r?.forEach((o) => this.addUsage(o, this.external, Ai));
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
      o && (o.usage--, o.usage <= 0 && (Zc(o.elements), r.delete(n)));
    }
    ngOnDestroy() {
      for (let [, { elements: n }] of [...this.inline, ...this.external])
        Zc(n);
      this.hosts.clear();
    }
    addHost(n) {
      this.hosts.add(n);
      for (let [r, { elements: o }] of this.inline)
        o.push(this.addElement(n, Yc(r, this.doc)));
      for (let [r, { elements: o }] of this.external)
        o.push(this.addElement(n, Ai(r, this.doc)));
    }
    removeHost(n) {
      this.hosts.delete(n);
    }
    addElement(n, r) {
      return this.nonce && r.setAttribute("nonce", this.nonce), n.appendChild(r);
    }
    static \u0275fac = function(r) {
      return new (r || e6)(E(A), E($n), E(zn, 8), E(Ot));
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var Ni = { svg: "http://www.w3.org/2000/svg", xhtml: "http://www.w3.org/1999/xhtml", xlink: "http://www.w3.org/1999/xlink", xml: "http://www.w3.org/XML/1998/namespace", xmlns: "http://www.w3.org/2000/xmlns/", math: "http://www.w3.org/1998/Math/MathML" };
var Oi = /%COMP%/g;
var Kc = "%COMP%";
var Sp = `_nghost-${Kc}`;
var bp = `_ngcontent-${Kc}`;
var Np = true;
var Ap = new m("", { factory: () => Np });
function xp(e6) {
  return bp.replace(Oi, e6);
}
function Rp(e6) {
  return Sp.replace(Oi, e6);
}
function Jc(e6, t) {
  return t.map((n) => n.replace(Oi, e6));
}
var ki = (() => {
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
      this.eventManager = n, this.sharedStylesHost = r, this.appId = o, this.removeStylesOnCompDestroy = i, this.doc = s, this.ngZone = a, this.nonce = c, this.tracingService = u, this.defaultRenderer = new zt(n, s, a, this.tracingService);
    }
    createRenderer(n, r) {
      if (!n || !r)
        return this.defaultRenderer;
      let o = this.getOrCreateRenderer(n, r);
      return o instanceof ir ? o.applyToHost(n) : o instanceof Gt && o.applyStyles(), o;
    }
    getOrCreateRenderer(n, r) {
      let o = this.rendererByCompId, i = o.get(r.id);
      if (!i) {
        let s = this.doc, a = this.ngZone, c = this.eventManager, u = this.sharedStylesHost, l = this.removeStylesOnCompDestroy, d = this.tracingService;
        switch (r.encapsulation) {
          case G.Emulated:
            i = new ir(c, u, r, this.appId, l, s, a, d);
            break;
          case G.ShadowDom:
            return new or(c, n, r, s, a, this.nonce, d, u);
          case G.ExperimentalIsolatedShadowDom:
            return new or(c, n, r, s, a, this.nonce, d);
          default:
            i = new Gt(c, u, r, l, s, a, d);
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
      return new (r || e6)(E(xi), E(Ri), E($n), E(Ap), E(A), E(j), E(zn), E(rt, 8));
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var zt = class {
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
    return n ? this.doc.createElementNS(Ni[n] || n, t) : this.doc.createElement(t);
  }
  createComment(t) {
    return this.doc.createComment(t);
  }
  createText(t) {
    return this.doc.createTextNode(t);
  }
  appendChild(t, n) {
    (Qc(t) ? t.content : t).appendChild(n);
  }
  insertBefore(t, n, r) {
    t && (Qc(t) ? t.content : t).insertBefore(n, r);
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
      let i = Ni[o];
      i ? t.setAttributeNS(i, n, r) : t.setAttribute(n, r);
    } else
      t.setAttribute(n, r);
  }
  removeAttribute(t, n, r) {
    if (r) {
      let o = Ni[r];
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
    o & (Oe.DashCase | Oe.Important) ? t.style.setProperty(n, r, o & Oe.Important ? "important" : "") : t.style[n] = r;
  }
  removeStyle(t, n, r) {
    r & Oe.DashCase ? t.style.removeProperty(n) : t.style[n] = "";
  }
  setProperty(t, n, r) {
    t != null && (t[n] = r);
  }
  setValue(t, n) {
    t.nodeValue = n;
  }
  listen(t, n, r, o) {
    if (typeof t == "string" && (t = it().getGlobalEventTarget(this.doc, t), !t))
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
function Qc(e6) {
  return e6.tagName === "TEMPLATE" && e6.content !== void 0;
}
var or = class extends zt {
  hostEl;
  sharedStylesHost;
  shadowRoot;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, o, i, a), this.hostEl = n, this.sharedStylesHost = c, this.shadowRoot = n.attachShadow({ mode: "open" }), this.sharedStylesHost && this.sharedStylesHost.addHost(this.shadowRoot);
    let u = r.styles;
    u = Jc(r.id, u);
    for (let d of u) {
      let p = document.createElement("style");
      s && p.setAttribute("nonce", s), p.textContent = d, this.shadowRoot.appendChild(p);
    }
    let l = r.getExternalStyles?.();
    if (l)
      for (let d of l) {
        let p = Ai(d, o);
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
var Gt = class extends zt {
  sharedStylesHost;
  removeStylesOnCompDestroy;
  styles;
  styleUrls;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, i, s, a), this.sharedStylesHost = n, this.removeStylesOnCompDestroy = o;
    let u = r.styles;
    this.styles = c ? Jc(c, u) : u, this.styleUrls = r.getExternalStyles?.(c);
  }
  applyStyles() {
    this.sharedStylesHost.addStyles(this.styles, this.styleUrls);
  }
  destroy() {
    this.removeStylesOnCompDestroy && tt.size === 0 && this.sharedStylesHost.removeStyles(this.styles, this.styleUrls);
  }
};
var ir = class extends Gt {
  contentAttr;
  hostAttr;
  constructor(t, n, r, o, i, s, a, c) {
    let u = o + "-" + r.id;
    super(t, n, r, i, s, a, c, u), this.contentAttr = xp(u), this.hostAttr = Rp(u);
  }
  applyToHost(t) {
    this.applyStyles(), this.setAttribute(t, this.hostAttr, "");
  }
  createElement(t, n) {
    let r = super.createElement(t, n);
    return super.setAttribute(r, this.contentAttr, ""), r;
  }
};
var ar = class e4 extends Ht {
  supportsDOMEvents = true;
  static makeCurrent() {
    _i(new e4());
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
    let n = Op();
    return n == null ? null : kp(n);
  }
  resetBaseElement() {
    Wt = null;
  }
  getUserAgent() {
    return window.navigator.userAgent;
  }
  getCookie(t) {
    return Si(document.cookie, t);
  }
};
var Wt = null;
function Op() {
  return Wt = Wt || document.head.querySelector("base"), Wt ? Wt.getAttribute("href") : null;
}
function kp(e6) {
  return new URL(e6, document.baseURI).pathname;
}
var Fp = (() => {
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
var Xc = ["alt", "control", "meta", "shift"];
var Lp = { "\b": "Backspace", "	": "Tab", "\x7F": "Delete", "\x1B": "Escape", Del: "Delete", Esc: "Escape", Left: "ArrowLeft", Right: "ArrowRight", Up: "ArrowUp", Down: "ArrowDown", Menu: "ContextMenu", Scroll: "ScrollLock", Win: "OS" };
var Pp = { alt: (e6) => e6.altKey, control: (e6) => e6.ctrlKey, meta: (e6) => e6.metaKey, shift: (e6) => e6.shiftKey };
var eu = (() => {
  class e6 extends Ut {
    constructor(n) {
      super(n);
    }
    supports(n) {
      return e6.parseEventName(n) != null;
    }
    addEventListener(n, r, o, i) {
      let s = e6.parseEventName(r), a = e6.eventCallback(s.fullKey, o, this.manager.getZone());
      return this.manager.getZone().runOutsideAngular(() => it().onAndCancel(n, s.domEventName, a, i));
    }
    static parseEventName(n) {
      let r = n.toLowerCase().split("."), o = r.shift();
      if (r.length === 0 || !(o === "keydown" || o === "keyup"))
        return null;
      let i = e6._normalizeKey(r.pop()), s = "", a = r.indexOf("code");
      if (a > -1 && (r.splice(a, 1), s = "code."), Xc.forEach((u) => {
        let l = r.indexOf(u);
        l > -1 && (r.splice(l, 1), s += u + ".");
      }), s += i, r.length != 0 || i.length === 0)
        return null;
      let c = {};
      return c.domEventName = o, c.fullKey = s, c;
    }
    static matchEventFullKeyCode(n, r) {
      let o = Lp[n.key] || n.key, i = "";
      return r.indexOf("code.") > -1 && (o = n.code, i = "code."), o == null || !o ? false : (o = o.toLowerCase(), o === " " ? o = "space" : o === "." && (o = "dot"), Xc.forEach((s) => {
        if (s !== o) {
          let a = Pp[s];
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
      return new (r || e6)(E(A));
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
async function Fi(e6, t, n) {
  let r = x({ rootComponent: e6 }, jp(t, n));
  return Gc(r);
}
function jp(e6, t) {
  return { platformRef: t?.platformRef, appProviders: [...Up, ...e6?.providers ?? []], platformProviders: $p };
}
function Bp() {
  ar.makeCurrent();
}
function Vp() {
  return new ne();
}
function Hp() {
  return ai(document), document;
}
var $p = [{ provide: Ot, useValue: qc }, { provide: Un, useValue: Bp, multi: true }, { provide: A, useFactory: Hp }];
var Up = [{ provide: ht, useValue: "root" }, { provide: ne, useFactory: Vp }, { provide: sr, useClass: rr, multi: true }, { provide: sr, useClass: eu, multi: true }, ki, Ri, xi, { provide: Re, useExisting: ki }, { provide: $t, useClass: Fp }, []];
var Li = (() => {
  class e6 {
    static \u0275fac = function(r) {
      return new (r || e6)();
    };
    static \u0275prov = _({ token: e6, factory: function(r) {
      let o = null;
      return r ? o = new (r || e6)() : o = E(zp), o;
    }, providedIn: "root" });
  }
  return e6;
})();
var zp = (() => {
  class e6 extends Li {
    _doc;
    constructor(n) {
      super(), this._doc = n;
    }
    sanitize(n, r) {
      if (r == null)
        return null;
      switch (n) {
        case J.NONE:
          return r;
        case J.HTML:
          return ye(r, "HTML") ? me(r) : qn(this._doc, String(r)).toString();
        case J.STYLE:
          return ye(r, "Style") ? me(r) : r;
        case J.SCRIPT:
          if (ye(r, "Script"))
            return me(r);
          throw new g(5200, false);
        case J.URL:
          return ye(r, "URL") ? me(r) : Wn(String(r));
        case J.RESOURCE_URL:
          if (ye(r, "ResourceURL"))
            return me(r);
          throw new g(5201, false);
        default:
          throw new g(5202, false);
      }
    }
    bypassSecurityTrustHtml(n) {
      return ui(n);
    }
    bypassSecurityTrustStyle(n) {
      return li(n);
    }
    bypassSecurityTrustScript(n) {
      return di(n);
    }
    bypassSecurityTrustUrl(n) {
      return fi(n);
    }
    bypassSecurityTrustResourceUrl(n) {
      return pi(n);
    }
    static \u0275fac = function(r) {
      return new (r || e6)(E(A));
    };
    static \u0275prov = _({ token: e6, factory: e6.\u0275fac, providedIn: "root" });
  }
  return e6;
})();
var cr = class e5 {
  constructor(t, n) {
    this.model = t;
    this.sanitizer = n;
    if (t) {
      this.message.set(t.get("message") || "Model loaded, no message.");
      let r = t.get("table_html") || "<p>No table HTML yet.</p>";
      this.sanitizedHtml.set(this.sanitizer.bypassSecurityTrustHtml(r)), t.on("change:message", () => {
        this.message.set(t.get("message"));
      }), t.on("change:table_html", () => {
        let o = t.get("table_html");
        this.sanitizedHtml.set(this.sanitizer.bypassSecurityTrustHtml(o));
      });
    }
  }
  message = Mt("Waiting for model...");
  sanitizedHtml = Mt("");
  static \u0275fac = function(n) {
    return new (n || e5)(ot("ANYWIDGET_MODEL"), ot(Li));
  };
  static \u0275cmp = Ei({ type: e5, selectors: [["app-root"]], decls: 8, vars: 2, consts: [[1, "angular-widget"], [3, "innerHTML"]], template: function(n, r) {
    n & 1 && (ke(0, "div", 0)(1, "h3"), jt(2, "Angular Hybrid Widget"), De(), ke(3, "p"), jt(4, "Status: Infrastructure Loaded"), De(), ke(5, "p"), jt(6), De(), Jn(7, "div", 1), De()), n & 2 && (Zn(6), er("Message from Python: ", r.message()), Zn(), Xn("innerHTML", r.sanitizedHtml(), hi));
  }, dependencies: [nr], styles: [".angular-widget[_ngcontent-%COMP%]{padding:10px;border:1px solid #ccc;border-radius:4px;background-color:#f9f9f9}"] });
};
function Wp({ model: e6, el: t }) {
  let n = document.createElement("app-root");
  t.appendChild(n);
  let r = { providers: [So(), { provide: "ANYWIDGET_MODEL", useValue: e6 }] };
  Fi(cr, r).catch((o) => console.error(o));
}
var k_ = { render: Wp };
export {
  k_ as default
};
