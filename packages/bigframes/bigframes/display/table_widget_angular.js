/*
 * Copyright 2026 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


// dist/table-widget-angular/browser/main.js
var tl = Object.defineProperty;
var nl = Object.defineProperties;
var rl = Object.getOwnPropertyDescriptors;
var ki = Object.getOwnPropertySymbols;
var ol = Object.prototype.hasOwnProperty;
var il = Object.prototype.propertyIsEnumerable;
var Oi = (e6, t, n) => t in e6 ? tl(e6, t, { enumerable: true, configurable: true, writable: true, value: n }) : e6[t] = n;
var A = (e6, t) => {
  for (var n in t ||= {})
    ol.call(t, n) && Oi(e6, n, t[n]);
  if (ki)
    for (var n of ki(t))
      il.call(t, n) && Oi(e6, n, t[n]);
  return e6;
};
var V = (e6, t) => nl(e6, rl(t));
var b = null;
var zt = false;
var cr = 1;
var sl = null;
var W = Symbol("SIGNAL");
function v(e6) {
  let t = b;
  return b = e6, t;
}
function Wt() {
  return b;
}
var Gt = { version: 0, lastCleanEpoch: 0, dirty: false, producers: void 0, producersTail: void 0, consumers: void 0, consumersTail: void 0, recomputing: false, consumerAllowSignalWrites: false, consumerIsAlwaysLive: false, kind: "unknown", producerMustRecompute: () => false, producerRecomputeValue: () => {
}, consumerMarkedDirty: () => {
}, consumerOnSignalRead: () => {
} };
function Li(e6) {
  if (zt)
    throw new Error("");
  if (b === null)
    return;
  b.consumerOnSignalRead(e6);
  let t = b.producersTail;
  if (t !== void 0 && t.producer === e6)
    return;
  let n, r = b.recomputing;
  if (r && (n = t !== void 0 ? t.nextProducer : b.producers, n !== void 0 && n.producer === e6)) {
    b.producersTail = n, n.lastReadVersion = e6.version;
    return;
  }
  let o = e6.consumersTail;
  if (o !== void 0 && o.consumer === b && (!r || cl(o, b)))
    return;
  let i = Le(b), s = { producer: e6, consumer: b, nextProducer: n, prevConsumer: o, lastReadVersion: e6.version, nextConsumer: void 0 };
  b.producersTail = s, t !== void 0 ? t.nextProducer = s : b.producers = s, i && Bi(e6, s);
}
function Pi() {
  cr++;
}
function Fi(e6) {
  if (!(Le(e6) && !e6.dirty) && !(!e6.dirty && e6.lastCleanEpoch === cr)) {
    if (!e6.producerMustRecompute(e6) && !fr(e6)) {
      ar(e6);
      return;
    }
    e6.producerRecomputeValue(e6), ar(e6);
  }
}
function lr(e6) {
  if (e6.consumers === void 0)
    return;
  let t = zt;
  zt = true;
  try {
    for (let n = e6.consumers; n !== void 0; n = n.nextConsumer) {
      let r = n.consumer;
      r.dirty || al(r);
    }
  } finally {
    zt = t;
  }
}
function ur() {
  return b?.consumerAllowSignalWrites !== false;
}
function al(e6) {
  e6.dirty = true, lr(e6), e6.consumerMarkedDirty?.(e6);
}
function ar(e6) {
  e6.dirty = false, e6.lastCleanEpoch = cr;
}
function dr(e6) {
  return e6 && ji(e6), v(e6);
}
function ji(e6) {
  e6.producersTail = void 0, e6.recomputing = true;
}
function Hi(e6, t) {
  v(t), e6 && Vi(e6);
}
function Vi(e6) {
  e6.recomputing = false;
  let t = e6.producersTail, n = t !== void 0 ? t.nextProducer : e6.producers;
  if (n !== void 0) {
    if (Le(e6))
      do
        n = pr(n);
      while (n !== void 0);
    t !== void 0 ? t.nextProducer = void 0 : e6.producers = void 0;
  }
}
function fr(e6) {
  for (let t = e6.producers; t !== void 0; t = t.nextProducer) {
    let n = t.producer, r = t.lastReadVersion;
    if (r !== n.version || (Fi(n), r !== n.version))
      return true;
  }
  return false;
}
function qt(e6) {
  if (Le(e6)) {
    let t = e6.producers;
    for (; t !== void 0; )
      t = pr(t);
  }
  e6.producers = void 0, e6.producersTail = void 0, e6.consumers = void 0, e6.consumersTail = void 0;
}
function Bi(e6, t) {
  let n = e6.consumersTail, r = Le(e6);
  if (n !== void 0 ? (t.nextConsumer = n.nextConsumer, n.nextConsumer = t) : (t.nextConsumer = void 0, e6.consumers = t), t.prevConsumer = n, e6.consumersTail = t, !r)
    for (let o = e6.producers; o !== void 0; o = o.nextProducer)
      Bi(o.producer, o);
}
function pr(e6) {
  let t = e6.producer, n = e6.nextProducer, r = e6.nextConsumer, o = e6.prevConsumer;
  if (e6.nextConsumer = void 0, e6.prevConsumer = void 0, r !== void 0 ? r.prevConsumer = o : t.consumersTail = o, o !== void 0)
    o.nextConsumer = r;
  else if (t.consumers = r, !Le(t)) {
    let i = t.producers;
    for (; i !== void 0; )
      i = pr(i);
  }
  return n;
}
function Le(e6) {
  return e6.consumerIsAlwaysLive || e6.consumers !== void 0;
}
function $i(e6) {
  sl?.(e6);
}
function cl(e6, t) {
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
function Ui(e6, t) {
  return Object.is(e6, t);
}
function ll() {
  throw new Error();
}
var zi = ll;
function Wi(e6) {
  zi(e6);
}
function hr(e6) {
  zi = e6;
}
var ul = null;
function gr(e6, t) {
  let n = Object.create(Zi);
  n.value = e6, t !== void 0 && (n.equal = t);
  let r = () => Gi(n);
  return r[W] = n, $i(n), [r, (s) => mr(n, s), (s) => qi(n, s)];
}
function Gi(e6) {
  return Li(e6), e6.value;
}
function mr(e6, t) {
  ur() || Wi(e6), e6.equal(e6.value, t) || (e6.value = t, dl(e6));
}
function qi(e6, t) {
  ur() || Wi(e6), mr(e6, t(e6.value));
}
var Zi = V(A({}, Gt), { equal: Ui, value: void 0, kind: "signal" });
function dl(e6) {
  e6.version++, Pi(), lr(e6), ul?.(e6);
}
function N(e6) {
  return typeof e6 == "function";
}
function Zt(e6) {
  let n = e6((r) => {
    Error.call(r), r.stack = new Error().stack;
  });
  return n.prototype = Object.create(Error.prototype), n.prototype.constructor = n, n;
}
var Qt = Zt((e6) => function(n) {
  e6(this), this.message = n ? `${n.length} errors occurred during unsubscription:
${n.map((r, o) => `${o + 1}) ${r.toString()}`).join(`
  `)}` : "", this.name = "UnsubscriptionError", this.errors = n;
});
function ot(e6, t) {
  if (e6) {
    let n = e6.indexOf(t);
    0 <= n && e6.splice(n, 1);
  }
}
var _ = class e {
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
          t = i instanceof Qt ? i.errors : [i];
        }
      let { _finalizers: o } = this;
      if (o) {
        this._finalizers = null;
        for (let i of o)
          try {
            Qi(i);
          } catch (s) {
            t = t ?? [], s instanceof Qt ? t = [...t, ...s.errors] : t.push(s);
          }
      }
      if (t)
        throw new Qt(t);
    }
  }
  add(t) {
    var n;
    if (t && t !== this)
      if (this.closed)
        Qi(t);
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
    n === t ? this._parentage = null : Array.isArray(n) && ot(n, t);
  }
  remove(t) {
    let { _finalizers: n } = this;
    n && ot(n, t), t instanceof e && t._removeParent(this);
  }
};
_.EMPTY = (() => {
  let e6 = new _();
  return e6.closed = true, e6;
})();
var yr = _.EMPTY;
function Yt(e6) {
  return e6 instanceof _ || e6 && "closed" in e6 && N(e6.remove) && N(e6.add) && N(e6.unsubscribe);
}
function Qi(e6) {
  N(e6) ? e6() : e6.unsubscribe();
}
var B = { onUnhandledError: null, onStoppedNotification: null, Promise: void 0, useDeprecatedSynchronousErrorHandling: false, useDeprecatedNextContext: false };
var Pe = { setTimeout(e6, t, ...n) {
  let { delegate: r } = Pe;
  return r?.setTimeout ? r.setTimeout(e6, t, ...n) : setTimeout(e6, t, ...n);
}, clearTimeout(e6) {
  let { delegate: t } = Pe;
  return (t?.clearTimeout || clearTimeout)(e6);
}, delegate: void 0 };
function Yi(e6) {
  Pe.setTimeout(() => {
    let { onUnhandledError: t } = B;
    if (t)
      t(e6);
    else
      throw e6;
  });
}
function vr() {
}
var Ki = Er("C", void 0, void 0);
function Ji(e6) {
  return Er("E", void 0, e6);
}
function Xi(e6) {
  return Er("N", e6, void 0);
}
function Er(e6, t, n) {
  return { kind: e6, value: t, error: n };
}
var ve = null;
function Fe(e6) {
  if (B.useDeprecatedSynchronousErrorHandling) {
    let t = !ve;
    if (t && (ve = { errorThrown: false, error: null }), e6(), t) {
      let { errorThrown: n, error: r } = ve;
      if (ve = null, n)
        throw r;
    }
  } else
    e6();
}
function es(e6) {
  B.useDeprecatedSynchronousErrorHandling && ve && (ve.errorThrown = true, ve.error = e6);
}
var Ee = class extends _ {
  constructor(t) {
    super(), this.isStopped = false, t ? (this.destination = t, Yt(t) && t.add(this)) : this.destination = hl;
  }
  static create(t, n, r) {
    return new je(t, n, r);
  }
  next(t) {
    this.isStopped ? Dr(Xi(t), this) : this._next(t);
  }
  error(t) {
    this.isStopped ? Dr(Ji(t), this) : (this.isStopped = true, this._error(t));
  }
  complete() {
    this.isStopped ? Dr(Ki, this) : (this.isStopped = true, this._complete());
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
var fl = Function.prototype.bind;
function Ir(e6, t) {
  return fl.call(e6, t);
}
var wr = class {
  constructor(t) {
    this.partialObserver = t;
  }
  next(t) {
    let { partialObserver: n } = this;
    if (n.next)
      try {
        n.next(t);
      } catch (r) {
        Kt(r);
      }
  }
  error(t) {
    let { partialObserver: n } = this;
    if (n.error)
      try {
        n.error(t);
      } catch (r) {
        Kt(r);
      }
    else
      Kt(t);
  }
  complete() {
    let { partialObserver: t } = this;
    if (t.complete)
      try {
        t.complete();
      } catch (n) {
        Kt(n);
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
      this && B.useDeprecatedNextContext ? (i = Object.create(t), i.unsubscribe = () => this.unsubscribe(), o = { next: t.next && Ir(t.next, i), error: t.error && Ir(t.error, i), complete: t.complete && Ir(t.complete, i) }) : o = t;
    }
    this.destination = new wr(o);
  }
};
function Kt(e6) {
  B.useDeprecatedSynchronousErrorHandling ? es(e6) : Yi(e6);
}
function pl(e6) {
  throw e6;
}
function Dr(e6, t) {
  let { onStoppedNotification: n } = B;
  n && Pe.setTimeout(() => n(e6, t));
}
var hl = { closed: true, next: vr, error: pl, complete: vr };
var ts = typeof Symbol == "function" && Symbol.observable || "@@observable";
function ns(e6) {
  return e6;
}
function rs(e6) {
  return e6.length === 0 ? ns : e6.length === 1 ? e6[0] : function(n) {
    return e6.reduce((r, o) => o(r), n);
  };
}
var He = (() => {
  class e6 {
    constructor(n) {
      n && (this._subscribe = n);
    }
    lift(n) {
      let r = new e6();
      return r.source = this, r.operator = n, r;
    }
    subscribe(n, r, o) {
      let i = ml(n) ? n : new je(n, r, o);
      return Fe(() => {
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
      return r = os(r), new r((o, i) => {
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
    [ts]() {
      return this;
    }
    pipe(...n) {
      return rs(n)(this);
    }
    toPromise(n) {
      return n = os(n), new n((r, o) => {
        let i;
        this.subscribe((s) => i = s, (s) => o(s), () => r(i));
      });
    }
  }
  return e6.create = (t) => new e6(t), e6;
})();
function os(e6) {
  var t;
  return (t = e6 ?? B.Promise) !== null && t !== void 0 ? t : Promise;
}
function gl(e6) {
  return e6 && N(e6.next) && N(e6.error) && N(e6.complete);
}
function ml(e6) {
  return e6 && e6 instanceof Ee || gl(e6) && Yt(e6);
}
function yl(e6) {
  return N(e6?.lift);
}
function is(e6) {
  return (t) => {
    if (yl(t))
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
function ss(e6, t, n, r, o) {
  return new Cr(e6, t, n, r, o);
}
var Cr = class extends Ee {
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
var as = Zt((e6) => function() {
  e6(this), this.name = "ObjectUnsubscribedError", this.message = "object unsubscribed";
});
var ae = (() => {
  class e6 extends He {
    constructor() {
      super(), this.closed = false, this.currentObservers = null, this.observers = [], this.isStopped = false, this.hasError = false, this.thrownError = null;
    }
    lift(n) {
      let r = new Jt(this, this);
      return r.operator = n, r;
    }
    _throwIfClosed() {
      if (this.closed)
        throw new as();
    }
    next(n) {
      Fe(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.currentObservers || (this.currentObservers = Array.from(this.observers));
          for (let r of this.currentObservers)
            r.next(n);
        }
      });
    }
    error(n) {
      Fe(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.hasError = this.isStopped = true, this.thrownError = n;
          let { observers: r } = this;
          for (; r.length; )
            r.shift().error(n);
        }
      });
    }
    complete() {
      Fe(() => {
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
      return r || o ? yr : (this.currentObservers = null, i.push(n), new _(() => {
        this.currentObservers = null, ot(i, n);
      }));
    }
    _checkFinalizedStatuses(n) {
      let { hasError: r, thrownError: o, isStopped: i } = this;
      r ? n.error(o) : i && n.complete();
    }
    asObservable() {
      let n = new He();
      return n.source = this, n;
    }
  }
  return e6.create = (t, n) => new Jt(t, n), e6;
})();
var Jt = class extends ae {
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
    return (r = (n = this.source) === null || n === void 0 ? void 0 : n.subscribe(t)) !== null && r !== void 0 ? r : yr;
  }
};
var it = class extends ae {
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
function Tr(e6, t) {
  return is((n, r) => {
    let o = 0;
    n.subscribe(ss(r, (i) => {
      r.next(e6.call(t, i, o++));
    }));
  });
}
var Mr;
function Xt() {
  return Mr;
}
function G(e6) {
  let t = Mr;
  return Mr = e6, t;
}
var cs = Symbol("NotFound");
function Ve(e6) {
  return e6 === cs || e6?.name === "\u0275NotFound";
}
var sn = "https://angular.dev/best-practices/security#preventing-cross-site-scripting-xss";
var g = class extends Error {
  code;
  constructor(t, n) {
    super(an(t, n)), this.code = t;
  }
};
function Dl(e6) {
  return `NG0${Math.abs(e6)}`;
}
function an(e6, t) {
  return `${Dl(e6)}${t ? ": " + t : ""}`;
}
var ce = globalThis;
function C(e6) {
  for (let t in e6)
    if (e6[t] === C)
      return t;
  throw Error("");
}
function Br(e6, t) {
  return e6 ? t ? `${e6} ${t}` : e6 : t || "";
}
var wl = C({ __forward_ref__: C });
function cn(e6) {
  return e6.__forward_ref__ = cn, e6;
}
function k(e6) {
  return ps(e6) ? e6() : e6;
}
function ps(e6) {
  return typeof e6 == "function" && e6.hasOwnProperty(wl) && e6.__forward_ref__ === cn;
}
function S(e6) {
  return { token: e6.token, providedIn: e6.providedIn || null, factory: e6.factory, value: void 0 };
}
function ln(e6) {
  return Cl(e6, un);
}
function Cl(e6, t) {
  return e6.hasOwnProperty(t) && e6[t] || null;
}
function Tl(e6) {
  let t = e6?.[un] ?? null;
  return t || null;
}
function br(e6) {
  return e6 && e6.hasOwnProperty(tn) ? e6[tn] : null;
}
var un = C({ \u0275prov: C });
var tn = C({ \u0275inj: C });
var m = class {
  _desc;
  ngMetadataName = "InjectionToken";
  \u0275prov;
  constructor(t, n) {
    this._desc = t, this.\u0275prov = void 0, typeof n == "number" ? this.__NG_ELEMENT_ID__ = n : n !== void 0 && (this.\u0275prov = S({ token: this, providedIn: n.providedIn || "root", factory: n.factory }));
  }
  get multi() {
    return this;
  }
  toString() {
    return `InjectionToken ${this._desc}`;
  }
};
function $r(e6) {
  return e6 && !!e6.\u0275providers;
}
var Ur = C({ \u0275cmp: C });
var zr = C({ \u0275dir: C });
var Wr = C({ \u0275pipe: C });
var _r = C({ \u0275fac: C });
var Me = C({ __NG_ELEMENT_ID__: C });
var ls = C({ __NG_ENV_ID__: C });
function ut(e6) {
  return qr(e6, "@Component"), e6[Ur] || null;
}
function Gr(e6) {
  return qr(e6, "@Directive"), e6[zr] || null;
}
function hs(e6) {
  return qr(e6, "@Pipe"), e6[Wr] || null;
}
function qr(e6, t) {
  if (e6 == null)
    throw new g(-919, false);
}
function Zr(e6) {
  return typeof e6 == "string" ? e6 : e6 == null ? "" : String(e6);
}
var gs = C({ ngErrorCode: C });
var Ml = C({ ngErrorMessage: C });
var Sl = C({ ngTokenPath: C });
function Qr(e6, t) {
  return ms("", -200, t);
}
function dn(e6, t) {
  throw new g(-201, false);
}
function ms(e6, t, n) {
  let r = new g(t, e6);
  return r[gs] = t, r[Ml] = e6, n && (r[Sl] = n), r;
}
function bl(e6) {
  return e6[gs];
}
var Nr;
function ys() {
  return Nr;
}
function R(e6) {
  let t = Nr;
  return Nr = e6, t;
}
function Yr(e6, t, n) {
  let r = ln(e6);
  if (r && r.providedIn == "root")
    return r.value === void 0 ? r.value = r.factory() : r.value;
  if (n & 8)
    return null;
  if (t !== void 0)
    return t;
  dn(e6, "");
}
var _l = {};
var Ie = _l;
var Nl = "__NG_DI_FLAG__";
var xr = class {
  injector;
  constructor(t) {
    this.injector = t;
  }
  retrieve(t, n) {
    let r = De(n) || 0;
    try {
      return this.injector.get(t, r & 8 ? null : Ie, r);
    } catch (o) {
      if (Ve(o))
        return o;
      throw o;
    }
  }
};
function xl(e6, t = 0) {
  let n = Xt();
  if (n === void 0)
    throw new g(-203, false);
  if (n === null)
    return Yr(e6, void 0, t);
  {
    let r = Al(t), o = n.retrieve(e6, r);
    if (Ve(o)) {
      if (r.optional)
        return null;
      throw o;
    }
    return o;
  }
}
function I(e6, t = 0) {
  return (ys() || xl)(k(e6), t);
}
function E(e6, t) {
  return I(e6, De(t));
}
function De(e6) {
  return typeof e6 > "u" || typeof e6 == "number" ? e6 : 0 | (e6.optional && 8) | (e6.host && 1) | (e6.self && 2) | (e6.skipSelf && 4);
}
function Al(e6) {
  return { optional: !!(e6 & 8), host: !!(e6 & 1), self: !!(e6 & 2), skipSelf: !!(e6 & 4) };
}
function Ar(e6) {
  let t = [];
  for (let n = 0; n < e6.length; n++) {
    let r = k(e6[n]);
    if (Array.isArray(r)) {
      if (r.length === 0)
        throw new g(900, false);
      let o, i = 0;
      for (let s = 0; s < r.length; s++) {
        let a = r[s], c = Rl(a);
        typeof c == "number" ? c === -1 ? o = a.token : i |= c : o = a;
      }
      t.push(I(o, i));
    } else
      t.push(I(r));
  }
  return t;
}
function Rl(e6) {
  return e6[Nl];
}
function $e(e6, t) {
  let n = e6.hasOwnProperty(_r);
  return n ? e6[_r] : null;
}
function fn(e6, t) {
  e6.forEach((n) => Array.isArray(n) ? fn(n, t) : t(n));
}
function Kr(e6, t) {
  return t >= e6.length - 1 ? e6.pop() : e6.splice(t, 1)[0];
}
var Se = {};
var we = [];
var be = new m("");
var Jr = new m("", -1);
var Xr = new m("");
var at = class {
  get(t, n = Ie) {
    if (n === Ie) {
      let o = ms("", -201);
      throw o.name = "\u0275NotFound", o;
    }
    return n;
  }
};
function dt(e6) {
  return { \u0275providers: e6 };
}
function vs(e6) {
  return dt([{ provide: be, multi: true, useValue: e6 }]);
}
function Es(...e6) {
  return { \u0275providers: eo(true, e6), \u0275fromNgModule: true };
}
function eo(e6, ...t) {
  let n = [], r = /* @__PURE__ */ new Set(), o, i = (s) => {
    n.push(s);
  };
  return fn(t, (s) => {
    let a = s;
    nn(a, i, [], r) && (o ||= [], o.push(a));
  }), o !== void 0 && Is(o, i), n;
}
function Is(e6, t) {
  for (let n = 0; n < e6.length; n++) {
    let { ngModule: r, providers: o } = e6[n];
    to(o, (i) => {
      t(i, r);
    });
  }
}
function nn(e6, t, n, r) {
  if (e6 = k(e6), !e6)
    return false;
  let o = null, i = br(e6), s = !i && ut(e6);
  if (!i && !s) {
    let c = e6.ngModule;
    if (i = br(c), i)
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
      for (let l of c)
        nn(l, t, n, r);
    }
  } else if (i) {
    if (i.imports != null && !a) {
      r.add(o);
      let l;
      fn(i.imports, (u) => {
        nn(u, t, n, r) && (l ||= [], l.push(u));
      }), l !== void 0 && Is(l, t);
    }
    if (!a) {
      let l = $e(o) || (() => new o());
      t({ provide: o, useFactory: l, deps: we }, o), t({ provide: Xr, useValue: o, multi: true }, o), t({ provide: be, useValue: () => I(o), multi: true }, o);
    }
    let c = i.providers;
    if (c != null && !a) {
      let l = e6;
      to(c, (u) => {
        t(u, l);
      });
    }
  } else
    return false;
  return o !== e6 && e6.providers !== void 0;
}
function to(e6, t) {
  for (let n of e6)
    $r(n) && (n = n.\u0275providers), Array.isArray(n) ? to(n, t) : t(n);
}
var kl = C({ provide: String, useValue: C });
function Ds(e6) {
  return e6 !== null && typeof e6 == "object" && kl in e6;
}
function Ol(e6) {
  return !!(e6 && e6.useExisting);
}
function Ll(e6) {
  return !!(e6 && e6.useFactory);
}
function rn(e6) {
  return typeof e6 == "function";
}
var ft = new m("");
var en = {};
var us = {};
var Sr;
function pt() {
  return Sr === void 0 && (Sr = new at()), Sr;
}
var $ = class {
};
var Ce = class extends $ {
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
    super(), this.parent = n, this.source = r, this.scopes = o, kr(t, (s) => this.processProvider(s)), this.records.set(Jr, Be(void 0, this)), o.has("environment") && this.records.set($, Be(void 0, this));
    let i = this.records.get(ft);
    i != null && typeof i.value == "string" && this.scopes.add(i.value), this.injectorDefTypes = new Set(this.get(Xr, we, { self: true }));
  }
  retrieve(t, n) {
    let r = De(n) || 0;
    try {
      return this.get(t, Ie, r);
    } catch (o) {
      if (Ve(o))
        return o;
      throw o;
    }
  }
  destroy() {
    st(this), this._destroyed = true;
    let t = v(null);
    try {
      for (let r of this._ngOnDestroyHooks)
        r.ngOnDestroy();
      let n = this._onDestroyHooks;
      this._onDestroyHooks = [];
      for (let r of n)
        r();
    } finally {
      this.records.clear(), this._ngOnDestroyHooks.clear(), this.injectorDefTypes.clear(), v(t);
    }
  }
  onDestroy(t) {
    return st(this), this._onDestroyHooks.push(t), () => this.removeOnDestroy(t);
  }
  runInContext(t) {
    st(this);
    let n = G(this), r = R(void 0), o;
    try {
      return t();
    } finally {
      G(n), R(r);
    }
  }
  get(t, n = Ie, r) {
    if (st(this), t.hasOwnProperty(ls))
      return t[ls](this);
    let o = De(r), i, s = G(this), a = R(void 0);
    try {
      if (!(o & 4)) {
        let l = this.records.get(t);
        if (l === void 0) {
          let u = Vl(t) && ln(t);
          u && this.injectableDefInScope(u) ? l = Be(Rr(t), en) : l = null, this.records.set(t, l);
        }
        if (l != null)
          return this.hydrate(t, l, o);
      }
      let c = o & 2 ? pt() : this.parent;
      return n = o & 8 && n === Ie ? null : n, c.get(t, n);
    } catch (c) {
      let l = bl(c);
      throw l === -200 || l === -201 ? new g(l, null) : c;
    } finally {
      R(a), G(s);
    }
  }
  resolveInjectorInitializers() {
    let t = v(null), n = G(this), r = R(void 0), o;
    try {
      let i = this.get(be, we, { self: true });
      for (let s of i)
        s();
    } finally {
      G(n), R(r), v(t);
    }
  }
  toString() {
    return "R3Injector[...]";
  }
  processProvider(t) {
    t = k(t);
    let n = rn(t) ? t : k(t && t.provide), r = Fl(t);
    if (!rn(t) && t.multi === true) {
      let o = this.records.get(n);
      o || (o = Be(void 0, en, true), o.factory = () => Ar(o.multi), this.records.set(n, o)), n = t, o.multi.push(t);
    }
    this.records.set(n, r);
  }
  hydrate(t, n, r) {
    let o = v(null);
    try {
      if (n.value === us)
        throw Qr("");
      return n.value === en && (n.value = us, n.value = n.factory(void 0, r)), typeof n.value == "object" && n.value && Hl(n.value) && this._ngOnDestroyHooks.add(n.value), n.value;
    } finally {
      v(o);
    }
  }
  injectableDefInScope(t) {
    if (!t.providedIn)
      return false;
    let n = k(t.providedIn);
    return typeof n == "string" ? n === "any" || this.scopes.has(n) : this.injectorDefTypes.has(n);
  }
  removeOnDestroy(t) {
    let n = this._onDestroyHooks.indexOf(t);
    n !== -1 && this._onDestroyHooks.splice(n, 1);
  }
};
function Rr(e6) {
  let t = ln(e6), n = t !== null ? t.factory : $e(e6);
  if (n !== null)
    return n;
  if (e6 instanceof m)
    throw new g(-204, false);
  if (e6 instanceof Function)
    return Pl(e6);
  throw new g(-204, false);
}
function Pl(e6) {
  if (e6.length > 0)
    throw new g(-204, false);
  let n = Tl(e6);
  return n !== null ? () => n.factory(e6) : () => new e6();
}
function Fl(e6) {
  if (Ds(e6))
    return Be(void 0, e6.useValue);
  {
    let t = ws(e6);
    return Be(t, en);
  }
}
function ws(e6, t, n) {
  let r;
  if (rn(e6)) {
    let o = k(e6);
    return $e(o) || Rr(o);
  } else if (Ds(e6))
    r = () => k(e6.useValue);
  else if (Ll(e6))
    r = () => e6.useFactory(...Ar(e6.deps || []));
  else if (Ol(e6))
    r = (o, i) => I(k(e6.useExisting), i !== void 0 && i & 8 ? 8 : void 0);
  else {
    let o = k(e6 && (e6.useClass || e6.provide));
    if (jl(e6))
      r = () => new o(...Ar(e6.deps));
    else
      return $e(o) || Rr(o);
  }
  return r;
}
function st(e6) {
  if (e6.destroyed)
    throw new g(-205, false);
}
function Be(e6, t, n = false) {
  return { factory: e6, value: t, multi: n ? [] : void 0 };
}
function jl(e6) {
  return !!e6.deps;
}
function Hl(e6) {
  return e6 !== null && typeof e6 == "object" && typeof e6.ngOnDestroy == "function";
}
function Vl(e6) {
  return typeof e6 == "function" || typeof e6 == "object" && e6.ngMetadataName === "InjectionToken";
}
function kr(e6, t) {
  for (let n of e6)
    Array.isArray(n) ? kr(n, t) : n && $r(n) ? kr(n.\u0275providers, t) : t(n);
}
function pn(e6, t) {
  let n;
  e6 instanceof Ce ? (st(e6), n = e6) : n = new xr(e6);
  let r, o = G(n), i = R(void 0);
  try {
    return t();
  } finally {
    G(o), R(i);
  }
}
function Cs() {
  return ys() !== void 0 || Xt() != null;
}
var q = 0;
var y = 1;
var h = 2;
var O = 3;
var ne = 4;
var re = 5;
var hn = 6;
var gn = 7;
var L = 8;
var _e = 9;
var Z = 10;
var P = 11;
var ze = 12;
var no = 13;
var We = 14;
var Q = 15;
var ht = 16;
var Ne = 17;
var mn = 18;
var le = 19;
var ro = 20;
var X = 21;
var yn = 22;
var gt = 23;
var F = 24;
var vn = 25;
var Ge = 26;
var U = 27;
var Ts = 1;
var En = 7;
var Ms = 8;
var mt = 9;
var oe = 10;
function ue(e6) {
  return Array.isArray(e6) && typeof e6[Ts] == "object";
}
function de(e6) {
  return Array.isArray(e6) && e6[Ts] === true;
}
function oo(e6) {
  return (e6.flags & 4) !== 0;
}
function yt(e6) {
  return e6.componentOffset > -1;
}
function Ss(e6) {
  return (e6.flags & 1) === 1;
}
function qe(e6) {
  return !!e6.template;
}
function Ze(e6) {
  return (e6[h] & 512) !== 0;
}
function xe(e6) {
  return (e6[h] & 256) === 256;
}
var bs = "svg";
var _s = "math";
function fe(e6) {
  for (; Array.isArray(e6); )
    e6 = e6[q];
  return e6;
}
function Ns(e6, t) {
  return fe(t[e6]);
}
function Ae(e6, t) {
  return fe(t[e6.index]);
}
function io(e6, t) {
  return e6.data[t];
}
function pe(e6, t) {
  let n = t[e6];
  return ue(n) ? n : n[q];
}
function In(e6) {
  return (e6[h] & 128) === 128;
}
function vt(e6, t) {
  return t == null ? null : e6[t];
}
function so(e6) {
  e6[Ne] = 0;
}
function ao(e6) {
  e6[h] & 1024 || (e6[h] |= 1024, In(e6) && It(e6));
}
function Et(e6) {
  return !!(e6[h] & 9216 || e6[F]?.dirty);
}
function co(e6) {
  e6[Z].changeDetectionScheduler?.notify(8), e6[h] & 64 && (e6[h] |= 1024), Et(e6) && It(e6);
}
function It(e6) {
  e6[Z].changeDetectionScheduler?.notify(0);
  let t = Te(e6);
  for (; t !== null && !(t[h] & 8192 || (t[h] |= 8192, !In(t))); )
    t = Te(t);
}
function lo(e6, t) {
  if (xe(e6))
    throw new g(911, false);
  e6[X] === null && (e6[X] = []), e6[X].push(t);
}
function xs(e6, t) {
  if (e6[X] === null)
    return;
  let n = e6[X].indexOf(t);
  n !== -1 && e6[X].splice(n, 1);
}
function Te(e6) {
  let t = e6[O];
  return de(t) ? t[O] : t;
}
var D = { lFrame: zs(null), bindingsEnabled: true, skipHydrationRootTNode: null };
var Or = false;
function As() {
  return D.lFrame.elementDepthCount;
}
function Rs() {
  D.lFrame.elementDepthCount++;
}
function ks() {
  D.lFrame.elementDepthCount--;
}
function Os() {
  return D.skipHydrationRootTNode !== null;
}
function Ls(e6) {
  return D.skipHydrationRootTNode === e6;
}
function Ps() {
  D.skipHydrationRootTNode = null;
}
function H() {
  return D.lFrame.lView;
}
function Dn() {
  return D.lFrame.tView;
}
function Qe() {
  let e6 = uo();
  for (; e6 !== null && e6.type === 64; )
    e6 = e6.parent;
  return e6;
}
function uo() {
  return D.lFrame.currentTNode;
}
function Fs() {
  let e6 = D.lFrame, t = e6.currentTNode;
  return e6.isParent ? t : t.parent;
}
function Dt(e6, t) {
  let n = D.lFrame;
  n.currentTNode = e6, n.isParent = t;
}
function fo() {
  return D.lFrame.isParent;
}
function js() {
  D.lFrame.isParent = false;
}
function po() {
  return Or;
}
function ho(e6) {
  let t = Or;
  return Or = e6, t;
}
function Hs(e6) {
  return D.lFrame.bindingIndex = e6;
}
function go() {
  return D.lFrame.bindingIndex++;
}
function Vs() {
  return D.lFrame.inI18n;
}
function Bs(e6, t) {
  let n = D.lFrame;
  n.bindingIndex = n.bindingRootIndex = e6, wn(t);
}
function $s() {
  return D.lFrame.currentDirectiveIndex;
}
function wn(e6) {
  D.lFrame.currentDirectiveIndex = e6;
}
function mo(e6) {
  D.lFrame.currentQueryIndex = e6;
}
function Bl(e6) {
  let t = e6[y];
  return t.type === 2 ? t.declTNode : t.type === 1 ? e6[re] : null;
}
function yo(e6, t, n) {
  if (n & 4) {
    let o = t, i = e6;
    for (; o = o.parent, o === null && !(n & 1); )
      if (o = Bl(i), o === null || (i = i[We], o.type & 10))
        break;
    if (o === null)
      return false;
    t = o, e6 = i;
  }
  let r = D.lFrame = Us();
  return r.currentTNode = t, r.lView = e6, true;
}
function Cn(e6) {
  let t = Us(), n = e6[y];
  D.lFrame = t, t.currentTNode = n.firstChild, t.lView = e6, t.tView = n, t.contextLView = e6, t.bindingIndex = n.bindingStartIndex, t.inI18n = false;
}
function Us() {
  let e6 = D.lFrame, t = e6 === null ? null : e6.child;
  return t === null ? zs(e6) : t;
}
function zs(e6) {
  let t = { currentTNode: null, isParent: true, lView: null, tView: null, selectedIndex: -1, contextLView: null, elementDepthCount: 0, currentNamespace: null, currentDirectiveIndex: -1, bindingRootIndex: -1, bindingIndex: -1, currentQueryIndex: 0, parent: e6, child: null, inI18n: false };
  return e6 !== null && (e6.child = t), t;
}
function Ws() {
  let e6 = D.lFrame;
  return D.lFrame = e6.parent, e6.currentTNode = null, e6.lView = null, e6;
}
var vo = Ws;
function Tn() {
  let e6 = Ws();
  e6.isParent = true, e6.tView = null, e6.selectedIndex = -1, e6.contextLView = null, e6.elementDepthCount = 0, e6.currentDirectiveIndex = -1, e6.currentNamespace = null, e6.bindingRootIndex = -1, e6.bindingIndex = -1, e6.currentQueryIndex = 0;
}
function Mn() {
  return D.lFrame.selectedIndex;
}
function he(e6) {
  D.lFrame.selectedIndex = e6;
}
function Gs() {
  let e6 = D.lFrame;
  return io(e6.tView, e6.selectedIndex);
}
function qs() {
  return D.lFrame.currentNamespace;
}
var Zs = true;
function Eo() {
  return Zs;
}
function Io(e6) {
  Zs = e6;
}
function Lr(e6, t = null, n = null, r) {
  let o = Qs(e6, t, n, r);
  return o.resolveInjectorInitializers(), o;
}
function Qs(e6, t = null, n = null, r, o = /* @__PURE__ */ new Set()) {
  let i = [n || we, Es(e6)], s;
  return new Ce(i, t || pt(), s || null, o);
}
var ee = class e2 {
  static THROW_IF_NOT_FOUND = Ie;
  static NULL = new at();
  static create(t, n) {
    if (Array.isArray(t))
      return Lr({ name: "" }, n, t, "");
    {
      let r = t.name ?? "";
      return Lr({ name: r }, t.parent, t.providers, r);
    }
  }
  static \u0275prov = S({ token: e2, providedIn: "any", factory: () => I(Jr) });
  static __NG_ELEMENT_ID__ = -1;
};
var x = new m("");
var wt = /* @__PURE__ */ (() => {
  class e6 {
    static __NG_ELEMENT_ID__ = $l;
    static __NG_ENV_ID__ = (n) => n;
  }
  return e6;
})();
var Pr = class extends wt {
  _lView;
  constructor(t) {
    super(), this._lView = t;
  }
  get destroyed() {
    return xe(this._lView);
  }
  onDestroy(t) {
    let n = this._lView;
    return lo(n, t), () => xs(n, t);
  }
};
function $l() {
  return new Pr(H());
}
var Ys = false;
var Ks = new m("");
var Ye = (() => {
  class e6 {
    taskId = 0;
    pendingTasks = /* @__PURE__ */ new Set();
    destroyed = false;
    pendingTask = new it(false);
    debugTaskTracker = E(Ks, { optional: true });
    get hasPendingTasks() {
      return this.destroyed ? false : this.pendingTask.value;
    }
    get hasPendingTasksObservable() {
      return this.destroyed ? new He((n) => {
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
    static \u0275prov = S({ token: e6, providedIn: "root", factory: () => new e6() });
  }
  return e6;
})();
var Fr = class extends ae {
  __isAsync;
  destroyRef = void 0;
  pendingTasks = void 0;
  constructor(t = false) {
    super(), this.__isAsync = t, Cs() && (this.destroyRef = E(wt, { optional: true }) ?? void 0, this.pendingTasks = E(Ye, { optional: true }) ?? void 0);
  }
  emit(t) {
    let n = v(null);
    try {
      super.next(t);
    } finally {
      v(n);
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
    return t instanceof _ && t.add(a), a;
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
var J = Fr;
function on(...e6) {
}
function Do(e6) {
  let t, n;
  function r() {
    e6 = on;
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
function Js(e6) {
  return queueMicrotask(() => e6()), () => {
    e6 = on;
  };
}
var wo = "isAngularZone";
var ct = wo + "_ID";
var Ul = 0;
var j = class e3 {
  hasPendingMacrotasks = false;
  hasPendingMicrotasks = false;
  isStable = true;
  onUnstable = new J(false);
  onMicrotaskEmpty = new J(false);
  onStable = new J(false);
  onError = new J(false);
  constructor(t) {
    let { enableLongStackTrace: n = false, shouldCoalesceEventChangeDetection: r = false, shouldCoalesceRunChangeDetection: o = false, scheduleInRootZone: i = Ys } = t;
    if (typeof Zone > "u")
      throw new g(908, false);
    Zone.assertZonePatched();
    let s = this;
    s._nesting = 0, s._outer = s._inner = Zone.current, Zone.TaskTrackingZoneSpec && (s._inner = s._inner.fork(new Zone.TaskTrackingZoneSpec())), n && Zone.longStackTraceZoneSpec && (s._inner = s._inner.fork(Zone.longStackTraceZoneSpec)), s.shouldCoalesceEventChangeDetection = !o && r, s.shouldCoalesceRunChangeDetection = o, s.callbackScheduled = false, s.scheduleInRootZone = i, Gl(s);
  }
  static isInAngularZone() {
    return typeof Zone < "u" && Zone.current.get(wo) === true;
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
    let i = this._inner, s = i.scheduleEventTask("NgZoneEvent: " + o, t, zl, on, on);
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
var zl = {};
function Co(e6) {
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
function Wl(e6) {
  if (e6.isCheckStableRunning || e6.callbackScheduled)
    return;
  e6.callbackScheduled = true;
  function t() {
    Do(() => {
      e6.callbackScheduled = false, jr(e6), e6.isCheckStableRunning = true, Co(e6), e6.isCheckStableRunning = false;
    });
  }
  e6.scheduleInRootZone ? Zone.root.run(() => {
    t();
  }) : e6._outer.run(() => {
    t();
  }), jr(e6);
}
function Gl(e6) {
  let t = () => {
    Wl(e6);
  }, n = Ul++;
  e6._inner = e6._inner.fork({ name: "angular", properties: { [wo]: true, [ct]: n, [ct + n]: true }, onInvokeTask: (r, o, i, s, a, c) => {
    if (ql(c))
      return r.invokeTask(i, s, a, c);
    try {
      return ds(e6), r.invokeTask(i, s, a, c);
    } finally {
      (e6.shouldCoalesceEventChangeDetection && s.type === "eventTask" || e6.shouldCoalesceRunChangeDetection) && t(), fs(e6);
    }
  }, onInvoke: (r, o, i, s, a, c, l) => {
    try {
      return ds(e6), r.invoke(i, s, a, c, l);
    } finally {
      e6.shouldCoalesceRunChangeDetection && !e6.callbackScheduled && !Zl(c) && t(), fs(e6);
    }
  }, onHasTask: (r, o, i, s) => {
    r.hasTask(i, s), o === i && (s.change == "microTask" ? (e6._hasPendingMicrotasks = s.microTask, jr(e6), Co(e6)) : s.change == "macroTask" && (e6.hasPendingMacrotasks = s.macroTask));
  }, onHandleError: (r, o, i, s) => (r.handleError(i, s), e6.runOutsideAngular(() => e6.onError.emit(s)), false) });
}
function jr(e6) {
  e6._hasPendingMicrotasks || (e6.shouldCoalesceEventChangeDetection || e6.shouldCoalesceRunChangeDetection) && e6.callbackScheduled === true ? e6.hasPendingMicrotasks = true : e6.hasPendingMicrotasks = false;
}
function ds(e6) {
  e6._nesting++, e6.isStable && (e6.isStable = false, e6.onUnstable.emit(null));
}
function fs(e6) {
  e6._nesting--, Co(e6);
}
var lt = class {
  hasPendingMicrotasks = false;
  hasPendingMacrotasks = false;
  isStable = true;
  onUnstable = new J();
  onMicrotaskEmpty = new J();
  onStable = new J();
  onError = new J();
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
function ql(e6) {
  return Xs(e6, "__ignore_ng_zone__");
}
function Zl(e6) {
  return Xs(e6, "__scheduler_tick__");
}
function Xs(e6, t) {
  return !Array.isArray(e6) || e6.length !== 1 ? false : e6[0]?.data?.[t] === true;
}
var te = class {
  _console = console;
  handleError(t) {
    this._console.error("ERROR", t);
  }
};
var Ke = new m("", { factory: () => {
  let e6 = E(j), t = E($), n;
  return (r) => {
    e6.runOutsideAngular(() => {
      t.destroyed && !n ? setTimeout(() => {
        throw r;
      }) : (n ??= t.get(te), n.handleError(r));
    });
  };
} });
var ea = { provide: be, useValue: () => {
  let e6 = E(te, { optional: true });
}, multi: true };
var Ql = new m("", { factory: () => {
  let e6 = E(x).defaultView;
  if (!e6)
    return;
  let t = E(Ke), n = (i) => {
    t(i.reason), i.preventDefault();
  }, r = (i) => {
    i.error ? t(i.error) : t(new Error(i.message, { cause: i })), i.preventDefault();
  }, o = () => {
    e6.addEventListener("unhandledrejection", n), e6.addEventListener("error", r);
  };
  typeof Zone < "u" ? Zone.root.run(o) : o(), E(wt).onDestroy(() => {
    e6.removeEventListener("error", r), e6.removeEventListener("unhandledrejection", n);
  });
} });
function To() {
  return dt([vs(() => {
    E(Ql);
  })]);
}
function Ct(e6, t) {
  let [n, r, o] = gr(e6, t?.equal), i = n, s = i[W];
  return i.set = r, i.update = o, i.asReadonly = ta.bind(i), i;
}
function ta() {
  let e6 = this[W];
  if (e6.readonlyFn === void 0) {
    let t = () => this();
    t[W] = e6, e6.readonlyFn = t;
  }
  return e6.readonlyFn;
}
var Ue = class {
};
var Tt = new m("", { factory: () => true });
var Mo = new m("");
var So = (() => {
  class e6 {
    static \u0275prov = S({ token: e6, providedIn: "root", factory: () => new Hr() });
  }
  return e6;
})();
var Hr = class {
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
var Vr = class {
  [W];
  constructor(t) {
    this[W] = t;
  }
  destroy() {
    this[W].destroy();
  }
};
function Ma(e6) {
  return { toString: e6 }.toString();
}
function Sa(e6, t, n, r) {
  t !== null ? t.applyValueToInputSignal(t, r) : e6[n] = r;
}
var Rn = class {
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
function fu(e6) {
  return e6.type.prototype.ngOnChanges && (e6.setInput = hu), pu;
}
function pu() {
  let e6 = _a(this), t = e6?.current;
  if (t) {
    let n = e6.previous;
    if (n === Se)
      e6.previous = t;
    else
      for (let r in t)
        n[r] = t[r];
    e6.current = null, this.ngOnChanges(t);
  }
}
function hu(e6, t, n, r, o) {
  let i = this.declaredInputs[r], s = _a(e6) || gu(e6, { previous: Se, current: null }), a = s.current || (s.current = {}), c = s.previous, l = c[i];
  a[i] = new Rn(l && l.currentValue, n, c === Se), Sa(e6, t, o, n);
}
var ba = "__ngSimpleChanges__";
function _a(e6) {
  return e6[ba] || null;
}
function gu(e6, t) {
  return e6[ba] = t;
}
var na = [];
var M = function(e6, t = null, n) {
  for (let r = 0; r < na.length; r++) {
    let o = na[r];
    o(e6, t, n);
  }
};
var w = function(e6) {
  return e6[e6.TemplateCreateStart = 0] = "TemplateCreateStart", e6[e6.TemplateCreateEnd = 1] = "TemplateCreateEnd", e6[e6.TemplateUpdateStart = 2] = "TemplateUpdateStart", e6[e6.TemplateUpdateEnd = 3] = "TemplateUpdateEnd", e6[e6.LifecycleHookStart = 4] = "LifecycleHookStart", e6[e6.LifecycleHookEnd = 5] = "LifecycleHookEnd", e6[e6.OutputStart = 6] = "OutputStart", e6[e6.OutputEnd = 7] = "OutputEnd", e6[e6.BootstrapApplicationStart = 8] = "BootstrapApplicationStart", e6[e6.BootstrapApplicationEnd = 9] = "BootstrapApplicationEnd", e6[e6.BootstrapComponentStart = 10] = "BootstrapComponentStart", e6[e6.BootstrapComponentEnd = 11] = "BootstrapComponentEnd", e6[e6.ChangeDetectionStart = 12] = "ChangeDetectionStart", e6[e6.ChangeDetectionEnd = 13] = "ChangeDetectionEnd", e6[e6.ChangeDetectionSyncStart = 14] = "ChangeDetectionSyncStart", e6[e6.ChangeDetectionSyncEnd = 15] = "ChangeDetectionSyncEnd", e6[e6.AfterRenderHooksStart = 16] = "AfterRenderHooksStart", e6[e6.AfterRenderHooksEnd = 17] = "AfterRenderHooksEnd", e6[e6.ComponentStart = 18] = "ComponentStart", e6[e6.ComponentEnd = 19] = "ComponentEnd", e6[e6.DeferBlockStateStart = 20] = "DeferBlockStateStart", e6[e6.DeferBlockStateEnd = 21] = "DeferBlockStateEnd", e6[e6.DynamicComponentStart = 22] = "DynamicComponentStart", e6[e6.DynamicComponentEnd = 23] = "DynamicComponentEnd", e6[e6.HostBindingsUpdateStart = 24] = "HostBindingsUpdateStart", e6[e6.HostBindingsUpdateEnd = 25] = "HostBindingsUpdateEnd", e6;
}(w || {});
function mu(e6, t, n) {
  let { ngOnChanges: r, ngOnInit: o, ngDoCheck: i } = t.type.prototype;
  if (r) {
    let s = fu(t);
    (n.preOrderHooks ??= []).push(e6, s), (n.preOrderCheckHooks ??= []).push(e6, s);
  }
  o && (n.preOrderHooks ??= []).push(0 - e6, o), i && ((n.preOrderHooks ??= []).push(e6, i), (n.preOrderCheckHooks ??= []).push(e6, i));
}
function yu(e6, t) {
  for (let n = t.directiveStart, r = t.directiveEnd; n < r; n++) {
    let i = e6.data[n].type.prototype, { ngAfterContentInit: s, ngAfterContentChecked: a, ngAfterViewInit: c, ngAfterViewChecked: l, ngOnDestroy: u } = i;
    s && (e6.contentHooks ??= []).push(-n, s), a && ((e6.contentHooks ??= []).push(n, a), (e6.contentCheckHooks ??= []).push(n, a)), c && (e6.viewHooks ??= []).push(-n, c), l && ((e6.viewHooks ??= []).push(n, l), (e6.viewCheckHooks ??= []).push(n, l)), u != null && (e6.destroyHooks ??= []).push(n, u);
  }
}
function Nn(e6, t, n) {
  Na(e6, t, 3, n);
}
function xn(e6, t, n, r) {
  (e6[h] & 3) === n && Na(e6, t, n, r);
}
function bo(e6, t) {
  let n = e6[h];
  (n & 3) === t && (n &= 16383, n += 1, e6[h] = n);
}
function Na(e6, t, n, r) {
  let o = r !== void 0 ? e6[Ne] & 65535 : 0, i = r ?? -1, s = t.length - 1, a = 0;
  for (let c = o; c < s; c++)
    if (typeof t[c + 1] == "number") {
      if (a = t[c], r != null && a >= r)
        break;
    } else
      t[c] < 0 && (e6[Ne] += 65536), (a < i || i == -1) && (vu(e6, n, t, c), e6[Ne] = (e6[Ne] & 4294901760) + c + 2), c++;
}
function ra(e6, t) {
  M(w.LifecycleHookStart, e6, t);
  let n = v(null);
  try {
    t.call(e6);
  } finally {
    v(n), M(w.LifecycleHookEnd, e6, t);
  }
}
function vu(e6, t, n, r) {
  let o = n[r] < 0, i = n[r + 1], s = o ? -n[r] : n[r], a = e6[s];
  o ? e6[h] >> 14 < e6[Ne] >> 16 && (e6[h] & 3) === t && (e6[h] += 16384, ra(a, i)) : ra(a, i);
}
var Xe = -1;
var bt = class {
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
function Eu(e6, t, n) {
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
      Iu(i) ? e6.setProperty(t, i, s) : e6.setAttribute(t, i, s), r++;
    }
  }
  return r;
}
function Iu(e6) {
  return e6.charCodeAt(0) === 64;
}
function ti(e6, t) {
  if (!(t === null || t.length === 0))
    if (e6 === null || e6.length === 0)
      e6 = t.slice();
    else {
      let n = -1;
      for (let r = 0; r < t.length; r++) {
        let o = t[r];
        typeof o == "number" ? n = o : n === 0 || (n === -1 || n === 2 ? oa(e6, n, o, null, t[++r]) : oa(e6, n, o, null, null));
      }
    }
  return e6;
}
function oa(e6, t, n, r, o) {
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
function Du(e6) {
  return e6 !== Xe;
}
function xo(e6) {
  return e6 & 32767;
}
function wu(e6) {
  return e6 >> 16;
}
function Ao(e6, t) {
  let n = wu(e6), r = t;
  for (; n > 0; )
    r = r[We], n--;
  return r;
}
var Ro = true;
function ia(e6) {
  let t = Ro;
  return Ro = e6, t;
}
var Cu = 256;
var xa = Cu - 1;
var Aa = 5;
var Tu = 0;
var Y = {};
function Mu(e6, t, n) {
  let r;
  typeof n == "string" ? r = n.charCodeAt(0) || 0 : n.hasOwnProperty(Me) && (r = n[Me]), r == null && (r = n[Me] = Tu++);
  let o = r & xa, i = 1 << o;
  t.data[e6 + (o >> Aa)] |= i;
}
function Ra(e6, t) {
  let n = ka(e6, t);
  if (n !== -1)
    return n;
  let r = t[y];
  r.firstCreatePass && (e6.injectorIndex = t.length, _o(r.data, e6), _o(t, null), _o(r.blueprint, null));
  let o = Oa(e6, t), i = e6.injectorIndex;
  if (Du(o)) {
    let s = xo(o), a = Ao(o, t), c = a[y].data;
    for (let l = 0; l < 8; l++)
      t[i + l] = a[s + l] | c[s + l];
  }
  return t[i + 8] = o, i;
}
function _o(e6, t) {
  e6.push(0, 0, 0, 0, 0, 0, 0, 0, t);
}
function ka(e6, t) {
  return e6.injectorIndex === -1 || e6.parent && e6.parent.injectorIndex === e6.injectorIndex || t[e6.injectorIndex + 8] === null ? -1 : e6.injectorIndex;
}
function Oa(e6, t) {
  if (e6.parent && e6.parent.injectorIndex !== -1)
    return e6.parent.injectorIndex;
  let n = 0, r = null, o = t;
  for (; o !== null; ) {
    if (r = Ha(o), r === null)
      return Xe;
    if (n++, o = o[We], r.injectorIndex !== -1)
      return r.injectorIndex | n << 16;
  }
  return Xe;
}
function Su(e6, t, n) {
  Mu(e6, t, n);
}
function La(e6, t, n) {
  if (n & 8 || e6 !== void 0)
    return e6;
  dn(t, "NodeInjector");
}
function Pa(e6, t, n, r) {
  if (n & 8 && r === void 0 && (r = null), (n & 3) === 0) {
    let o = e6[_e], i = R(void 0);
    try {
      return o ? o.get(t, r, n & 8) : Yr(t, r, n & 8);
    } finally {
      R(i);
    }
  }
  return La(r, t, n);
}
function Fa(e6, t, n, r = 0, o) {
  if (e6 !== null) {
    if (t[h] & 2048 && !(r & 2)) {
      let s = Au(e6, t, n, r, Y);
      if (s !== Y)
        return s;
    }
    let i = ja(e6, t, n, r, Y);
    if (i !== Y)
      return i;
  }
  return Pa(t, n, r, o);
}
function ja(e6, t, n, r, o) {
  let i = Nu(n);
  if (typeof i == "function") {
    if (!yo(t, e6, r))
      return r & 1 ? La(o, n, r) : Pa(t, n, r, o);
    try {
      let s;
      if (s = i(r), s == null && !(r & 8))
        dn(n);
      else
        return s;
    } finally {
      vo();
    }
  } else if (typeof i == "number") {
    let s = null, a = ka(e6, t), c = Xe, l = r & 1 ? t[Q][re] : null;
    for ((a === -1 || r & 4) && (c = a === -1 ? Oa(e6, t) : t[a + 8], c === Xe || !aa(r, false) ? a = -1 : (s = t[y], a = xo(c), t = Ao(c, t))); a !== -1; ) {
      let u = t[y];
      if (sa(i, a, u.data)) {
        let d = bu(a, t, n, s, r, l);
        if (d !== Y)
          return d;
      }
      c = t[a + 8], c !== Xe && aa(r, t[y].data[a + 8] === l) && sa(i, a, t) ? (s = u, a = xo(c), t = Ao(c, t)) : a = -1;
    }
  }
  return o;
}
function bu(e6, t, n, r, o, i) {
  let s = t[y], a = s.data[e6 + 8], c = r == null ? yt(a) && Ro : r != s && (a.type & 3) !== 0, l = o & 1 && i === a, u = _u(a, s, n, c, l);
  return u !== null ? ko(t, s, u, a, o) : Y;
}
function _u(e6, t, n, r, o) {
  let i = e6.providerIndexes, s = t.data, a = i & 1048575, c = e6.directiveStart, l = e6.directiveEnd, u = i >> 20, d = r ? a : a + u, p = o ? a + u : l;
  for (let f = d; f < p; f++) {
    let T = s[f];
    if (f < c && n === T || f >= c && T.type === n)
      return f;
  }
  if (o) {
    let f = s[c];
    if (f && qe(f) && f.type === n)
      return c;
  }
  return null;
}
function ko(e6, t, n, r, o) {
  let i = e6[n], s = t.data;
  if (i instanceof bt) {
    let a = i;
    if (a.resolving)
      throw Qr("");
    let c = ia(a.canSeeViewProviders);
    a.resolving = true;
    let l = s[n].type || s[n], u, d = a.injectImpl ? R(a.injectImpl) : null, p = yo(e6, r, 0);
    try {
      i = e6[n] = a.factory(void 0, o, s, e6, r), t.firstCreatePass && n >= r.directiveStart && mu(n, s[n], t);
    } finally {
      d !== null && R(d), ia(c), a.resolving = false, vo();
    }
  }
  return i;
}
function Nu(e6) {
  if (typeof e6 == "string")
    return e6.charCodeAt(0) || 0;
  let t = e6.hasOwnProperty(Me) ? e6[Me] : void 0;
  return typeof t == "number" ? t >= 0 ? t & xa : xu : t;
}
function sa(e6, t, n) {
  let r = 1 << e6;
  return !!(n[t + (e6 >> Aa)] & r);
}
function aa(e6, t) {
  return !(e6 & 2) && !(e6 & 1 && t);
}
var kn = class {
  _tNode;
  _lView;
  constructor(t, n) {
    this._tNode = t, this._lView = n;
  }
  get(t, n, r) {
    return Fa(this._tNode, this._lView, t, De(r), n);
  }
};
function xu() {
  return new kn(Qe(), H());
}
function Au(e6, t, n, r, o) {
  let i = e6, s = t;
  for (; i !== null && s !== null && s[h] & 2048 && !Ze(s); ) {
    let a = ja(i, s, n, r | 2, Y);
    if (a !== Y)
      return a;
    let c = i.parent;
    if (!c) {
      let l = s[ro];
      if (l) {
        let u = l.get(n, Y, r & -5);
        if (u !== Y)
          return u;
      }
      c = Ha(s), s = s[We];
    }
    i = c;
  }
  return o;
}
function Ha(e6) {
  let t = e6[y], n = t.type;
  return n === 2 ? t.declTNode : n === 1 ? e6[re] : null;
}
function Ru() {
  return Va(Qe(), H());
}
function Va(e6, t) {
  return new Ba(Ae(e6, t));
}
var Ba = /* @__PURE__ */ (() => {
  class e6 {
    nativeElement;
    constructor(n) {
      this.nativeElement = n;
    }
    static __NG_ELEMENT_ID__ = Ru;
  }
  return e6;
})();
function ku(e6) {
  return (e6.flags & 128) === 128;
}
var ni = function(e6) {
  return e6[e6.OnPush = 0] = "OnPush", e6[e6.Eager = 1] = "Eager", e6[e6.Default = 1] = "Default", e6;
}(ni || {});
var $a = /* @__PURE__ */ new Map();
var Ou = 0;
function Lu() {
  return Ou++;
}
function Pu(e6) {
  $a.set(e6[le], e6);
}
function Oo(e6) {
  $a.delete(e6[le]);
}
var ca = "__ngContext__";
function _t(e6, t) {
  ue(t) ? (e6[ca] = t[le], Pu(t)) : e6[ca] = t;
}
function Ua(e6) {
  return Wa(e6[ze]);
}
function za(e6) {
  return Wa(e6[ne]);
}
function Wa(e6) {
  for (; e6 !== null && !de(e6); )
    e6 = e6[ne];
  return e6;
}
var Lo;
function ri(e6) {
  Lo = e6;
}
function Ga() {
  if (Lo !== void 0)
    return Lo;
  if (typeof document < "u")
    return document;
  throw new g(210, false);
}
var Hn = new m("", { factory: () => Fu });
var Fu = "ng";
var Vn = new m("");
var At = new m("", { providedIn: "platform", factory: () => "unknown" });
var Bn = new m("", { factory: () => E(x).body?.querySelector("[ngCspNonce]")?.getAttribute("ngCspNonce") || null });
var qa = false;
var Za = new m("", { factory: () => qa });
function oi(e6) {
  return (e6.flags & 32) === 32;
}
var ju = () => null;
function Qa(e6, t, n = false) {
  return ju(e6, t, n);
}
function Ya(e6, t) {
  let n = e6.contentQueries;
  if (n !== null) {
    let r = v(null);
    try {
      for (let o = 0; o < n.length; o += 2) {
        let i = n[o], s = n[o + 1];
        if (s !== -1) {
          let a = e6.data[s];
          mo(i), a.contentQueries(2, t[s], s);
        }
      }
    } finally {
      v(r);
    }
  }
}
function Po(e6, t, n) {
  mo(0);
  let r = v(null);
  try {
    t(e6, n);
  } finally {
    v(r);
  }
}
function Hu(e6, t, n) {
  if (oo(t)) {
    let r = v(null);
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
      v(r);
    }
  }
}
var z = function(e6) {
  return e6[e6.Emulated = 0] = "Emulated", e6[e6.None = 2] = "None", e6[e6.ShadowDom = 3] = "ShadowDom", e6[e6.ExperimentalIsolatedShadowDom = 4] = "ExperimentalIsolatedShadowDom", e6;
}(z || {});
var Sn;
function Vu() {
  if (Sn === void 0 && (Sn = null, ce.trustedTypes))
    try {
      Sn = ce.trustedTypes.createPolicy("angular", { createHTML: (e6) => e6, createScript: (e6) => e6, createScriptURL: (e6) => e6 });
    } catch {
    }
  return Sn;
}
function $n(e6) {
  return Vu()?.createHTML(e6) || e6;
}
var bn;
function Bu() {
  if (bn === void 0 && (bn = null, ce.trustedTypes))
    try {
      bn = ce.trustedTypes.createPolicy("angular#unsafe-bypass", { createHTML: (e6) => e6, createScript: (e6) => e6, createScriptURL: (e6) => e6 });
    } catch {
    }
  return bn;
}
function la(e6) {
  return Bu()?.createHTML(e6) || e6;
}
var ie = class {
  changingThisBreaksApplicationSecurity;
  constructor(t) {
    this.changingThisBreaksApplicationSecurity = t;
  }
  toString() {
    return `SafeValue must use [property]=binding: ${this.changingThisBreaksApplicationSecurity} (see ${sn})`;
  }
};
var Fo = class extends ie {
  getTypeName() {
    return "HTML";
  }
};
var jo = class extends ie {
  getTypeName() {
    return "Style";
  }
};
var Ho = class extends ie {
  getTypeName() {
    return "Script";
  }
};
var Vo = class extends ie {
  getTypeName() {
    return "URL";
  }
};
var Bo = class extends ie {
  getTypeName() {
    return "ResourceURL";
  }
};
function ge(e6) {
  return e6 instanceof ie ? e6.changingThisBreaksApplicationSecurity : e6;
}
function me(e6, t) {
  let n = Ka(e6);
  if (n != null && n !== t) {
    if (n === "ResourceURL" && t === "URL")
      return true;
    throw new Error(`Required a safe ${t}, got a ${n} (see ${sn})`);
  }
  return n === t;
}
function Ka(e6) {
  return e6 instanceof ie && e6.getTypeName() || null;
}
function ii(e6) {
  return new Fo(e6);
}
function si(e6) {
  return new jo(e6);
}
function ai(e6) {
  return new Ho(e6);
}
function ci(e6) {
  return new Vo(e6);
}
function li(e6) {
  return new Bo(e6);
}
function $u(e6) {
  let t = new Uo(e6);
  return Uu() ? new $o(t) : t;
}
var $o = class {
  inertDocumentHelper;
  constructor(t) {
    this.inertDocumentHelper = t;
  }
  getInertBodyElement(t) {
    t = "<body><remove></remove>" + t;
    try {
      let n = new window.DOMParser().parseFromString($n(t), "text/html").body;
      return n === null ? this.inertDocumentHelper.getInertBodyElement(t) : (n.firstChild?.remove(), n);
    } catch {
      return null;
    }
  }
};
var Uo = class {
  defaultDoc;
  inertDocument;
  constructor(t) {
    this.defaultDoc = t, this.inertDocument = this.defaultDoc.implementation.createHTMLDocument("sanitization-inert");
  }
  getInertBodyElement(t) {
    let n = this.inertDocument.createElement("template");
    return n.innerHTML = $n(t), n;
  }
};
function Uu() {
  try {
    return !!new window.DOMParser().parseFromString($n(""), "text/html");
  } catch {
    return false;
  }
}
var zu = /^(?!javascript:)(?:[a-z0-9+.-]+:|[^&:\/?#]*(?:[\/?#]|$))/i;
function Un(e6) {
  return e6 = String(e6), e6.match(zu) ? e6 : "unsafe:" + e6;
}
function se(e6) {
  let t = {};
  for (let n of e6.split(","))
    t[n] = true;
  return t;
}
function Rt(...e6) {
  let t = {};
  for (let n of e6)
    for (let r in n)
      n.hasOwnProperty(r) && (t[r] = true);
  return t;
}
var Ja = se("area,br,col,hr,img,wbr");
var Xa = se("colgroup,dd,dt,li,p,tbody,td,tfoot,th,thead,tr");
var ec = se("rp,rt");
var Wu = Rt(ec, Xa);
var Gu = Rt(Xa, se("address,article,aside,blockquote,caption,center,del,details,dialog,dir,div,dl,figure,figcaption,footer,h1,h2,h3,h4,h5,h6,header,hgroup,hr,ins,main,map,menu,nav,ol,pre,section,summary,table,ul"));
var qu = Rt(ec, se("a,abbr,acronym,audio,b,bdi,bdo,big,br,cite,code,del,dfn,em,font,i,img,ins,kbd,label,map,mark,picture,q,ruby,rp,rt,s,samp,small,source,span,strike,strong,sub,sup,time,track,tt,u,var,video"));
var ua = Rt(Ja, Gu, qu, Wu);
var tc = se("background,cite,href,itemtype,longdesc,poster,src,xlink:href");
var Zu = se("abbr,accesskey,align,alt,autoplay,axis,bgcolor,border,cellpadding,cellspacing,class,clear,color,cols,colspan,compact,controls,coords,datetime,default,dir,download,face,headers,height,hidden,hreflang,hspace,ismap,itemscope,itemprop,kind,label,lang,language,loop,media,muted,nohref,nowrap,open,preload,rel,rev,role,rows,rowspan,rules,scope,scrolling,shape,size,sizes,span,srclang,srcset,start,summary,tabindex,target,title,translate,type,usemap,valign,value,vspace,width");
var Qu = se("aria-activedescendant,aria-atomic,aria-autocomplete,aria-busy,aria-checked,aria-colcount,aria-colindex,aria-colspan,aria-controls,aria-current,aria-describedby,aria-details,aria-disabled,aria-dropeffect,aria-errormessage,aria-expanded,aria-flowto,aria-grabbed,aria-haspopup,aria-hidden,aria-invalid,aria-keyshortcuts,aria-label,aria-labelledby,aria-level,aria-live,aria-modal,aria-multiline,aria-multiselectable,aria-orientation,aria-owns,aria-placeholder,aria-posinset,aria-pressed,aria-readonly,aria-relevant,aria-required,aria-roledescription,aria-rowcount,aria-rowindex,aria-rowspan,aria-selected,aria-setsize,aria-sort,aria-valuemax,aria-valuemin,aria-valuenow,aria-valuetext");
var Yu = Rt(tc, Zu, Qu);
var Ku = se("script,style,template");
var zo = class {
  sanitizedSomething = false;
  buf = [];
  sanitizeChildren(t) {
    let n = t.firstChild, r = true, o = [];
    for (; n; ) {
      if (n.nodeType === Node.ELEMENT_NODE ? r = this.startElement(n) : n.nodeType === Node.TEXT_NODE ? this.chars(n.nodeValue) : this.sanitizedSomething = true, r && n.firstChild) {
        o.push(n), n = ed(n);
        continue;
      }
      for (; n; ) {
        n.nodeType === Node.ELEMENT_NODE && this.endElement(n);
        let i = Xu(n);
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
    let n = da(t).toLowerCase();
    if (!ua.hasOwnProperty(n))
      return this.sanitizedSomething = true, !Ku.hasOwnProperty(n);
    this.buf.push("<"), this.buf.push(n);
    let r = t.attributes;
    for (let o = 0; o < r.length; o++) {
      let i = r.item(o), s = i.name, a = s.toLowerCase();
      if (!Yu.hasOwnProperty(a)) {
        this.sanitizedSomething = true;
        continue;
      }
      let c = i.value;
      tc[a] && (c = Un(c)), this.buf.push(" ", s, '="', fa(c), '"');
    }
    return this.buf.push(">"), true;
  }
  endElement(t) {
    let n = da(t).toLowerCase();
    ua.hasOwnProperty(n) && !Ja.hasOwnProperty(n) && (this.buf.push("</"), this.buf.push(n), this.buf.push(">"));
  }
  chars(t) {
    this.buf.push(fa(t));
  }
};
function Ju(e6, t) {
  return (e6.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_CONTAINED_BY) !== Node.DOCUMENT_POSITION_CONTAINED_BY;
}
function Xu(e6) {
  let t = e6.nextSibling;
  if (t && e6 !== t.previousSibling)
    throw nc(t);
  return t;
}
function ed(e6) {
  let t = e6.firstChild;
  if (t && Ju(e6, t))
    throw nc(t);
  return t;
}
function da(e6) {
  let t = e6.nodeName;
  return typeof t == "string" ? t : "FORM";
}
function nc(e6) {
  return new Error(`Failed to sanitize html because the element is clobbered: ${e6.outerHTML}`);
}
var td = /[\uD800-\uDBFF][\uDC00-\uDFFF]/g;
var nd = /([^\#-~ |!])/g;
function fa(e6) {
  return e6.replace(/&/g, "&amp;").replace(td, function(t) {
    let n = t.charCodeAt(0), r = t.charCodeAt(1);
    return "&#" + ((n - 55296) * 1024 + (r - 56320) + 65536) + ";";
  }).replace(nd, function(t) {
    return "&#" + t.charCodeAt(0) + ";";
  }).replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
var _n;
function zn(e6, t) {
  let n = null;
  try {
    _n = _n || $u(e6);
    let r = t ? String(t) : "";
    n = _n.getInertBodyElement(r);
    let o = 5, i = r;
    do {
      if (o === 0)
        throw new Error("Failed to sanitize html because the input is unstable");
      o--, r = i, i = n.innerHTML, n = _n.getInertBodyElement(r);
    } while (r !== i);
    let a = new zo().sanitizeChildren(pa(n) || n);
    return $n(a);
  } finally {
    if (n) {
      let r = pa(n) || n;
      for (; r.firstChild; )
        r.firstChild.remove();
    }
  }
}
function pa(e6) {
  return "content" in e6 && rd(e6) ? e6.content : null;
}
function rd(e6) {
  return e6.nodeType === Node.ELEMENT_NODE && e6.nodeName === "TEMPLATE";
}
function od(e6, t) {
  return e6.createText(t);
}
function id(e6, t, n) {
  e6.setValue(t, n);
}
function rc(e6, t, n) {
  return e6.createElement(t, n);
}
function Wo(e6, t, n, r, o) {
  e6.insertBefore(t, n, r, o);
}
function oc(e6, t, n) {
  e6.appendChild(t, n);
}
function ha(e6, t, n, r, o) {
  r !== null ? Wo(e6, t, n, r, o) : oc(e6, t, n);
}
function sd(e6, t, n, r) {
  e6.removeChild(null, t, n, r);
}
function ad(e6, t, n) {
  e6.setAttribute(t, "style", n);
}
function cd(e6, t, n) {
  n === "" ? e6.removeAttribute(t, "class") : e6.setAttribute(t, "class", n);
}
function ic(e6, t, n) {
  let { mergedAttrs: r, classes: o, styles: i } = n;
  r !== null && Eu(e6, t, r), o !== null && cd(e6, t, o), i !== null && ad(e6, t, i);
}
var K = function(e6) {
  return e6[e6.NONE = 0] = "NONE", e6[e6.HTML = 1] = "HTML", e6[e6.STYLE = 2] = "STYLE", e6[e6.SCRIPT = 3] = "SCRIPT", e6[e6.URL = 4] = "URL", e6[e6.RESOURCE_URL = 5] = "RESOURCE_URL", e6;
}(K || {});
function ui(e6) {
  let t = ld();
  return t ? la(t.sanitize(K.HTML, e6) || "") : me(e6, "HTML") ? la(ge(e6)) : zn(Ga(), Zr(e6));
}
function ld() {
  let e6 = H();
  return e6 && e6[Z].sanitizer;
}
var ud = "ng-template";
function dd(e6) {
  return e6.type === 4 && e6.value !== ud;
}
function Go(e6) {
  return (e6 & 1) === 0;
}
function ga(e6, t) {
  return e6 ? ":not(" + t.trim() + ")" : t;
}
function fd(e6) {
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
      o !== "" && !Go(s) && (t += ga(i, o), o = ""), r = s, i = i || !Go(r);
    n++;
  }
  return o !== "" && (t += ga(i, o)), t;
}
function pd(e6) {
  return e6.map(fd).join(",");
}
function hd(e6) {
  let t = [], n = [], r = 1, o = 2;
  for (; r < e6.length; ) {
    let i = e6[r];
    if (typeof i == "string")
      o === 2 ? i !== "" && t.push(i, e6[++r]) : o === 8 && n.push(i);
    else {
      if (!Go(o))
        break;
      o = i;
    }
    r++;
  }
  return n.length && t.push(1, ...n), t;
}
var tt = {};
function sc(e6, t, n, r, o, i, s, a, c, l, u) {
  let d = U + r, p = d + o, f = gd(d, p), T = typeof l == "function" ? l() : l;
  return f[y] = { type: e6, blueprint: f, template: n, queries: null, viewQuery: a, declTNode: t, data: f.slice().fill(null, d), bindingStartIndex: d, expandoStartIndex: p, hostBindingOpCodes: null, firstCreatePass: true, firstUpdatePass: true, staticViewQueries: false, staticContentQueries: false, preOrderHooks: null, preOrderCheckHooks: null, contentHooks: null, contentCheckHooks: null, viewHooks: null, viewCheckHooks: null, destroyHooks: null, cleanup: null, contentQueries: null, components: null, directiveRegistry: typeof i == "function" ? i() : i, pipeRegistry: typeof s == "function" ? s() : s, firstChild: null, schemas: c, consts: T, incompleteFirstPass: false, ssrId: u };
}
function gd(e6, t) {
  let n = [];
  for (let r = 0; r < t; r++)
    n.push(r < e6 ? null : tt);
  return n;
}
function md(e6) {
  let t = e6.tView;
  return t === null || t.incompleteFirstPass ? e6.tView = sc(1, null, e6.template, e6.decls, e6.vars, e6.directiveDefs, e6.pipeDefs, e6.viewQuery, e6.schemas, e6.consts, e6.id) : t;
}
function ac(e6, t, n, r, o, i, s, a, c, l, u) {
  let d = t.blueprint.slice();
  return d[q] = o, d[h] = r | 4 | 128 | 8 | 64 | 1024, (l !== null || e6 && e6[h] & 2048) && (d[h] |= 2048), so(d), d[O] = d[We] = e6, d[L] = n, d[Z] = s || e6 && e6[Z], d[P] = a || e6 && e6[P], d[_e] = c || e6 && e6[_e] || null, d[re] = i, d[le] = Lu(), d[hn] = u, d[ro] = l, d[Q] = t.type == 2 ? e6[Q] : d, d;
}
function yd(e6, t, n) {
  let r = Ae(t, e6), o = md(n), i = e6[Z].rendererFactory, s = vd(e6, ac(e6, o, null, cc(n), r, t, null, i.createRenderer(r, n), null, null, null));
  return e6[t.index] = s;
}
function cc(e6) {
  let t = 16;
  return e6.signals ? t = 4096 : e6.onPush && (t = 64), t;
}
function lc(e6, t, n, r) {
  if (n === 0)
    return -1;
  let o = t.length;
  for (let i = 0; i < n; i++)
    t.push(r), e6.blueprint.push(r), e6.data.push(null);
  return o;
}
function vd(e6, t) {
  return e6[ze] ? e6[no][ne] = t : e6[ze] = t, e6[no] = t, t;
}
function Wn(e6 = 1) {
  uc(Dn(), H(), Mn() + e6, false);
}
function uc(e6, t, n, r) {
  if (!r)
    if ((t[h] & 3) === 3) {
      let i = e6.preOrderCheckHooks;
      i !== null && Nn(t, i, n);
    } else {
      let i = e6.preOrderHooks;
      i !== null && xn(t, i, 0, n);
    }
  he(n);
}
var Gn = function(e6) {
  return e6[e6.None = 0] = "None", e6[e6.SignalBased = 1] = "SignalBased", e6[e6.HasDecoratorInputTransform = 2] = "HasDecoratorInputTransform", e6;
}(Gn || {});
function qo(e6, t, n, r) {
  let o = v(null);
  try {
    let [i, s, a] = e6.inputs[n], c = null;
    (s & Gn.SignalBased) !== 0 && (c = t[i][W]), c !== null && c.transformFn !== void 0 ? r = c.transformFn(r) : a !== null && (r = a.call(t, r)), e6.setInput !== null ? e6.setInput(t, c, r, n, i) : Sa(t, c, i, r);
  } finally {
    v(o);
  }
}
var ke = function(e6) {
  return e6[e6.Important = 1] = "Important", e6[e6.DashCase = 2] = "DashCase", e6;
}(ke || {});
var Ed;
function dc(e6, t) {
  return Ed(e6, t);
}
var ny = typeof document < "u" && typeof document?.documentElement?.getAnimations == "function";
var Zo = /* @__PURE__ */ new WeakMap();
var Mt = /* @__PURE__ */ new WeakSet();
function Id(e6, t) {
  let n = Zo.get(e6);
  if (!n || n.length === 0)
    return;
  let r = t.parentNode, o = t.previousSibling;
  for (let i = n.length - 1; i >= 0; i--) {
    let s = n[i], a = s.parentNode;
    s === t ? (n.splice(i, 1), Mt.add(s), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } }))) : (o && s === o || a && r && a !== r) && (n.splice(i, 1), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } })), s.parentNode?.removeChild(s));
  }
}
function Dd(e6, t) {
  let n = Zo.get(e6);
  n ? n.includes(t) || n.push(t) : Zo.set(e6, [t]);
}
var et = /* @__PURE__ */ new Set();
var di = function(e6) {
  return e6[e6.CHANGE_DETECTION = 0] = "CHANGE_DETECTION", e6[e6.AFTER_NEXT_RENDER = 1] = "AFTER_NEXT_RENDER", e6;
}(di || {});
var nt = new m("");
var ma = /* @__PURE__ */ new Set();
function fc(e6) {
  ma.has(e6) || (ma.add(e6), performance?.mark?.("mark_feature_usage", { detail: { feature: e6 } }));
}
var pc = (() => {
  class e6 {
    impl = null;
    execute() {
      this.impl?.execute();
    }
    static \u0275prov = S({ token: e6, providedIn: "root", factory: () => new e6() });
  }
  return e6;
})();
var wd = new m("", { factory: () => ({ queue: /* @__PURE__ */ new Set(), isScheduled: false, scheduler: null, injector: E($) }) });
function hc(e6, t, n) {
  let r = e6.get(wd);
  if (Array.isArray(t))
    for (let o of t)
      r.queue.add(o), n?.detachedLeaveAnimationFns?.push(o);
  else
    r.queue.add(t), n?.detachedLeaveAnimationFns?.push(t);
  r.scheduler && r.scheduler(e6);
}
function Cd(e6, t) {
  for (let [n, r] of t)
    hc(e6, r.animateFns);
}
function ya(e6, t, n, r) {
  let o = e6?.[Ge]?.enter;
  t !== null && o && o.has(n.index) && Cd(r, o);
}
function Je(e6, t, n, r, o, i, s, a) {
  if (o != null) {
    let c, l = false;
    de(o) ? c = o : ue(o) && (l = true, o = o[q]);
    let u = fe(o);
    e6 === 0 && r !== null ? (ya(a, r, i, n), s == null ? oc(t, r, u) : Wo(t, r, u, s || null, true)) : e6 === 1 && r !== null ? (ya(a, r, i, n), Wo(t, r, u, s || null, true), Id(i, u)) : e6 === 2 ? (a?.[Ge]?.leave?.has(i.index) && Dd(i, u), Mt.delete(u), va(a, i, n, (d) => {
      if (Mt.has(u)) {
        Mt.delete(u);
        return;
      }
      sd(t, u, l, d);
    })) : e6 === 3 && (Mt.delete(u), va(a, i, n, () => {
      t.destroyNode(u);
    })), c != null && Fd(t, e6, n, c, i, r, s);
  }
}
function Td(e6, t) {
  gc(e6, t), t[q] = null, t[re] = null;
}
function gc(e6, t) {
  t[Z].changeDetectionScheduler?.notify(9), hi(e6, t, t[P], 2, null, null);
}
function Md(e6) {
  let t = e6[ze];
  if (!t)
    return No(e6[y], e6);
  for (; t; ) {
    let n = null;
    if (ue(t))
      n = t[ze];
    else {
      let r = t[oe];
      r && (n = r);
    }
    if (!n) {
      for (; t && !t[ne] && t !== e6; )
        ue(t) && No(t[y], t), t = t[O];
      t === null && (t = e6), ue(t) && No(t[y], t), n = t && t[ne];
    }
    t = n;
  }
}
function fi(e6, t) {
  let n = e6[mt], r = n.indexOf(t);
  n.splice(r, 1);
}
function Sd(e6, t) {
  if (xe(t))
    return;
  let n = t[P];
  n.destroyNode && hi(e6, t, n, 3, null, null), Md(t);
}
function No(e6, t) {
  if (xe(t))
    return;
  let n = v(null);
  try {
    t[h] &= -129, t[h] |= 256, t[F] && qt(t[F]), Nd(e6, t), _d(e6, t), t[y].type === 1 && t[P].destroy();
    let r = t[ht];
    if (r !== null && de(t[O])) {
      r !== t[O] && fi(r, t);
      let o = t[mn];
      o !== null && o.detachView(e6);
    }
    Oo(t);
  } finally {
    v(n);
  }
}
function va(e6, t, n, r) {
  let o = e6?.[Ge];
  if (o == null || o.leave == null || !o.leave.has(t.index))
    return r(false);
  e6 && et.add(e6[le]), hc(n, () => {
    if (o.leave && o.leave.has(t.index)) {
      let s = o.leave.get(t.index), a = [];
      if (s) {
        for (let c = 0; c < s.animateFns.length; c++) {
          let l = s.animateFns[c], { promise: u } = l();
          a.push(u);
        }
        o.detachedLeaveAnimationFns = void 0;
      }
      o.running = Promise.allSettled(a), bd(e6, r);
    } else
      e6 && et.delete(e6[le]), r(false);
  }, o);
}
function bd(e6, t) {
  let n = e6[Ge]?.running;
  if (n) {
    n.then(() => {
      e6[Ge].running = void 0, et.delete(e6[le]), t(true);
    });
    return;
  }
  t(false);
}
function _d(e6, t) {
  let n = e6.cleanup, r = t[gn];
  if (n !== null)
    for (let s = 0; s < n.length - 1; s += 2)
      if (typeof n[s] == "string") {
        let a = n[s + 3];
        a >= 0 ? r[a]() : r[-a].unsubscribe(), s += 2;
      } else {
        let a = r[n[s + 1]];
        n[s].call(a);
      }
  r !== null && (t[gn] = null);
  let o = t[X];
  if (o !== null) {
    t[X] = null;
    for (let s = 0; s < o.length; s++) {
      let a = o[s];
      a();
    }
  }
  let i = t[gt];
  if (i !== null) {
    t[gt] = null;
    for (let s of i)
      s.destroy();
  }
}
function Nd(e6, t) {
  let n;
  if (e6 != null && (n = e6.destroyHooks) != null)
    for (let r = 0; r < n.length; r += 2) {
      let o = t[n[r]];
      if (!(o instanceof bt)) {
        let i = n[r + 1];
        if (Array.isArray(i))
          for (let s = 0; s < i.length; s += 2) {
            let a = o[i[s]], c = i[s + 1];
            M(w.LifecycleHookStart, a, c);
            try {
              c.call(a);
            } finally {
              M(w.LifecycleHookEnd, a, c);
            }
          }
        else {
          M(w.LifecycleHookStart, o, i);
          try {
            i.call(o);
          } finally {
            M(w.LifecycleHookEnd, o, i);
          }
        }
      }
    }
}
function xd(e6, t, n) {
  return Ad(e6, t.parent, n);
}
function Ad(e6, t, n) {
  let r = t;
  for (; r !== null && r.type & 168; )
    t = r, r = t.parent;
  if (r === null)
    return n[q];
  if (yt(r)) {
    let { encapsulation: o } = e6.data[r.directiveStart + r.componentOffset];
    if (o === z.None || o === z.Emulated)
      return null;
  }
  return Ae(r, n);
}
function Rd(e6, t, n) {
  return Od(e6, t, n);
}
function kd(e6, t, n) {
  return e6.type & 40 ? Ae(e6, n) : null;
}
var Od = kd;
var Ea;
function mc(e6, t, n, r) {
  let o = xd(e6, r, t), i = t[P], s = r.parent || t[re], a = Rd(s, r, t);
  if (o != null)
    if (Array.isArray(n))
      for (let c = 0; c < n.length; c++)
        ha(i, o, n[c], a, false);
    else
      ha(i, o, n, a, false);
  Ea !== void 0 && Ea(i, r, t, n, o);
}
function Ld(e6, t) {
  if (t !== null) {
    let r = e6[Q][re], o = t.projection;
    return r.projection[o];
  }
  return null;
}
function pi(e6, t, n, r, o, i, s) {
  for (; n != null; ) {
    let a = r[_e];
    if (n.type === 128) {
      n = n.next;
      continue;
    }
    let c = r[n.index], l = n.type;
    if (s && t === 0 && (c && _t(fe(c), r), n.flags |= 2), !oi(n))
      if (l & 8)
        pi(e6, t, n.child, r, o, i, false), Je(t, e6, a, o, c, n, i, r);
      else if (l & 32) {
        let u = dc(n, r), d;
        for (; d = u(); )
          Je(t, e6, a, o, d, n, i, r);
        Je(t, e6, a, o, c, n, i, r);
      } else
        l & 16 ? Pd(e6, t, r, n, o, i) : Je(t, e6, a, o, c, n, i, r);
    n = s ? n.projectionNext : n.next;
  }
}
function hi(e6, t, n, r, o, i) {
  pi(n, r, e6.firstChild, t, o, i, false);
}
function Pd(e6, t, n, r, o, i) {
  let s = n[Q], c = s[re].projection[r.projection];
  if (Array.isArray(c))
    for (let l = 0; l < c.length; l++) {
      let u = c[l];
      Je(t, e6, n[_e], o, u, r, i, n);
    }
  else {
    let l = c, u = s[O];
    ku(r) && (l.flags |= 128), pi(e6, t, l, u, o, i, true);
  }
}
function Fd(e6, t, n, r, o, i, s) {
  let a = r[En], c = fe(r);
  a !== c && Je(t, e6, n, i, a, o, s);
  for (let l = oe; l < r.length; l++) {
    let u = r[l];
    hi(u[y], u, e6, t, i, a);
  }
}
function yc(e6, t, n, r, o) {
  let i = Mn(), s = r & 2;
  try {
    he(-1), s && t.length > U && uc(e6, t, U, false);
    let a = s ? w.TemplateUpdateStart : w.TemplateCreateStart;
    M(a, o, n), n(r, o);
  } finally {
    he(i);
    let a = s ? w.TemplateUpdateEnd : w.TemplateCreateEnd;
    M(a, o, n);
  }
}
function jd(e6, t, n) {
  zd(e6, t, n), (n.flags & 64) === 64 && Wd(e6, t, n);
}
function Hd(e6, t, n = Ae) {
  let r = t.localNames;
  if (r !== null) {
    let o = t.index + 1;
    for (let i = 0; i < r.length; i += 2) {
      let s = r[i + 1], a = s === -1 ? n(t, e6) : e6[s];
      e6[o++] = a;
    }
  }
}
function Vd(e6, t, n, r) {
  let i = r.get(Za, qa) || n === z.ShadowDom || n === z.ExperimentalIsolatedShadowDom, s = e6.selectRootElement(t, i);
  return Bd(s), s;
}
function Bd(e6) {
  $d(e6);
}
var $d = () => null;
function Ud(e6, t, n, r, o, i) {
  if (e6.type & 3) {
    let s = Ae(e6, t);
    r = i != null ? i(r, e6.value || "", n) : r, o.setProperty(s, n, r);
  } else
    e6.type & 12;
}
function zd(e6, t, n) {
  let r = n.directiveStart, o = n.directiveEnd;
  yt(n) && yd(t, n, e6.data[r + n.componentOffset]), e6.firstCreatePass || Ra(n, t);
  let i = n.initialInputs;
  for (let s = r; s < o; s++) {
    let a = e6.data[s], c = ko(t, e6, s, n);
    if (_t(c, t), i !== null && qd(t, s - r, c, a, n, i), qe(a)) {
      let l = pe(n.index, t);
      l[L] = ko(t, e6, s, n);
    }
  }
}
function Wd(e6, t, n) {
  let r = n.directiveStart, o = n.directiveEnd, i = n.index, s = $s();
  try {
    he(i);
    for (let a = r; a < o; a++) {
      let c = e6.data[a], l = t[a];
      wn(a), (c.hostBindings !== null || c.hostVars !== 0 || c.hostAttrs !== null) && Gd(c, l);
    }
  } finally {
    he(-1), wn(s);
  }
}
function Gd(e6, t) {
  e6.hostBindings !== null && e6.hostBindings(1, t);
}
function qd(e6, t, n, r, o, i) {
  let s = i[t];
  if (s !== null)
    for (let a = 0; a < s.length; a += 2) {
      let c = s[a], l = s[a + 1];
      qo(r, n, c, l);
    }
}
function Zd(e6, t, n, r, o) {
  let i = U + n, s = t[y], a = o(s, t, e6, r, n);
  t[i] = a, Dt(e6, true);
  let c = e6.type === 2;
  return c ? (ic(t[P], a, e6), (As() === 0 || Ss(e6)) && _t(a, t), Rs()) : _t(a, t), Eo() && (!c || !oi(e6)) && mc(s, t, a, e6), e6;
}
function Qd(e6) {
  let t = e6;
  return fo() ? js() : (t = t.parent, Dt(t, false)), t;
}
function Yd(e6, t, n, r, o) {
  let i = e6.inputs?.[r], s = e6.hostDirectiveInputs?.[r], a = false;
  if (s)
    for (let c = 0; c < s.length; c += 2) {
      let l = s[c], u = s[c + 1], d = t.data[l];
      qo(d, n[l], u, o), a = true;
    }
  if (i)
    for (let c of i) {
      let l = n[c], u = t.data[c];
      qo(u, l, r, o), a = true;
    }
  return a;
}
function Kd(e6, t) {
  let n = pe(t, e6), r = n[y];
  Jd(r, n);
  let o = n[q];
  o !== null && n[hn] === null && (n[hn] = Qa(o, n[_e])), M(w.ComponentStart);
  try {
    vc(r, n, n[L]);
  } finally {
    M(w.ComponentEnd, n[L]);
  }
}
function Jd(e6, t) {
  for (let n = t.length; n < e6.blueprint.length; n++)
    t.push(e6.blueprint[n]);
}
function vc(e6, t, n) {
  Cn(t);
  try {
    let r = e6.viewQuery;
    r !== null && Po(1, r, n);
    let o = e6.template;
    o !== null && yc(e6, t, o, 1, n), e6.firstCreatePass && (e6.firstCreatePass = false), t[mn]?.finishViewCreation(e6), e6.staticContentQueries && Ya(e6, t), e6.staticViewQueries && Po(2, e6.viewQuery, n);
    let i = e6.components;
    i !== null && Xd(t, i);
  } catch (r) {
    throw e6.firstCreatePass && (e6.incompleteFirstPass = true, e6.firstCreatePass = false), r;
  } finally {
    t[h] &= -5, Tn();
  }
}
function Xd(e6, t) {
  for (let n = 0; n < t.length; n++)
    Kd(e6, t[n]);
}
function Nt(e6, t, n, r, o = false) {
  for (; n !== null; ) {
    if (n.type === 128) {
      n = o ? n.projectionNext : n.next;
      continue;
    }
    let i = t[n.index];
    i !== null && r.push(fe(i)), de(i) && Ec(i, r);
    let s = n.type;
    if (s & 8)
      Nt(e6, t, n.child, r);
    else if (s & 32) {
      let a = dc(n, t), c;
      for (; c = a(); )
        r.push(c);
    } else if (s & 16) {
      let a = Ld(t, n);
      if (Array.isArray(a))
        r.push(...a);
      else {
        let c = Te(t[Q]);
        Nt(c[y], c, a, r, true);
      }
    }
    n = o ? n.projectionNext : n.next;
  }
  return r;
}
function Ec(e6, t) {
  for (let n = oe; n < e6.length; n++) {
    let r = e6[n], o = r[y].firstChild;
    o !== null && Nt(r[y], r, o, t);
  }
  e6[En] !== e6[q] && t.push(e6[En]);
}
function Ic(e6) {
  if (e6[vn] !== null) {
    for (let t of e6[vn])
      t.impl.addSequence(t);
    e6[vn].length = 0;
  }
}
var Dc = [];
function ef(e6) {
  return e6[F] ?? tf(e6);
}
function tf(e6) {
  let t = Dc.pop() ?? Object.create(rf);
  return t.lView = e6, t;
}
function nf(e6) {
  e6.lView[F] !== e6 && (e6.lView = null, Dc.push(e6));
}
var rf = V(A({}, Gt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e6) => {
  It(e6.lView);
}, consumerOnSignalRead() {
  this.lView[F] = this;
} });
function of(e6) {
  let t = e6[F] ?? Object.create(sf);
  return t.lView = e6, t;
}
var sf = V(A({}, Gt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e6) => {
  let t = Te(e6.lView);
  for (; t && !wc(t[y]); )
    t = Te(t);
  t && ao(t);
}, consumerOnSignalRead() {
  this.lView[F] = this;
} });
function wc(e6) {
  return e6.type !== 2;
}
function Cc(e6) {
  if (e6[gt] === null)
    return;
  let t = true;
  for (; t; ) {
    let n = false;
    for (let r of e6[gt])
      r.dirty && (n = true, r.zone === null || Zone.current === r.zone ? r.run() : r.zone.run(() => r.run()));
    t = n && !!(e6[h] & 8192);
  }
}
var af = 100;
function Tc(e6, t = 0) {
  let r = e6[Z].rendererFactory, o = false;
  o || r.begin?.();
  try {
    cf(e6, t);
  } finally {
    o || r.end?.();
  }
}
function cf(e6, t) {
  let n = po();
  try {
    ho(true), Qo(e6, t);
    let r = 0;
    for (; Et(e6); ) {
      if (r === af)
        throw new g(103, false);
      r++, Qo(e6, 1);
    }
  } finally {
    ho(n);
  }
}
function lf(e6, t, n, r) {
  if (xe(t))
    return;
  let o = t[h], i = false, s = false;
  Cn(t);
  let a = true, c = null, l = null;
  i || (wc(e6) ? (l = ef(t), c = dr(l)) : Wt() === null ? (a = false, l = of(t), c = dr(l)) : t[F] && (qt(t[F]), t[F] = null));
  try {
    so(t), Hs(e6.bindingStartIndex), n !== null && yc(e6, t, n, 2, r);
    let u = (o & 3) === 3;
    if (!i)
      if (u) {
        let f = e6.preOrderCheckHooks;
        f !== null && Nn(t, f, null);
      } else {
        let f = e6.preOrderHooks;
        f !== null && xn(t, f, 0, null), bo(t, 0);
      }
    if (s || uf(t), Cc(t), Mc(t, 0), e6.contentQueries !== null && Ya(e6, t), !i)
      if (u) {
        let f = e6.contentCheckHooks;
        f !== null && Nn(t, f);
      } else {
        let f = e6.contentHooks;
        f !== null && xn(t, f, 1), bo(t, 1);
      }
    ff(e6, t);
    let d = e6.components;
    d !== null && bc(t, d, 0);
    let p = e6.viewQuery;
    if (p !== null && Po(2, p, r), !i)
      if (u) {
        let f = e6.viewCheckHooks;
        f !== null && Nn(t, f);
      } else {
        let f = e6.viewHooks;
        f !== null && xn(t, f, 2), bo(t, 2);
      }
    if (e6.firstUpdatePass === true && (e6.firstUpdatePass = false), t[yn]) {
      for (let f of t[yn])
        f();
      t[yn] = null;
    }
    i || (Ic(t), t[h] &= -73);
  } catch (u) {
    throw i || It(t), u;
  } finally {
    l !== null && (Hi(l, c), a && nf(l)), Tn();
  }
}
function Mc(e6, t) {
  for (let n = Ua(e6); n !== null; n = za(n))
    for (let r = oe; r < n.length; r++) {
      let o = n[r];
      Sc(o, t);
    }
}
function uf(e6) {
  for (let t = Ua(e6); t !== null; t = za(t)) {
    if (!(t[h] & 2))
      continue;
    let n = t[mt];
    for (let r = 0; r < n.length; r++) {
      let o = n[r];
      ao(o);
    }
  }
}
function df(e6, t, n) {
  M(w.ComponentStart);
  let r = pe(t, e6);
  try {
    Sc(r, n);
  } finally {
    M(w.ComponentEnd, r[L]);
  }
}
function Sc(e6, t) {
  In(e6) && Qo(e6, t);
}
function Qo(e6, t) {
  let r = e6[y], o = e6[h], i = e6[F], s = !!(t === 0 && o & 16);
  if (s ||= !!(o & 64 && t === 0), s ||= !!(o & 1024), s ||= !!(i?.dirty && fr(i)), s ||= false, i && (i.dirty = false), e6[h] &= -9217, s)
    lf(r, e6, r.template, e6[L]);
  else if (o & 8192) {
    let a = v(null);
    try {
      Cc(e6), Mc(e6, 1);
      let c = r.components;
      c !== null && bc(e6, c, 1), Ic(e6);
    } finally {
      v(a);
    }
  }
}
function bc(e6, t, n) {
  for (let r = 0; r < t.length; r++)
    df(e6, t[r], n);
}
function ff(e6, t) {
  let n = e6.hostBindingOpCodes;
  if (n !== null)
    try {
      for (let r = 0; r < n.length; r++) {
        let o = n[r];
        if (o < 0)
          he(~o);
        else {
          let i = o, s = n[++r], a = n[++r];
          Bs(s, i);
          let c = t[i];
          M(w.HostBindingsUpdateStart, c);
          try {
            a(2, c);
          } finally {
            M(w.HostBindingsUpdateEnd, c);
          }
        }
      }
    } finally {
      he(-1);
    }
}
function _c(e6, t) {
  let n = po() ? 64 : 1088;
  for (e6[Z].changeDetectionScheduler?.notify(t); e6; ) {
    e6[h] |= n;
    let r = Te(e6);
    if (Ze(e6) && !r)
      return e6;
    e6 = r;
  }
  return null;
}
function pf(e6, t) {
  if (e6.length <= oe)
    return;
  let n = oe + t, r = e6[n];
  if (r) {
    let o = r[ht];
    o !== null && o !== e6 && fi(o, r), t > 0 && (e6[n - 1][ne] = r[ne]);
    let i = Kr(e6, oe + t);
    Td(r[y], r);
    let s = i[mn];
    s !== null && s.detachView(i[y]), r[O] = null, r[ne] = null, r[h] &= -129;
  }
  return r;
}
function hf(e6, t) {
  let n = e6[mt], r = t[O];
  if (ue(r))
    e6[h] |= 2;
  else {
    let o = r[O][Q];
    t[Q] !== o && (e6[h] |= 2);
  }
  n === null ? e6[mt] = [t] : n.push(t);
}
var On = class {
  _lView;
  _cdRefInjectingView;
  _appRef = null;
  _attachedToViewContainer = false;
  exhaustive;
  get rootNodes() {
    let t = this._lView, n = t[y];
    return Nt(n, t, n.firstChild, []);
  }
  constructor(t, n) {
    this._lView = t, this._cdRefInjectingView = n;
  }
  get context() {
    return this._lView[L];
  }
  set context(t) {
    this._lView[L] = t;
  }
  get destroyed() {
    return xe(this._lView);
  }
  destroy() {
    if (this._appRef)
      this._appRef.detachView(this);
    else if (this._attachedToViewContainer) {
      let t = this._lView[O];
      if (de(t)) {
        let n = t[Ms], r = n ? n.indexOf(this) : -1;
        r > -1 && (pf(t, r), Kr(n, r));
      }
      this._attachedToViewContainer = false;
    }
    Sd(this._lView[y], this._lView);
  }
  onDestroy(t) {
    lo(this._lView, t);
  }
  markForCheck() {
    _c(this._cdRefInjectingView || this._lView, 4);
  }
  detach() {
    this._lView[h] &= -129;
  }
  reattach() {
    co(this._lView), this._lView[h] |= 128;
  }
  detectChanges() {
    this._lView[h] |= 1024, Tc(this._lView);
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
    let t = Ze(this._lView), n = this._lView[ht];
    n !== null && !t && fi(n, this._lView), gc(this._lView[y], this._lView);
  }
  attachToAppRef(t) {
    if (this._attachedToViewContainer)
      throw new g(902, false);
    this._appRef = t;
    let n = Ze(this._lView), r = this._lView[ht];
    r !== null && !n && hf(r, this._lView), co(this._lView);
  }
};
function gi(e6, t, n, r, o) {
  let i = e6.data[t];
  if (i === null)
    i = gf(e6, t, n, r, o), Vs() && (i.flags |= 32);
  else if (i.type & 64) {
    i.type = n, i.value = r, i.attrs = o;
    let s = Fs();
    i.injectorIndex = s === null ? -1 : s.injectorIndex;
  }
  return Dt(i, true), i;
}
function gf(e6, t, n, r, o) {
  let i = uo(), s = fo(), a = s ? i : i && i.parent, c = e6.data[t] = yf(e6, a, n, t, r, o);
  return mf(e6, c, i, s), c;
}
function mf(e6, t, n, r) {
  e6.firstChild === null && (e6.firstChild = t), n !== null && (r ? n.child == null && t.parent !== null && (n.child = t) : n.next === null && (n.next = t, t.prev = n));
}
function yf(e6, t, n, r, o, i) {
  let s = t ? t.injectorIndex : -1, a = 0;
  return Os() && (a |= 128), { type: n, index: r, insertBeforeIndex: null, injectorIndex: s, directiveStart: -1, directiveEnd: -1, directiveStylingLast: -1, componentOffset: -1, controlDirectiveIndex: -1, customControlIndex: -1, propertyBindings: null, flags: a, providerIndexes: 0, value: o, attrs: i, mergedAttrs: null, localNames: null, initialInputs: null, inputs: null, hostDirectiveInputs: null, outputs: null, hostDirectiveOutputs: null, directiveToIndex: null, tView: null, next: null, prev: null, projectionNext: null, child: null, parent: t, projection: null, styles: null, stylesWithoutHost: null, residualStyles: void 0, classes: null, classesWithoutHost: null, residualClasses: void 0, classBindings: 0, styleBindings: 0 };
}
var Nc = class {
};
var qn = class {
};
var Yo = class {
  resolveComponentFactory(t) {
    throw new g(917, false);
  }
};
var Zn = class {
  static NULL = new Yo();
};
var Re = class {
};
var xc = (() => {
  class e6 {
    static \u0275prov = S({ token: e6, providedIn: "root", factory: () => null });
  }
  return e6;
})();
var An = {};
var Ko = class {
  injector;
  parentInjector;
  constructor(t, n) {
    this.injector = t, this.parentInjector = n;
  }
  get(t, n, r) {
    let o = this.injector.get(t, An, r);
    return o !== An || n === An ? o : this.parentInjector.get(t, n, r);
  }
};
function Ln(e6, t, n) {
  let r = n ? e6.styles : null, o = n ? e6.classes : null, i = 0;
  if (t !== null)
    for (let s = 0; s < t.length; s++) {
      let a = t[s];
      if (typeof a == "number")
        i = a;
      else if (i == 1)
        o = Br(o, a);
      else if (i == 2) {
        let c = a, l = t[++s];
        r = Br(r, c + ": " + l + ";");
      }
    }
  n ? e6.styles = r : e6.stylesWithoutHost = r, n ? e6.classes = o : e6.classesWithoutHost = o;
}
function kt(e6, t = 0) {
  let n = H();
  if (n === null)
    return I(e6, t);
  let r = Qe();
  return Fa(r, n, k(e6), t);
}
function vf(e6, t, n, r, o) {
  let i = r === null ? null : { "": -1 }, s = o(e6, n);
  if (s !== null) {
    let a = s, c = null, l = null;
    for (let u of s)
      if (u.resolveHostDirectives !== null) {
        [a, c, l] = u.resolveHostDirectives(s);
        break;
      }
    Df(e6, t, n, a, i, c, l);
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
function Df(e6, t, n, r, o, i, s) {
  let a = r.length, c = null;
  for (let p = 0; p < a; p++) {
    let f = r[p];
    c === null && qe(f) && (c = f, If(e6, n, p)), Su(Ra(n, t), e6, f.type);
  }
  bf(n, e6.data.length, a), c?.viewProvidersResolver && c.viewProvidersResolver(c);
  for (let p = 0; p < a; p++) {
    let f = r[p];
    f.providersResolver && f.providersResolver(f);
  }
  let l = false, u = false, d = lc(e6, t, a, null);
  a > 0 && (n.directiveToIndex = /* @__PURE__ */ new Map());
  for (let p = 0; p < a; p++) {
    let f = r[p];
    if (n.mergedAttrs = ti(n.mergedAttrs, f.hostAttrs), Cf(e6, n, t, d, f), Sf(d, f, o), s !== null && s.has(f)) {
      let [sr, el] = s.get(f);
      n.directiveToIndex.set(f.type, [d, sr + n.directiveStart, el + n.directiveStart]);
    } else
      (i === null || !i.has(f)) && n.directiveToIndex.set(f.type, d);
    f.contentQueries !== null && (n.flags |= 4), (f.hostBindings !== null || f.hostAttrs !== null || f.hostVars !== 0) && (n.flags |= 64);
    let T = f.type.prototype;
    !l && (T.ngOnChanges || T.ngOnInit || T.ngDoCheck) && ((e6.preOrderHooks ??= []).push(n.index), l = true), !u && (T.ngOnChanges || T.ngDoCheck) && ((e6.preOrderCheckHooks ??= []).push(n.index), u = true), d++;
  }
  wf(e6, n, i);
}
function wf(e6, t, n) {
  for (let r = t.directiveStart; r < t.directiveEnd; r++) {
    let o = e6.data[r];
    if (n === null || !n.has(o))
      Ia(0, t, o, r), Ia(1, t, o, r), wa(t, r, false);
    else {
      let i = n.get(o);
      Da(0, t, i, r), Da(1, t, i, r), wa(t, r, true);
    }
  }
}
function Ia(e6, t, n, r) {
  let o = e6 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s;
      e6 === 0 ? s = t.inputs ??= {} : s = t.outputs ??= {}, s[i] ??= [], s[i].push(r), Ac(t, i);
    }
}
function Da(e6, t, n, r) {
  let o = e6 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s = o[i], a;
      e6 === 0 ? a = t.hostDirectiveInputs ??= {} : a = t.hostDirectiveOutputs ??= {}, a[s] ??= [], a[s].push(r, i), Ac(t, s);
    }
}
function Ac(e6, t) {
  t === "class" ? e6.flags |= 8 : t === "style" && (e6.flags |= 16);
}
function wa(e6, t, n) {
  let { attrs: r, inputs: o, hostDirectiveInputs: i } = e6;
  if (r === null || !n && o === null || n && i === null || dd(e6)) {
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
      let l = o[c];
      for (let u of l)
        if (u === t) {
          s ??= [], s.push(c, r[a + 1]);
          break;
        }
    } else if (n && i.hasOwnProperty(c)) {
      let l = i[c];
      for (let u = 0; u < l.length; u += 2)
        if (l[u] === t) {
          s ??= [], s.push(l[u + 1], r[a + 1]);
          break;
        }
    }
    a += 2;
  }
  e6.initialInputs ??= [], e6.initialInputs.push(s);
}
function Cf(e6, t, n, r, o) {
  e6.data[r] = o;
  let i = o.factory || (o.factory = $e(o.type, true)), s = new bt(i, qe(o), kt, null);
  e6.blueprint[r] = s, n[r] = s, Tf(e6, t, r, lc(e6, n, o.hostVars, tt), o);
}
function Tf(e6, t, n, r, o) {
  let i = o.hostBindings;
  if (i) {
    let s = e6.hostBindingOpCodes;
    s === null && (s = e6.hostBindingOpCodes = []);
    let a = ~t.index;
    Mf(s) != a && s.push(a), s.push(n, r, i);
  }
}
function Mf(e6) {
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
    qe(t) && (n[""] = e6);
  }
}
function bf(e6, t, n) {
  e6.flags |= 1, e6.directiveStart = t, e6.directiveEnd = t + n, e6.providerIndexes = t;
}
function _f(e6, t, n, r, o, i, s, a) {
  let c = t[y], l = c.consts, u = vt(l, s), d = gi(c, e6, n, r, u);
  return i && vf(c, t, d, vt(l, a), o), d.mergedAttrs = ti(d.mergedAttrs, d.attrs), d.attrs !== null && Ln(d, d.attrs, false), d.mergedAttrs !== null && Ln(d, d.mergedAttrs, true), c.queries !== null && c.queries.elementStart(c, d), d;
}
function Nf(e6, t) {
  yu(e6, t), oo(t) && e6.queries.elementEnd(t);
}
function xf(e6, t, n, r, o, i) {
  let s = t.consts, a = vt(s, o), c = gi(t, e6, n, r, a);
  if (c.mergedAttrs = ti(c.mergedAttrs, c.attrs), i != null) {
    let l = vt(s, i);
    c.localNames = [];
    for (let u = 0; u < l.length; u += 2)
      c.localNames.push(l[u], -1);
  }
  return c.attrs !== null && Ln(c, c.attrs, false), c.mergedAttrs !== null && Ln(c, c.mergedAttrs, true), t.queries !== null && t.queries.elementStart(t, c), c;
}
function Rc(e6, t, n) {
  if (n === tt)
    return false;
  let r = e6[t];
  return Object.is(r, n) ? false : (e6[t] = n, true);
}
var Jo = Symbol("BINDING");
function Af(e6) {
  return e6.debugInfo?.className || e6.type.name || null;
}
var Xo = class extends Zn {
  ngModule;
  constructor(t) {
    super(), this.ngModule = t;
  }
  resolveComponentFactory(t) {
    let n = ut(t);
    return new Pn(n, this.ngModule);
  }
};
function Rf(e6) {
  return Object.keys(e6).map((t) => {
    let [n, r, o] = e6[t], i = { propName: n, templateName: t, isSignal: (r & Gn.SignalBased) !== 0 };
    return o && (i.transform = o), i;
  });
}
function kf(e6) {
  return Object.keys(e6).map((t) => ({ propName: e6[t], templateName: t }));
}
function Of(e6, t, n) {
  let r = t instanceof $ ? t : t?.injector;
  return r && e6.getStandaloneInjector !== null && (r = e6.getStandaloneInjector(r) || r), r ? new Ko(n, r) : n;
}
function Lf(e6) {
  let t = e6.get(Re, null);
  if (t === null)
    throw new g(407, false);
  let n = e6.get(xc, null), r = e6.get(Ue, null), o = e6.get(nt, null, { optional: true });
  return { rendererFactory: t, sanitizer: n, changeDetectionScheduler: r, ngReflect: false, tracingService: o };
}
function Pf(e6, t) {
  let n = kc(e6);
  return rc(t, n, n === "svg" ? bs : n === "math" ? _s : null);
}
function kc(e6) {
  return (e6.selectors[0][0] || "div").toLowerCase();
}
var Pn = class extends qn {
  componentDef;
  ngModule;
  selector;
  componentType;
  ngContentSelectors;
  isBoundToModule;
  cachedInputs = null;
  cachedOutputs = null;
  get inputs() {
    return this.cachedInputs ??= Rf(this.componentDef.inputs), this.cachedInputs;
  }
  get outputs() {
    return this.cachedOutputs ??= kf(this.componentDef.outputs), this.cachedOutputs;
  }
  constructor(t, n) {
    super(), this.componentDef = t, this.ngModule = n, this.componentType = t.type, this.selector = pd(t.selectors), this.ngContentSelectors = t.ngContentSelectors ?? [], this.isBoundToModule = !!n;
  }
  create(t, n, r, o, i, s) {
    M(w.DynamicComponentStart);
    let a = v(null);
    try {
      let c = this.componentDef, l = Of(c, o || this.ngModule, t), u = Lf(l), d = u.tracingService;
      return d && d.componentCreate ? d.componentCreate(Af(c), () => this.createComponentRef(u, l, n, r, i, s)) : this.createComponentRef(u, l, n, r, i, s);
    } finally {
      v(a);
    }
  }
  createComponentRef(t, n, r, o, i, s) {
    let a = this.componentDef, c = Ff(o, a, s, i), l = t.rendererFactory.createRenderer(null, a), u = o ? Vd(l, o, a.encapsulation, n) : Pf(a, l), d = s?.some(Ca) || i?.some((T) => typeof T != "function" && T.bindings.some(Ca)), p = ac(null, c, null, 512 | cc(a), null, null, t, l, n, null, Qa(u, n, true));
    p[U] = u, Cn(p);
    let f = null;
    try {
      let T = _f(U, p, 2, "#host", () => c.directiveRegistry, true, 0);
      ic(l, u, T), _t(u, p), jd(c, p, T), Hu(c, T, p), Nf(c, T), r !== void 0 && Hf(T, this.ngContentSelectors, r), f = pe(T.index, p), p[L] = f[L], vc(c, p, null);
    } catch (T) {
      throw f !== null && Oo(f), Oo(p), T;
    } finally {
      M(w.DynamicComponentEnd), Tn();
    }
    return new Fn(this.componentType, p, !!d);
  }
};
function Ff(e6, t, n, r) {
  let o = e6 ? ["ng-version", "21.2.11"] : hd(t.selectors[0]), i = null, s = null, a = 0;
  if (n)
    for (let u of n)
      a += u[Jo].requiredVars, u.create && (u.targetIdx = 0, (i ??= []).push(u)), u.update && (u.targetIdx = 0, (s ??= []).push(u));
  if (r)
    for (let u = 0; u < r.length; u++) {
      let d = r[u];
      if (typeof d != "function")
        for (let p of d.bindings) {
          a += p[Jo].requiredVars;
          let f = u + 1;
          p.create && (p.targetIdx = f, (i ??= []).push(p)), p.update && (p.targetIdx = f, (s ??= []).push(p));
        }
    }
  let c = [t];
  if (r)
    for (let u of r) {
      let d = typeof u == "function" ? u : u.type, p = Gr(d);
      c.push(p);
    }
  return sc(0, null, jf(i, s), 1, a, c, null, null, null, [o], null);
}
function jf(e6, t) {
  return !e6 && !t ? null : (n) => {
    if (n & 1 && e6)
      for (let r of e6)
        r.create();
    if (n & 2 && t)
      for (let r of t)
        r.update();
  };
}
function Ca(e6) {
  let t = e6[Jo].kind;
  return t === "input" || t === "twoWay";
}
var Fn = class extends Nc {
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
    super(), this._rootLView = n, this._hasInputBindings = r, this._tNode = io(n[y], U), this.location = Va(this._tNode, n), this.instance = pe(this._tNode.index, n)[L], this.hostView = this.changeDetectorRef = new On(n, void 0), this.componentType = t;
  }
  setInput(t, n) {
    this._hasInputBindings;
    let r = this._tNode;
    if (this.previousInputValues ??= /* @__PURE__ */ new Map(), this.previousInputValues.has(t) && Object.is(this.previousInputValues.get(t), n))
      return;
    let o = this._rootLView, i = Yd(r, o[y], o, t, n);
    this.previousInputValues.set(t, n);
    let s = pe(r.index, o);
    _c(s, 1);
  }
  get injector() {
    return new kn(this._tNode, this._rootLView);
  }
  destroy() {
    this.hostView.destroy();
  }
  onDestroy(t) {
    this.hostView.onDestroy(t);
  }
};
function Hf(e6, t, n) {
  let r = e6.projection = [];
  for (let o = 0; o < t.length; o++) {
    let i = n[o];
    r.push(i != null && i.length ? Array.from(i) : null);
  }
}
var jn = class {
};
var xt = class extends jn {
  injector;
  componentFactoryResolver = new Xo(this);
  instance = null;
  constructor(t) {
    super();
    let n = new Ce([...t.providers, { provide: jn, useValue: this }, { provide: Zn, useValue: this.componentFactoryResolver }], t.parent || pt(), t.debugName, /* @__PURE__ */ new Set(["environment"]));
    this.injector = n, t.runEnvironmentInitializers && n.resolveInjectorInitializers();
  }
  destroy() {
    this.injector.destroy();
  }
  onDestroy(t) {
    this.injector.onDestroy(t);
  }
};
function Oc(e6, t, n = null) {
  return new xt({ providers: e6, parent: t, debugName: n, runEnvironmentInitializers: true }).injector;
}
var Vf = (() => {
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
        let r = eo(false, n.type), o = r.length > 0 ? Oc([r], this._injector, "") : null;
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
    static \u0275prov = S({ token: e6, providedIn: "environment", factory: () => new e6(I($)) });
  }
  return e6;
})();
function mi(e6) {
  return Ma(() => {
    let t = zf(e6), n = V(A({}, t), { decls: e6.decls, vars: e6.vars, template: e6.template, consts: e6.consts || null, ngContentSelectors: e6.ngContentSelectors, onPush: e6.changeDetection === ni.OnPush, directiveDefs: null, pipeDefs: null, dependencies: t.standalone && e6.dependencies || null, getStandaloneInjector: t.standalone ? (o) => o.get(Vf).getOrCreateStandaloneInjector(n) : null, getExternalStyles: null, signals: e6.signals ?? false, data: e6.data || {}, encapsulation: e6.encapsulation || z.Emulated, styles: e6.styles || we, _: null, schemas: e6.schemas || null, tView: null, id: "" });
    t.standalone && fc("NgStandalone"), Wf(n);
    let r = e6.dependencies;
    return n.directiveDefs = Ta(r, Bf), n.pipeDefs = Ta(r, hs), n.id = Gf(n), n;
  });
}
function Bf(e6) {
  return ut(e6) || Gr(e6);
}
function $f(e6, t) {
  if (e6 == null)
    return Se;
  let n = {};
  for (let r in e6)
    if (e6.hasOwnProperty(r)) {
      let o = e6[r], i, s, a, c;
      Array.isArray(o) ? (a = o[0], i = o[1], s = o[2] ?? i, c = o[3] || null) : (i = o, s = o, a = Gn.None, c = null), n[i] = [r, a, c], t[i] = s;
    }
  return n;
}
function Uf(e6) {
  if (e6 == null)
    return Se;
  let t = {};
  for (let n in e6)
    e6.hasOwnProperty(n) && (t[e6[n]] = n);
  return t;
}
function zf(e6) {
  let t = {};
  return { type: e6.type, providersResolver: null, viewProvidersResolver: null, factory: null, hostBindings: e6.hostBindings || null, hostVars: e6.hostVars || 0, hostAttrs: e6.hostAttrs || null, contentQueries: e6.contentQueries || null, declaredInputs: t, inputConfig: e6.inputs || Se, exportAs: e6.exportAs || null, standalone: e6.standalone ?? true, signals: e6.signals === true, selectors: e6.selectors || we, viewQuery: e6.viewQuery || null, features: e6.features || null, setInput: null, resolveHostDirectives: null, hostDirectives: null, controlDef: null, inputs: $f(e6.inputs, t), outputs: Uf(e6.outputs), debugInfo: null };
}
function Wf(e6) {
  e6.features?.forEach((t) => t(e6));
}
function Ta(e6, t) {
  return e6 ? () => {
    let n = typeof e6 == "function" ? e6() : e6, r = [];
    for (let o of n) {
      let i = t(o);
      i !== null && r.push(i);
    }
    return r;
  } : null;
}
function Gf(e6) {
  let t = 0, n = typeof e6.consts == "function" ? "" : e6.consts, r = [e6.selectors, e6.ngContentSelectors, e6.hostVars, e6.hostAttrs, n, e6.vars, e6.decls, e6.encapsulation, e6.standalone, e6.signals, e6.exportAs, JSON.stringify(e6.inputs), JSON.stringify(e6.outputs), Object.getOwnPropertyNames(e6.type.prototype), !!e6.contentQueries, !!e6.viewQuery];
  for (let i of r.join("|"))
    t = Math.imul(31, t) + i.charCodeAt(0) << 0;
  return t += 2147483648, "c" + t;
}
var yi = new m("");
function vi(e6) {
  return !!e6 && typeof e6.then == "function";
}
function Lc(e6) {
  return !!e6 && typeof e6.subscribe == "function";
}
var Pc = new m("");
var Ei = (() => {
  class e6 {
    resolve;
    reject;
    initialized = false;
    done = false;
    donePromise = new Promise((n, r) => {
      this.resolve = n, this.reject = r;
    });
    appInits = E(Pc, { optional: true }) ?? [];
    injector = E(ee);
    constructor() {
    }
    runInitializers() {
      if (this.initialized)
        return;
      let n = [];
      for (let o of this.appInits) {
        let i = pn(this.injector, o);
        if (vi(i))
          n.push(i);
        else if (Lc(i)) {
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
    static \u0275prov = S({ token: e6, factory: e6.\u0275fac, providedIn: "root" });
  }
  return e6;
})();
var Fc = new m("");
function jc() {
  hr(() => {
    let e6 = "";
    throw new g(600, e6);
  });
}
function Hc(e6) {
  return e6.isBoundToModule;
}
var qf = 10;
var Ot = (() => {
  class e6 {
    _runningTick = false;
    _destroyed = false;
    _destroyListeners = [];
    _views = [];
    internalErrorHandler = E(Ke);
    afterRenderManager = E(pc);
    zonelessEnabled = E(Tt);
    rootEffectScheduler = E(So);
    dirtyFlags = 0;
    tracingSnapshot = null;
    allTestViews = /* @__PURE__ */ new Set();
    autoDetectTestViews = /* @__PURE__ */ new Set();
    includeAllTestViews = false;
    afterTick = new ae();
    get allViews() {
      return [...(this.includeAllTestViews ? this.allTestViews : this.autoDetectTestViews).keys(), ...this._views];
    }
    get destroyed() {
      return this._destroyed;
    }
    componentTypes = [];
    components = [];
    internalPendingTask = E(Ye);
    get isStable() {
      return this.internalPendingTask.hasPendingTasksObservable.pipe(Tr((n) => !n));
    }
    constructor() {
      E(nt, { optional: true });
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
    _injector = E($);
    _rendererFactory = null;
    get injector() {
      return this._injector;
    }
    bootstrap(n, r) {
      return this.bootstrapImpl(n, r);
    }
    bootstrapImpl(n, r, o = ee.NULL) {
      return this._injector.get(j).run(() => {
        M(w.BootstrapComponentStart);
        let s = n instanceof qn;
        if (!this._injector.get(Ei).done) {
          let T = "";
          throw new g(405, T);
        }
        let c;
        s ? c = n : c = this._injector.get(Zn).resolveComponentFactory(n), this.componentTypes.push(c.componentType);
        let l = Hc(c) ? void 0 : this._injector.get(jn), u = r || c.selector, d = c.create(o, [], u, l), p = d.location.nativeElement, f = d.injector.get(yi, null);
        return f?.registerApplication(p), d.onDestroy(() => {
          this.detachView(d.hostView), St(this.components, d), f?.unregisterApplication(p);
        }), this._loadComponent(d), M(w.BootstrapComponentEnd, d), d;
      });
    }
    tick() {
      this.zonelessEnabled || (this.dirtyFlags |= 1), this._tick();
    }
    _tick() {
      M(w.ChangeDetectionStart), this.tracingSnapshot !== null ? this.tracingSnapshot.run(di.CHANGE_DETECTION, this.tickImpl) : this.tickImpl();
    }
    tickImpl = () => {
      if (this._runningTick)
        throw M(w.ChangeDetectionEnd), new g(101, false);
      let n = v(null);
      try {
        this._runningTick = true, this.synchronize();
      } finally {
        this._runningTick = false, this.tracingSnapshot?.dispose(), this.tracingSnapshot = null, v(n), this.afterTick.next(), M(w.ChangeDetectionEnd);
      }
    };
    synchronize() {
      this._rendererFactory === null && !this._injector.destroyed && (this._rendererFactory = this._injector.get(Re, null, { optional: true }));
      let n = 0;
      for (; this.dirtyFlags !== 0 && n++ < qf; ) {
        M(w.ChangeDetectionSyncStart);
        try {
          this.synchronizeOnce();
        } finally {
          M(w.ChangeDetectionSyncEnd);
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
          if (!r && !Et(o))
            continue;
          let i = r && !this.zonelessEnabled ? 0 : 1;
          Tc(o, i), n = true;
        }
        if (this.dirtyFlags &= -5, this.syncDirtyFlagsWithViews(), this.dirtyFlags & 23)
          return;
      }
      n || (this._rendererFactory?.begin?.(), this._rendererFactory?.end?.()), this.dirtyFlags & 8 && (this.dirtyFlags &= -9, this.afterRenderManager.execute()), this.syncDirtyFlagsWithViews();
    }
    syncDirtyFlagsWithViews() {
      if (this.allViews.some(({ _lView: n }) => Et(n))) {
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
      St(this._views, r), r.detachFromAppRef();
    }
    _loadComponent(n) {
      this.attachView(n.hostView);
      try {
        this.tick();
      } catch (o) {
        this.internalErrorHandler(o);
      }
      this.components.push(n), this._injector.get(Fc, []).forEach((o) => o(n));
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
      return this._destroyListeners.push(n), () => St(this._destroyListeners, n);
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
    static \u0275prov = S({ token: e6, factory: e6.\u0275fac, providedIn: "root" });
  }
  return e6;
})();
function St(e6, t) {
  let n = e6.indexOf(t);
  n > -1 && e6.splice(n, 1);
}
function Oe(e6, t, n, r) {
  let o = H(), i = o[y], s = e6 + U, a = i.firstCreatePass ? xf(s, i, 2, t, n, r) : i.data[s];
  return Zd(a, o, e6, t, Zf), r != null && Hd(o, a), Oe;
}
function ye() {
  let e6 = Qe(), t = Qd(e6);
  return Ls(t) && Ps(), ks(), ye;
}
function Qn(e6, t, n, r) {
  return Oe(e6, t, n, r), ye(), Qn;
}
var Zf = (e6, t, n, r, o) => (Io(true), rc(t[P], r, qs()));
function Yn(e6, t, n) {
  let r = H(), o = go();
  if (Rc(r, o, t)) {
    let i = Dn(), s = Gs();
    Ud(s, r, e6, t, r[P], n);
  }
  return Yn;
}
var Lt = "en-US";
var Qf = Lt;
function Vc(e6) {
  typeof e6 == "string" && (Qf = e6.toLowerCase().replace(/_/g, "-"));
}
function Pt(e6, t = "") {
  let n = H(), r = Dn(), o = e6 + U, i = r.firstCreatePass ? gi(r, o, 1, t, null) : r.data[o], s = Yf(r, n, i, t);
  n[o] = s, Eo() && mc(r, n, s, i), Dt(i, false);
}
var Yf = (e6, t, n, r) => (Io(true), od(t[P], r));
function Kf(e6, t, n, r = "") {
  return Rc(e6, go(), n) ? t + Zr(n) + r : tt;
}
function Kn(e6, t, n) {
  let r = H(), o = Kf(r, e6, t, n);
  return o !== tt && Jf(r, Mn(), o), Kn;
}
function Jf(e6, t, n) {
  let r = Ns(t, e6);
  id(e6[P], r, n);
}
var Bc = (() => {
  class e6 {
    applicationErrorHandler = E(Ke);
    appRef = E(Ot);
    taskService = E(Ye);
    ngZone = E(j);
    zonelessEnabled = E(Tt);
    tracing = E(nt, { optional: true });
    zoneIsDefined = typeof Zone < "u" && !!Zone.root.run;
    schedulerTickApplyArgs = [{ data: { __scheduler_tick__: true } }];
    subscriptions = new _();
    angularZoneId = this.zoneIsDefined ? this.ngZone._inner?.get(ct) : null;
    scheduleInRootZone = !this.zonelessEnabled && this.zoneIsDefined && (E(Mo, { optional: true }) ?? false);
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
      let r = this.useMicrotaskScheduler ? Js : Do;
      this.pendingRenderTaskId = this.taskService.add(), this.scheduleInRootZone ? this.cancelScheduledCallback = Zone.root.run(() => r(() => this.tick())) : this.cancelScheduledCallback = this.ngZone.runOutsideAngular(() => r(() => this.tick()));
    }
    shouldScheduleTick() {
      return !(this.appRef.destroyed || this.pendingRenderTaskId !== null || this.runningTick || this.appRef._runningTick || !this.zonelessEnabled && this.zoneIsDefined && Zone.current.get(ct + this.angularZoneId));
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
    static \u0275prov = S({ token: e6, factory: e6.\u0275fac, providedIn: "root" });
  }
  return e6;
})();
function $c() {
  return [{ provide: Ue, useExisting: Bc }, { provide: j, useClass: lt }, { provide: Tt, useValue: true }];
}
function Xf() {
  return typeof $localize < "u" && $localize.locale || Lt;
}
var Ii = new m("", { factory: () => E(Ii, { optional: true, skipSelf: true }) || Xf() });
var Di = new m("");
var lp = new m("");
function Ft(e6) {
  return !e6.moduleRef;
}
function up(e6) {
  let t = Ft(e6) ? e6.r3Injector : e6.moduleRef.injector, n = t.get(j);
  return n.run(() => {
    Ft(e6) ? e6.r3Injector.resolveInjectorInitializers() : e6.moduleRef.resolveInjectorInitializers();
    let r = t.get(Ke), o;
    if (n.runOutsideAngular(() => {
      o = n.onError.subscribe({ next: r });
    }), Ft(e6)) {
      let i = () => t.destroy(), s = e6.platformInjector.get(Di);
      s.add(i), t.onDestroy(() => {
        o.unsubscribe(), s.delete(i);
      });
    } else {
      let i = () => e6.moduleRef.destroy(), s = e6.platformInjector.get(Di);
      s.add(i), e6.moduleRef.onDestroy(() => {
        St(e6.allPlatformModules, e6.moduleRef), o.unsubscribe(), s.delete(i);
      });
    }
    return fp(r, n, () => {
      let i = t.get(Ye), s = i.add(), a = t.get(Ei);
      return a.runInitializers(), a.donePromise.then(() => {
        let c = t.get(Ii, Lt);
        if (Vc(c || Lt), !t.get(lp, true))
          return Ft(e6) ? t.get(Ot) : (e6.allPlatformModules.push(e6.moduleRef), e6.moduleRef);
        if (Ft(e6)) {
          let u = t.get(Ot);
          return e6.rootComponent !== void 0 && u.bootstrap(e6.rootComponent), u;
        } else
          return dp?.(e6.moduleRef, e6.allPlatformModules), e6.moduleRef;
      }).finally(() => {
        i.remove(s);
      });
    });
  });
}
var dp;
function fp(e6, t, n) {
  try {
    let r = n();
    return vi(r) ? r.catch((o) => {
      throw t.runOutsideAngular(() => e6(o)), o;
    }) : r;
  } catch (r) {
    throw t.runOutsideAngular(() => e6(r)), r;
  }
}
var Jn = null;
function pp(e6 = [], t) {
  return ee.create({ name: t, providers: [{ provide: ft, useValue: "platform" }, { provide: Di, useValue: /* @__PURE__ */ new Set([() => Jn = null]) }, ...e6] });
}
function hp(e6 = []) {
  if (Jn)
    return Jn;
  let t = pp(e6);
  return Jn = t, jc(), gp(t), t;
}
function gp(e6) {
  let t = e6.get(Vn, null);
  pn(e6, () => {
    t?.forEach((n) => n());
  });
}
var mp = 1e4;
var pT = mp - 1e3;
function zc(e6) {
  let { rootComponent: t, appProviders: n, platformProviders: r, platformRef: o } = e6;
  M(w.BootstrapApplicationStart);
  try {
    let i = o?.injector ?? hp(r), s = [$c(), ea, ...n || []], a = new xt({ providers: s, parent: i, debugName: "", runEnvironmentInitializers: false });
    return up({ r3Injector: a.injector, platformInjector: i, rootComponent: t });
  } catch (i) {
    return Promise.reject(i);
  } finally {
    M(w.BootstrapApplicationEnd);
  }
}
var Wc = null;
function rt() {
  return Wc;
}
function wi(e6) {
  Wc ??= e6;
}
var jt = class {
};
function Ci(e6, t) {
  t = encodeURIComponent(t);
  for (let n of e6.split(";")) {
    let r = n.indexOf("="), [o, i] = r == -1 ? [n, ""] : [n.slice(0, r), n.slice(r + 1)];
    if (o.trim() === t)
      return decodeURIComponent(i);
  }
  return null;
}
var Ht = class {
};
var Gc = "browser";
var Vt = class {
  _doc;
  constructor(t) {
    this._doc = t;
  }
  manager;
};
var er = (() => {
  class e6 extends Vt {
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
      return new (r || e6)(I(x));
    };
    static \u0275prov = S({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var rr = new m("");
var bi = (() => {
  class e6 {
    _zone;
    _plugins;
    _eventNameToPlugin = /* @__PURE__ */ new Map();
    constructor(n, r) {
      this._zone = r, n.forEach((s) => {
        s.manager = this;
      });
      let o = n.filter((s) => !(s instanceof er));
      this._plugins = o.slice().reverse();
      let i = n.find((s) => s instanceof er);
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
      return new (r || e6)(I(rr), I(j));
    };
    static \u0275prov = S({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var Ti = "ng-app-id";
function qc(e6) {
  for (let t of e6)
    t.remove();
}
function Zc(e6, t) {
  let n = t.createElement("style");
  return n.textContent = e6, n;
}
function yp(e6, t, n, r) {
  let o = e6.head?.querySelectorAll(`style[${Ti}="${t}"],link[${Ti}="${t}"]`);
  if (o)
    for (let i of o)
      i.removeAttribute(Ti), i instanceof HTMLLinkElement ? r.set(i.href.slice(i.href.lastIndexOf("/") + 1), { usage: 0, elements: [i] }) : i.textContent && n.set(i.textContent, { usage: 0, elements: [i] });
}
function Si(e6, t) {
  let n = t.createElement("link");
  return n.setAttribute("rel", "stylesheet"), n.setAttribute("href", e6), n;
}
var _i = (() => {
  class e6 {
    doc;
    appId;
    nonce;
    inline = /* @__PURE__ */ new Map();
    external = /* @__PURE__ */ new Map();
    hosts = /* @__PURE__ */ new Set();
    constructor(n, r, o, i = {}) {
      this.doc = n, this.appId = r, this.nonce = o, yp(n, r, this.inline, this.external), this.hosts.add(n.head);
    }
    addStyles(n, r) {
      for (let o of n)
        this.addUsage(o, this.inline, Zc);
      r?.forEach((o) => this.addUsage(o, this.external, Si));
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
      o && (o.usage--, o.usage <= 0 && (qc(o.elements), r.delete(n)));
    }
    ngOnDestroy() {
      for (let [, { elements: n }] of [...this.inline, ...this.external])
        qc(n);
      this.hosts.clear();
    }
    addHost(n) {
      this.hosts.add(n);
      for (let [r, { elements: o }] of this.inline)
        o.push(this.addElement(n, Zc(r, this.doc)));
      for (let [r, { elements: o }] of this.external)
        o.push(this.addElement(n, Si(r, this.doc)));
    }
    removeHost(n) {
      this.hosts.delete(n);
    }
    addElement(n, r) {
      return this.nonce && r.setAttribute("nonce", this.nonce), n.appendChild(r);
    }
    static \u0275fac = function(r) {
      return new (r || e6)(I(x), I(Hn), I(Bn, 8), I(At));
    };
    static \u0275prov = S({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var Mi = { svg: "http://www.w3.org/2000/svg", xhtml: "http://www.w3.org/1999/xhtml", xlink: "http://www.w3.org/1999/xlink", xml: "http://www.w3.org/XML/1998/namespace", xmlns: "http://www.w3.org/2000/xmlns/", math: "http://www.w3.org/1998/Math/MathML" };
var Ni = /%COMP%/g;
var Yc = "%COMP%";
var vp = `_nghost-${Yc}`;
var Ep = `_ngcontent-${Yc}`;
var Ip = true;
var Dp = new m("", { factory: () => Ip });
function wp(e6) {
  return Ep.replace(Ni, e6);
}
function Cp(e6) {
  return vp.replace(Ni, e6);
}
function Kc(e6, t) {
  return t.map((n) => n.replace(Ni, e6));
}
var xi = (() => {
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
    constructor(n, r, o, i, s, a, c = null, l = null) {
      this.eventManager = n, this.sharedStylesHost = r, this.appId = o, this.removeStylesOnCompDestroy = i, this.doc = s, this.ngZone = a, this.nonce = c, this.tracingService = l, this.defaultRenderer = new Bt(n, s, a, this.tracingService);
    }
    createRenderer(n, r) {
      if (!n || !r)
        return this.defaultRenderer;
      let o = this.getOrCreateRenderer(n, r);
      return o instanceof nr ? o.applyToHost(n) : o instanceof $t && o.applyStyles(), o;
    }
    getOrCreateRenderer(n, r) {
      let o = this.rendererByCompId, i = o.get(r.id);
      if (!i) {
        let s = this.doc, a = this.ngZone, c = this.eventManager, l = this.sharedStylesHost, u = this.removeStylesOnCompDestroy, d = this.tracingService;
        switch (r.encapsulation) {
          case z.Emulated:
            i = new nr(c, l, r, this.appId, u, s, a, d);
            break;
          case z.ShadowDom:
            return new tr(c, n, r, s, a, this.nonce, d, l);
          case z.ExperimentalIsolatedShadowDom:
            return new tr(c, n, r, s, a, this.nonce, d);
          default:
            i = new $t(c, l, r, u, s, a, d);
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
      return new (r || e6)(I(bi), I(_i), I(Hn), I(Dp), I(x), I(j), I(Bn), I(nt, 8));
    };
    static \u0275prov = S({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var Bt = class {
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
    return n ? this.doc.createElementNS(Mi[n] || n, t) : this.doc.createElement(t);
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
      let i = Mi[o];
      i ? t.setAttributeNS(i, n, r) : t.setAttribute(n, r);
    } else
      t.setAttribute(n, r);
  }
  removeAttribute(t, n, r) {
    if (r) {
      let o = Mi[r];
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
    o & (ke.DashCase | ke.Important) ? t.style.setProperty(n, r, o & ke.Important ? "important" : "") : t.style[n] = r;
  }
  removeStyle(t, n, r) {
    r & ke.DashCase ? t.style.removeProperty(n) : t.style[n] = "";
  }
  setProperty(t, n, r) {
    t != null && (t[n] = r);
  }
  setValue(t, n) {
    t.nodeValue = n;
  }
  listen(t, n, r, o) {
    if (typeof t == "string" && (t = rt().getGlobalEventTarget(this.doc, t), !t))
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
var tr = class extends Bt {
  hostEl;
  sharedStylesHost;
  shadowRoot;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, o, i, a), this.hostEl = n, this.sharedStylesHost = c, this.shadowRoot = n.attachShadow({ mode: "open" }), this.sharedStylesHost && this.sharedStylesHost.addHost(this.shadowRoot);
    let l = r.styles;
    l = Kc(r.id, l);
    for (let d of l) {
      let p = document.createElement("style");
      s && p.setAttribute("nonce", s), p.textContent = d, this.shadowRoot.appendChild(p);
    }
    let u = r.getExternalStyles?.();
    if (u)
      for (let d of u) {
        let p = Si(d, o);
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
var $t = class extends Bt {
  sharedStylesHost;
  removeStylesOnCompDestroy;
  styles;
  styleUrls;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, i, s, a), this.sharedStylesHost = n, this.removeStylesOnCompDestroy = o;
    let l = r.styles;
    this.styles = c ? Kc(c, l) : l, this.styleUrls = r.getExternalStyles?.(c);
  }
  applyStyles() {
    this.sharedStylesHost.addStyles(this.styles, this.styleUrls);
  }
  destroy() {
    this.removeStylesOnCompDestroy && et.size === 0 && this.sharedStylesHost.removeStyles(this.styles, this.styleUrls);
  }
};
var nr = class extends $t {
  contentAttr;
  hostAttr;
  constructor(t, n, r, o, i, s, a, c) {
    let l = o + "-" + r.id;
    super(t, n, r, i, s, a, c, l), this.contentAttr = wp(l), this.hostAttr = Cp(l);
  }
  applyToHost(t) {
    this.applyStyles(), this.setAttribute(t, this.hostAttr, "");
  }
  createElement(t, n) {
    let r = super.createElement(t, n);
    return super.setAttribute(r, this.contentAttr, ""), r;
  }
};
var or = class e4 extends jt {
  supportsDOMEvents = true;
  static makeCurrent() {
    wi(new e4());
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
    let n = Tp();
    return n == null ? null : Mp(n);
  }
  resetBaseElement() {
    Ut = null;
  }
  getUserAgent() {
    return window.navigator.userAgent;
  }
  getCookie(t) {
    return Ci(document.cookie, t);
  }
};
var Ut = null;
function Tp() {
  return Ut = Ut || document.head.querySelector("base"), Ut ? Ut.getAttribute("href") : null;
}
function Mp(e6) {
  return new URL(e6, document.baseURI).pathname;
}
var Sp = (() => {
  class e6 {
    build() {
      return new XMLHttpRequest();
    }
    static \u0275fac = function(r) {
      return new (r || e6)();
    };
    static \u0275prov = S({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
var Jc = ["alt", "control", "meta", "shift"];
var bp = { "\b": "Backspace", "	": "Tab", "\x7F": "Delete", "\x1B": "Escape", Del: "Delete", Esc: "Escape", Left: "ArrowLeft", Right: "ArrowRight", Up: "ArrowUp", Down: "ArrowDown", Menu: "ContextMenu", Scroll: "ScrollLock", Win: "OS" };
var _p = { alt: (e6) => e6.altKey, control: (e6) => e6.ctrlKey, meta: (e6) => e6.metaKey, shift: (e6) => e6.shiftKey };
var Xc = (() => {
  class e6 extends Vt {
    constructor(n) {
      super(n);
    }
    supports(n) {
      return e6.parseEventName(n) != null;
    }
    addEventListener(n, r, o, i) {
      let s = e6.parseEventName(r), a = e6.eventCallback(s.fullKey, o, this.manager.getZone());
      return this.manager.getZone().runOutsideAngular(() => rt().onAndCancel(n, s.domEventName, a, i));
    }
    static parseEventName(n) {
      let r = n.toLowerCase().split("."), o = r.shift();
      if (r.length === 0 || !(o === "keydown" || o === "keyup"))
        return null;
      let i = e6._normalizeKey(r.pop()), s = "", a = r.indexOf("code");
      if (a > -1 && (r.splice(a, 1), s = "code."), Jc.forEach((l) => {
        let u = r.indexOf(l);
        u > -1 && (r.splice(u, 1), s += l + ".");
      }), s += i, r.length != 0 || i.length === 0)
        return null;
      let c = {};
      return c.domEventName = o, c.fullKey = s, c;
    }
    static matchEventFullKeyCode(n, r) {
      let o = bp[n.key] || n.key, i = "";
      return r.indexOf("code.") > -1 && (o = n.code, i = "code."), o == null || !o ? false : (o = o.toLowerCase(), o === " " ? o = "space" : o === "." && (o = "dot"), Jc.forEach((s) => {
        if (s !== o) {
          let a = _p[s];
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
      return new (r || e6)(I(x));
    };
    static \u0275prov = S({ token: e6, factory: e6.\u0275fac });
  }
  return e6;
})();
async function Ai(e6, t, n) {
  let r = A({ rootComponent: e6 }, Np(t, n));
  return zc(r);
}
function Np(e6, t) {
  return { platformRef: t?.platformRef, appProviders: [...Op, ...e6?.providers ?? []], platformProviders: kp };
}
function xp() {
  or.makeCurrent();
}
function Ap() {
  return new te();
}
function Rp() {
  return ri(document), document;
}
var kp = [{ provide: At, useValue: Gc }, { provide: Vn, useValue: xp, multi: true }, { provide: x, useFactory: Rp }];
var Op = [{ provide: ft, useValue: "root" }, { provide: te, useFactory: Ap }, { provide: rr, useClass: er, multi: true }, { provide: rr, useClass: Xc, multi: true }, xi, _i, bi, { provide: Re, useExisting: xi }, { provide: Ht, useClass: Sp }, []];
var Ri = (() => {
  class e6 {
    static \u0275fac = function(r) {
      return new (r || e6)();
    };
    static \u0275prov = S({ token: e6, factory: function(r) {
      let o = null;
      return r ? o = new (r || e6)() : o = I(Lp), o;
    }, providedIn: "root" });
  }
  return e6;
})();
var Lp = (() => {
  class e6 extends Ri {
    _doc;
    constructor(n) {
      super(), this._doc = n;
    }
    sanitize(n, r) {
      if (r == null)
        return null;
      switch (n) {
        case K.NONE:
          return r;
        case K.HTML:
          return me(r, "HTML") ? ge(r) : zn(this._doc, String(r)).toString();
        case K.STYLE:
          return me(r, "Style") ? ge(r) : r;
        case K.SCRIPT:
          if (me(r, "Script"))
            return ge(r);
          throw new g(5200, false);
        case K.URL:
          return me(r, "URL") ? ge(r) : Un(String(r));
        case K.RESOURCE_URL:
          if (me(r, "ResourceURL"))
            return ge(r);
          throw new g(5201, false);
        default:
          throw new g(5202, false);
      }
    }
    bypassSecurityTrustHtml(n) {
      return ii(n);
    }
    bypassSecurityTrustStyle(n) {
      return si(n);
    }
    bypassSecurityTrustScript(n) {
      return ai(n);
    }
    bypassSecurityTrustUrl(n) {
      return ci(n);
    }
    bypassSecurityTrustResourceUrl(n) {
      return li(n);
    }
    static \u0275fac = function(r) {
      return new (r || e6)(I(x));
    };
    static \u0275prov = S({ token: e6, factory: e6.\u0275fac, providedIn: "root" });
  }
  return e6;
})();
var ir = class e5 {
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
  message = Ct("Waiting for model...");
  sanitizedHtml = Ct("");
  static \u0275fac = function(n) {
    return new (n || e5)(kt("ANYWIDGET_MODEL"), kt(Ri));
  };
  static \u0275cmp = mi({ type: e5, selectors: [["app-root"]], decls: 8, vars: 2, consts: [[1, "angular-widget"], [3, "innerHTML"]], template: function(n, r) {
    n & 1 && (Oe(0, "div", 0)(1, "h3"), Pt(2, "Angular Hybrid Widget"), ye(), Oe(3, "p"), Pt(4, "Status: Infrastructure Loaded"), ye(), Oe(5, "p"), Pt(6), ye(), Qn(7, "div", 1), ye()), n & 2 && (Wn(6), Kn("Message from Python: ", r.message()), Wn(), Yn("innerHTML", r.sanitizedHtml(), ui));
  }, styles: [".angular-widget[_ngcontent-%COMP%]{background-color:#f9f9f9;border:1px solid #ccc;border-radius:4px;padding:10px}"] });
};
function Fp({ model: e6, el: t }) {
  let n = document.createElement("app-root");
  t.appendChild(n);
  let r = { providers: [To(), { provide: "ANYWIDGET_MODEL", useValue: e6 }] };
  Ai(ir, r).catch((o) => console.error(o));
}
var EM = { render: Fp };
export {
  EM as default
};
