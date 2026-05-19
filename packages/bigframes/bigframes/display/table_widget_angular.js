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
var rd = Object.defineProperty;
var od = Object.defineProperties;
var id = Object.getOwnPropertyDescriptors;
var Ea = Object.getOwnPropertySymbols;
var sd = Object.prototype.hasOwnProperty;
var ad = Object.prototype.propertyIsEnumerable;
var Ia = (e12, t, n) => t in e12 ? rd(e12, t, { enumerable: true, configurable: true, writable: true, value: n }) : e12[t] = n;
var N = (e12, t) => {
  for (var n in t ||= {})
    sd.call(t, n) && Ia(e12, n, t[n]);
  if (Ea)
    for (var n of Ea(t))
      ad.call(t, n) && Ia(e12, n, t[n]);
  return e12;
};
var A = (e12, t) => od(e12, id(t));
var L = null;
var Sn = false;
var yo = 1;
var cd = null;
var Z = Symbol("SIGNAL");
function g(e12) {
  let t = L;
  return L = e12, t;
}
function xn() {
  return L;
}
var lt = { version: 0, lastCleanEpoch: 0, dirty: false, producers: void 0, producersTail: void 0, consumers: void 0, consumersTail: void 0, recomputing: false, consumerAllowSignalWrites: false, consumerIsAlwaysLive: false, kind: "unknown", producerMustRecompute: () => false, producerRecomputeValue: () => {
}, consumerMarkedDirty: () => {
}, consumerOnSignalRead: () => {
} };
function vo(e12) {
  if (Sn)
    throw new Error("");
  if (L === null)
    return;
  L.consumerOnSignalRead(e12);
  let t = L.producersTail;
  if (t !== void 0 && t.producer === e12)
    return;
  let n, r = L.recomputing;
  if (r && (n = t !== void 0 ? t.nextProducer : L.producers, n !== void 0 && n.producer === e12)) {
    L.producersTail = n, n.lastReadVersion = e12.version;
    return;
  }
  let o = e12.consumersTail;
  if (o !== void 0 && o.consumer === L && (!r || ud(o, L)))
    return;
  let i = dt(L), s = { producer: e12, consumer: L, nextProducer: n, prevConsumer: o, lastReadVersion: e12.version, nextConsumer: void 0 };
  L.producersTail = s, t !== void 0 ? t.nextProducer = s : L.producers = s, i && Ca(e12, s);
}
function Da() {
  yo++;
}
function Eo(e12) {
  if (!(dt(e12) && !e12.dirty) && !(!e12.dirty && e12.lastCleanEpoch === yo)) {
    if (!e12.producerMustRecompute(e12) && !Rn(e12)) {
      mo(e12);
      return;
    }
    e12.producerRecomputeValue(e12), mo(e12);
  }
}
function Io(e12) {
  if (e12.consumers === void 0)
    return;
  let t = Sn;
  Sn = true;
  try {
    for (let n = e12.consumers; n !== void 0; n = n.nextConsumer) {
      let r = n.consumer;
      r.dirty || ld(r);
    }
  } finally {
    Sn = t;
  }
}
function Do() {
  return L?.consumerAllowSignalWrites !== false;
}
function ld(e12) {
  e12.dirty = true, Io(e12), e12.consumerMarkedDirty?.(e12);
}
function mo(e12) {
  e12.dirty = false, e12.lastCleanEpoch = yo;
}
function Vt(e12) {
  return e12 && wa(e12), g(e12);
}
function wa(e12) {
  e12.producersTail = void 0, e12.recomputing = true;
}
function An(e12, t) {
  g(t), e12 && ba(e12);
}
function ba(e12) {
  e12.recomputing = false;
  let t = e12.producersTail, n = t !== void 0 ? t.nextProducer : e12.producers;
  if (n !== void 0) {
    if (dt(e12))
      do
        n = wo(n);
      while (n !== void 0);
    t !== void 0 ? t.nextProducer = void 0 : e12.producers = void 0;
  }
}
function Rn(e12) {
  for (let t = e12.producers; t !== void 0; t = t.nextProducer) {
    let n = t.producer, r = t.lastReadVersion;
    if (r !== n.version || (Eo(n), r !== n.version))
      return true;
  }
  return false;
}
function ut(e12) {
  if (dt(e12)) {
    let t = e12.producers;
    for (; t !== void 0; )
      t = wo(t);
  }
  e12.producers = void 0, e12.producersTail = void 0, e12.consumers = void 0, e12.consumersTail = void 0;
}
function Ca(e12, t) {
  let n = e12.consumersTail, r = dt(e12);
  if (n !== void 0 ? (t.nextConsumer = n.nextConsumer, n.nextConsumer = t) : (t.nextConsumer = void 0, e12.consumers = t), t.prevConsumer = n, e12.consumersTail = t, !r)
    for (let o = e12.producers; o !== void 0; o = o.nextProducer)
      Ca(o.producer, o);
}
function wo(e12) {
  let t = e12.producer, n = e12.nextProducer, r = e12.nextConsumer, o = e12.prevConsumer;
  if (e12.nextConsumer = void 0, e12.prevConsumer = void 0, r !== void 0 ? r.prevConsumer = o : t.consumersTail = o, o !== void 0)
    o.nextConsumer = r;
  else if (t.consumers = r, !dt(t)) {
    let i = t.producers;
    for (; i !== void 0; )
      i = wo(i);
  }
  return n;
}
function dt(e12) {
  return e12.consumerIsAlwaysLive || e12.consumers !== void 0;
}
function bo(e12) {
  cd?.(e12);
}
function ud(e12, t) {
  let n = t.producersTail;
  if (n !== void 0) {
    let r = t.producers;
    do {
      if (r === e12)
        return true;
      if (r === n)
        break;
      r = r.nextProducer;
    } while (r !== void 0);
  }
  return false;
}
function Co(e12, t) {
  return Object.is(e12, t);
}
function On(e12, t) {
  let n = Object.create(dd);
  n.computation = e12, t !== void 0 && (n.equal = t);
  let r = () => {
    if (Eo(n), vo(n), n.value === Nn)
      throw n.error;
    return n.value;
  };
  return r[Z] = n, bo(n), r;
}
var ho = Symbol("UNSET");
var go = Symbol("COMPUTING");
var Nn = Symbol("ERRORED");
var dd = A(N({}, lt), { value: ho, dirty: true, error: null, equal: Co, kind: "computed", producerMustRecompute(e12) {
  return e12.value === ho || e12.value === go;
}, producerRecomputeValue(e12) {
  if (e12.value === go)
    throw new Error("");
  let t = e12.value;
  e12.value = go;
  let n = Vt(e12), r, o = false;
  try {
    r = e12.computation(), g(null), o = t !== ho && t !== Nn && r !== Nn && e12.equal(t, r);
  } catch (i) {
    r = Nn, e12.error = i;
  } finally {
    An(e12, n);
  }
  if (o) {
    e12.value = t;
    return;
  }
  e12.value = r, e12.version++;
} });
function fd() {
  throw new Error();
}
var Ta = fd;
function Ma(e12) {
  Ta(e12);
}
function To(e12) {
  Ta = e12;
}
var pd = null;
function Mo(e12, t) {
  let n = Object.create(Na);
  n.value = e12, t !== void 0 && (n.equal = t);
  let r = () => _a(n);
  return r[Z] = n, bo(n), [r, (s) => _o(n, s), (s) => Sa(n, s)];
}
function _a(e12) {
  return vo(e12), e12.value;
}
function _o(e12, t) {
  Do() || Ma(e12), e12.equal(e12.value, t) || (e12.value = t, hd(e12));
}
function Sa(e12, t) {
  Do() || Ma(e12), _o(e12, t(e12.value));
}
var Na = A(N({}, lt), { equal: Co, value: void 0, kind: "signal" });
function hd(e12) {
  e12.version++, Da(), Io(e12), pd?.(e12);
}
var So = A(N({}, lt), { consumerIsAlwaysLive: true, consumerAllowSignalWrites: true, dirty: true, kind: "effect" });
function No(e12) {
  if (e12.dirty = false, e12.version > 0 && !Rn(e12))
    return;
  e12.version++;
  let t = Vt(e12);
  try {
    e12.cleanup(), e12.fn();
  } finally {
    An(e12, t);
  }
}
function $(e12) {
  return typeof e12 == "function";
}
function kn(e12) {
  let n = e12((r) => {
    Error.call(r), r.stack = new Error().stack;
  });
  return n.prototype = Object.create(Error.prototype), n.prototype.constructor = n, n;
}
var Pn = kn((e12) => function(n) {
  e12(this), this.message = n ? `${n.length} errors occurred during unsubscription:
${n.map((r, o) => `${o + 1}) ${r.toString()}`).join(`
  `)}` : "", this.name = "UnsubscriptionError", this.errors = n;
});
function Bt(e12, t) {
  if (e12) {
    let n = e12.indexOf(t);
    0 <= n && e12.splice(n, 1);
  }
}
var H = class e {
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
      if ($(r))
        try {
          r();
        } catch (i) {
          t = i instanceof Pn ? i.errors : [i];
        }
      let { _finalizers: o } = this;
      if (o) {
        this._finalizers = null;
        for (let i of o)
          try {
            xa(i);
          } catch (s) {
            t = t ?? [], s instanceof Pn ? t = [...t, ...s.errors] : t.push(s);
          }
      }
      if (t)
        throw new Pn(t);
    }
  }
  add(t) {
    var n;
    if (t && t !== this)
      if (this.closed)
        xa(t);
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
    n === t ? this._parentage = null : Array.isArray(n) && Bt(n, t);
  }
  remove(t) {
    let { _finalizers: n } = this;
    n && Bt(n, t), t instanceof e && t._removeParent(this);
  }
};
H.EMPTY = (() => {
  let e12 = new H();
  return e12.closed = true, e12;
})();
var xo = H.EMPTY;
function Ln(e12) {
  return e12 instanceof H || e12 && "closed" in e12 && $(e12.remove) && $(e12.add) && $(e12.unsubscribe);
}
function xa(e12) {
  $(e12) ? e12() : e12.unsubscribe();
}
var te = { onUnhandledError: null, onStoppedNotification: null, Promise: void 0, useDeprecatedSynchronousErrorHandling: false, useDeprecatedNextContext: false };
var ft = { setTimeout(e12, t, ...n) {
  let { delegate: r } = ft;
  return r?.setTimeout ? r.setTimeout(e12, t, ...n) : setTimeout(e12, t, ...n);
}, clearTimeout(e12) {
  let { delegate: t } = ft;
  return (t?.clearTimeout || clearTimeout)(e12);
}, delegate: void 0 };
function Aa(e12) {
  ft.setTimeout(() => {
    let { onUnhandledError: t } = te;
    if (t)
      t(e12);
    else
      throw e12;
  });
}
function Ao() {
}
var Ra = Ro("C", void 0, void 0);
function Oa(e12) {
  return Ro("E", void 0, e12);
}
function ka(e12) {
  return Ro("N", e12, void 0);
}
function Ro(e12, t, n) {
  return { kind: e12, value: t, error: n };
}
var Ue = null;
function pt(e12) {
  if (te.useDeprecatedSynchronousErrorHandling) {
    let t = !Ue;
    if (t && (Ue = { errorThrown: false, error: null }), e12(), t) {
      let { errorThrown: n, error: r } = Ue;
      if (Ue = null, n)
        throw r;
    }
  } else
    e12();
}
function Pa(e12) {
  te.useDeprecatedSynchronousErrorHandling && Ue && (Ue.errorThrown = true, Ue.error = e12);
}
var ze = class extends H {
  constructor(t) {
    super(), this.isStopped = false, t ? (this.destination = t, Ln(t) && t.add(this)) : this.destination = yd;
  }
  static create(t, n, r) {
    return new ht(t, n, r);
  }
  next(t) {
    this.isStopped ? ko(ka(t), this) : this._next(t);
  }
  error(t) {
    this.isStopped ? ko(Oa(t), this) : (this.isStopped = true, this._error(t));
  }
  complete() {
    this.isStopped ? ko(Ra, this) : (this.isStopped = true, this._complete());
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
var gd = Function.prototype.bind;
function Oo(e12, t) {
  return gd.call(e12, t);
}
var Po = class {
  constructor(t) {
    this.partialObserver = t;
  }
  next(t) {
    let { partialObserver: n } = this;
    if (n.next)
      try {
        n.next(t);
      } catch (r) {
        Fn(r);
      }
  }
  error(t) {
    let { partialObserver: n } = this;
    if (n.error)
      try {
        n.error(t);
      } catch (r) {
        Fn(r);
      }
    else
      Fn(t);
  }
  complete() {
    let { partialObserver: t } = this;
    if (t.complete)
      try {
        t.complete();
      } catch (n) {
        Fn(n);
      }
  }
};
var ht = class extends ze {
  constructor(t, n, r) {
    super();
    let o;
    if ($(t) || !t)
      o = { next: t ?? void 0, error: n ?? void 0, complete: r ?? void 0 };
    else {
      let i;
      this && te.useDeprecatedNextContext ? (i = Object.create(t), i.unsubscribe = () => this.unsubscribe(), o = { next: t.next && Oo(t.next, i), error: t.error && Oo(t.error, i), complete: t.complete && Oo(t.complete, i) }) : o = t;
    }
    this.destination = new Po(o);
  }
};
function Fn(e12) {
  te.useDeprecatedSynchronousErrorHandling ? Pa(e12) : Aa(e12);
}
function md(e12) {
  throw e12;
}
function ko(e12, t) {
  let { onStoppedNotification: n } = te;
  n && ft.setTimeout(() => n(e12, t));
}
var yd = { closed: true, next: Ao, error: md, complete: Ao };
var La = typeof Symbol == "function" && Symbol.observable || "@@observable";
function Fa(e12) {
  return e12;
}
function ja(e12) {
  return e12.length === 0 ? Fa : e12.length === 1 ? e12[0] : function(n) {
    return e12.reduce((r, o) => o(r), n);
  };
}
var gt = (() => {
  class e12 {
    constructor(n) {
      n && (this._subscribe = n);
    }
    lift(n) {
      let r = new e12();
      return r.source = this, r.operator = n, r;
    }
    subscribe(n, r, o) {
      let i = Ed(n) ? n : new ht(n, r, o);
      return pt(() => {
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
      return r = Ha(r), new r((o, i) => {
        let s = new ht({ next: (a) => {
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
    [La]() {
      return this;
    }
    pipe(...n) {
      return ja(n)(this);
    }
    toPromise(n) {
      return n = Ha(n), new n((r, o) => {
        let i;
        this.subscribe((s) => i = s, (s) => o(s), () => r(i));
      });
    }
  }
  return e12.create = (t) => new e12(t), e12;
})();
function Ha(e12) {
  var t;
  return (t = e12 ?? te.Promise) !== null && t !== void 0 ? t : Promise;
}
function vd(e12) {
  return e12 && $(e12.next) && $(e12.error) && $(e12.complete);
}
function Ed(e12) {
  return e12 && e12 instanceof ze || vd(e12) && Ln(e12);
}
function Id(e12) {
  return $(e12?.lift);
}
function Va(e12) {
  return (t) => {
    if (Id(t))
      return t.lift(function(n) {
        try {
          return e12(n, this);
        } catch (r) {
          this.error(r);
        }
      });
    throw new TypeError("Unable to lift unknown Observable type");
  };
}
function Ba(e12, t, n, r, o) {
  return new Lo(e12, t, n, r, o);
}
var Lo = class extends ze {
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
var $a = kn((e12) => function() {
  e12(this), this.name = "ObjectUnsubscribedError", this.message = "object unsubscribed";
});
var ye = (() => {
  class e12 extends gt {
    constructor() {
      super(), this.closed = false, this.currentObservers = null, this.observers = [], this.isStopped = false, this.hasError = false, this.thrownError = null;
    }
    lift(n) {
      let r = new jn(this, this);
      return r.operator = n, r;
    }
    _throwIfClosed() {
      if (this.closed)
        throw new $a();
    }
    next(n) {
      pt(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.currentObservers || (this.currentObservers = Array.from(this.observers));
          for (let r of this.currentObservers)
            r.next(n);
        }
      });
    }
    error(n) {
      pt(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.hasError = this.isStopped = true, this.thrownError = n;
          let { observers: r } = this;
          for (; r.length; )
            r.shift().error(n);
        }
      });
    }
    complete() {
      pt(() => {
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
      return r || o ? xo : (this.currentObservers = null, i.push(n), new H(() => {
        this.currentObservers = null, Bt(i, n);
      }));
    }
    _checkFinalizedStatuses(n) {
      let { hasError: r, thrownError: o, isStopped: i } = this;
      r ? n.error(o) : i && n.complete();
    }
    asObservable() {
      let n = new gt();
      return n.source = this, n;
    }
  }
  return e12.create = (t, n) => new jn(t, n), e12;
})();
var jn = class extends ye {
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
    return (r = (n = this.source) === null || n === void 0 ? void 0 : n.subscribe(t)) !== null && r !== void 0 ? r : xo;
  }
};
var $t = class extends ye {
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
function Fo(e12, t) {
  return Va((n, r) => {
    let o = 0;
    n.subscribe(Ba(r, (i) => {
      r.next(e12.call(t, i, o++));
    }));
  });
}
var jo;
function Hn() {
  return jo;
}
function ae(e12) {
  let t = jo;
  return jo = e12, t;
}
var Ua = Symbol("NotFound");
function mt(e12) {
  return e12 === Ua || e12?.name === "\u0275NotFound";
}
var qn = "https://angular.dev/best-practices/security#preventing-cross-site-scripting-xss";
var v = class extends Error {
  code;
  constructor(t, n) {
    super(Zn(t, n)), this.code = t;
  }
};
function Dd(e12) {
  return `NG0${Math.abs(e12)}`;
}
function Zn(e12, t) {
  return `${Dd(e12)}${t ? ": " + t : ""}`;
}
var Re = globalThis;
function C(e12) {
  for (let t in e12)
    if (e12[t] === C)
      return t;
  throw Error("");
}
function Qn(e12) {
  if (typeof e12 == "string")
    return e12;
  if (Array.isArray(e12))
    return `[${e12.map(Qn).join(", ")}]`;
  if (e12 == null)
    return "" + e12;
  let t = e12.overriddenName || e12.name;
  if (t)
    return `${t}`;
  let n = e12.toString();
  if (n == null)
    return "" + n;
  let r = n.indexOf(`
`);
  return r >= 0 ? n.slice(0, r) : n;
}
function Jo(e12, t) {
  return e12 ? t ? `${e12} ${t}` : e12 : t || "";
}
var wd = C({ __forward_ref__: C });
function Yn(e12) {
  return e12.__forward_ref__ = Yn, e12;
}
function W(e12) {
  return Za(e12) ? e12() : e12;
}
function Za(e12) {
  return typeof e12 == "function" && e12.hasOwnProperty(wd) && e12.__forward_ref__ === Yn;
}
function _(e12) {
  return { token: e12.token, providedIn: e12.providedIn || null, factory: e12.factory, value: void 0 };
}
function Kn(e12) {
  return bd(e12, Jn);
}
function bd(e12, t) {
  return e12.hasOwnProperty(t) && e12[t] || null;
}
function Cd(e12) {
  let t = e12?.[Jn] ?? null;
  return t || null;
}
function Vo(e12) {
  return e12 && e12.hasOwnProperty(Bn) ? e12[Bn] : null;
}
var Jn = C({ \u0275prov: C });
var Bn = C({ \u0275inj: C });
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
function Xo(e12) {
  return e12 && !!e12.\u0275providers;
}
var ei = C({ \u0275cmp: C });
var ti = C({ \u0275dir: C });
var ni = C({ \u0275pipe: C });
var Bo = C({ \u0275fac: C });
var Qe = C({ __NG_ELEMENT_ID__: C });
var za = C({ __NG_ENV_ID__: C });
function Ye(e12) {
  return oi(e12, "@Component"), e12[ei] || null;
}
function ri(e12) {
  return oi(e12, "@Directive"), e12[ti] || null;
}
function Qa(e12) {
  return oi(e12, "@Pipe"), e12[ni] || null;
}
function oi(e12, t) {
  if (e12 == null)
    throw new v(-919, false);
}
function ii(e12) {
  return typeof e12 == "string" ? e12 : e12 == null ? "" : String(e12);
}
var Ya = C({ ngErrorCode: C });
var Td = C({ ngErrorMessage: C });
var Md = C({ ngTokenPath: C });
function si(e12, t) {
  return Ka("", -200, t);
}
function Xn(e12, t) {
  throw new v(-201, false);
}
function Ka(e12, t, n) {
  let r = new v(t, e12);
  return r[Ya] = t, r[Td] = e12, n && (r[Md] = n), r;
}
function _d(e12) {
  return e12[Ya];
}
var $o;
function Ja() {
  return $o;
}
function z(e12) {
  let t = $o;
  return $o = e12, t;
}
function ai(e12, t, n) {
  let r = Kn(e12);
  if (r && r.providedIn == "root")
    return r.value === void 0 ? r.value = r.factory() : r.value;
  if (n & 8)
    return null;
  if (t !== void 0)
    return t;
  Xn(e12, "");
}
var Sd = {};
var We = Sd;
var Nd = "__NG_DI_FLAG__";
var Uo = class {
  injector;
  constructor(t) {
    this.injector = t;
  }
  retrieve(t, n) {
    let r = Ge(n) || 0;
    try {
      return this.injector.get(t, r & 8 ? null : We, r);
    } catch (o) {
      if (mt(o))
        return o;
      throw o;
    }
  }
};
function xd(e12, t = 0) {
  let n = Hn();
  if (n === void 0)
    throw new v(-203, false);
  if (n === null)
    return ai(e12, void 0, t);
  {
    let r = Ad(t), o = n.retrieve(e12, r);
    if (mt(o)) {
      if (r.optional)
        return null;
      throw o;
    }
    return o;
  }
}
function w(e12, t = 0) {
  return (Ja() || xd)(W(e12), t);
}
function E(e12, t) {
  return w(e12, Ge(t));
}
function Ge(e12) {
  return typeof e12 > "u" || typeof e12 == "number" ? e12 : 0 | (e12.optional && 8) | (e12.host && 1) | (e12.self && 2) | (e12.skipSelf && 4);
}
function Ad(e12) {
  return { optional: !!(e12 & 8), host: !!(e12 & 1), self: !!(e12 & 2), skipSelf: !!(e12 & 4) };
}
function zo(e12) {
  let t = [];
  for (let n = 0; n < e12.length; n++) {
    let r = W(e12[n]);
    if (Array.isArray(r)) {
      if (r.length === 0)
        throw new v(900, false);
      let o, i = 0;
      for (let s = 0; s < r.length; s++) {
        let a = r[s], c = Rd(a);
        typeof c == "number" ? c === -1 ? o = a.token : i |= c : o = a;
      }
      t.push(w(o, i));
    } else
      t.push(w(r));
  }
  return t;
}
function Rd(e12) {
  return e12[Nd];
}
function vt(e12, t) {
  let n = e12.hasOwnProperty(Bo);
  return n ? e12[Bo] : null;
}
function Xa(e12, t, n) {
  if (e12.length !== t.length)
    return false;
  for (let r = 0; r < e12.length; r++) {
    let o = e12[r], i = t[r];
    if (n && (o = n(o), i = n(i)), i !== o)
      return false;
  }
  return true;
}
function ec(e12) {
  return e12.flat(Number.POSITIVE_INFINITY);
}
function er(e12, t) {
  e12.forEach((n) => Array.isArray(n) ? er(n, t) : t(n));
}
function ci(e12, t, n) {
  t >= e12.length ? e12.push(n) : e12.splice(t, 0, n);
}
function Zt(e12, t) {
  return t >= e12.length - 1 ? e12.pop() : e12.splice(t, 1)[0];
}
function tc(e12, t, n, r) {
  let o = e12.length;
  if (o == t)
    e12.push(n, r);
  else if (o === 1)
    e12.push(r, e12[0]), e12[0] = n;
  else {
    for (o--, e12.push(e12[o - 1], e12[o]); o > t; ) {
      let i = o - 2;
      e12[o] = e12[i], o--;
    }
    e12[t] = n, e12[t + 1] = r;
  }
}
function nc(e12, t, n) {
  let r = Et(e12, t);
  return r >= 0 ? e12[r | 1] = n : (r = ~r, tc(e12, r, t, n)), r;
}
function tr(e12, t) {
  let n = Et(e12, t);
  if (n >= 0)
    return e12[n | 1];
}
function Et(e12, t) {
  return Od(e12, t, 1);
}
function Od(e12, t, n) {
  let r = 0, o = e12.length >> n;
  for (; o !== r; ) {
    let i = r + (o - r >> 1), s = e12[i << n];
    if (t === s)
      return i << n;
    s > t ? o = i : r = i + 1;
  }
  return ~(o << n);
}
var Ke = {};
var Ne = [];
var Je = new D("");
var li = new D("", -1);
var ui = new D("");
var zt = class {
  get(t, n = We) {
    if (n === We) {
      let o = Ka("", -201);
      throw o.name = "\u0275NotFound", o;
    }
    return n;
  }
};
function Qt(e12) {
  return { \u0275providers: e12 };
}
function rc(e12) {
  return Qt([{ provide: Je, multi: true, useValue: e12 }]);
}
function oc(...e12) {
  return { \u0275providers: di(true, e12), \u0275fromNgModule: true };
}
function di(e12, ...t) {
  let n = [], r = /* @__PURE__ */ new Set(), o, i = (s) => {
    n.push(s);
  };
  return er(t, (s) => {
    let a = s;
    $n(a, i, [], r) && (o ||= [], o.push(a));
  }), o !== void 0 && ic(o, i), n;
}
function ic(e12, t) {
  for (let n = 0; n < e12.length; n++) {
    let { ngModule: r, providers: o } = e12[n];
    fi(o, (i) => {
      t(i, r);
    });
  }
}
function $n(e12, t, n, r) {
  if (e12 = W(e12), !e12)
    return false;
  let o = null, i = Vo(e12), s = !i && Ye(e12);
  if (!i && !s) {
    let c = e12.ngModule;
    if (i = Vo(c), i)
      o = c;
    else
      return false;
  } else {
    if (s && !s.standalone)
      return false;
    o = e12;
  }
  let a = r.has(o);
  if (s) {
    if (a)
      return false;
    if (r.add(o), s.dependencies) {
      let c = typeof s.dependencies == "function" ? s.dependencies() : s.dependencies;
      for (let l of c)
        $n(l, t, n, r);
    }
  } else if (i) {
    if (i.imports != null && !a) {
      r.add(o);
      let l;
      er(i.imports, (u) => {
        $n(u, t, n, r) && (l ||= [], l.push(u));
      }), l !== void 0 && ic(l, t);
    }
    if (!a) {
      let l = vt(o) || (() => new o());
      t({ provide: o, useFactory: l, deps: Ne }, o), t({ provide: ui, useValue: o, multi: true }, o), t({ provide: Je, useValue: () => w(o), multi: true }, o);
    }
    let c = i.providers;
    if (c != null && !a) {
      let l = e12;
      fi(c, (u) => {
        t(u, l);
      });
    }
  } else
    return false;
  return o !== e12 && e12.providers !== void 0;
}
function fi(e12, t) {
  for (let n of e12)
    Xo(n) && (n = n.\u0275providers), Array.isArray(n) ? fi(n, t) : t(n);
}
var kd = C({ provide: String, useValue: C });
function sc(e12) {
  return e12 !== null && typeof e12 == "object" && kd in e12;
}
function Pd(e12) {
  return !!(e12 && e12.useExisting);
}
function Ld(e12) {
  return !!(e12 && e12.useFactory);
}
function Un(e12) {
  return typeof e12 == "function";
}
var Yt = new D("");
var Vn = {};
var Wa = {};
var Ho;
function Kt() {
  return Ho === void 0 && (Ho = new zt()), Ho;
}
var Q = class {
};
var qe = class extends Q {
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
    super(), this.parent = n, this.source = r, this.scopes = o, Go(t, (s) => this.processProvider(s)), this.records.set(li, yt(void 0, this)), o.has("environment") && this.records.set(Q, yt(void 0, this));
    let i = this.records.get(Yt);
    i != null && typeof i.value == "string" && this.scopes.add(i.value), this.injectorDefTypes = new Set(this.get(ui, Ne, { self: true }));
  }
  retrieve(t, n) {
    let r = Ge(n) || 0;
    try {
      return this.get(t, We, r);
    } catch (o) {
      if (mt(o))
        return o;
      throw o;
    }
  }
  destroy() {
    Ut(this), this._destroyed = true;
    let t = g(null);
    try {
      for (let r of this._ngOnDestroyHooks)
        r.ngOnDestroy();
      let n = this._onDestroyHooks;
      this._onDestroyHooks = [];
      for (let r of n)
        r();
    } finally {
      this.records.clear(), this._ngOnDestroyHooks.clear(), this.injectorDefTypes.clear(), g(t);
    }
  }
  onDestroy(t) {
    return Ut(this), this._onDestroyHooks.push(t), () => this.removeOnDestroy(t);
  }
  runInContext(t) {
    Ut(this);
    let n = ae(this), r = z(void 0), o;
    try {
      return t();
    } finally {
      ae(n), z(r);
    }
  }
  get(t, n = We, r) {
    if (Ut(this), t.hasOwnProperty(za))
      return t[za](this);
    let o = Ge(r), i, s = ae(this), a = z(void 0);
    try {
      if (!(o & 4)) {
        let l = this.records.get(t);
        if (l === void 0) {
          let u = Bd(t) && Kn(t);
          u && this.injectableDefInScope(u) ? l = yt(Wo(t), Vn) : l = null, this.records.set(t, l);
        }
        if (l != null)
          return this.hydrate(t, l, o);
      }
      let c = o & 2 ? Kt() : this.parent;
      return n = o & 8 && n === We ? null : n, c.get(t, n);
    } catch (c) {
      let l = _d(c);
      throw l === -200 || l === -201 ? new v(l, null) : c;
    } finally {
      z(a), ae(s);
    }
  }
  resolveInjectorInitializers() {
    let t = g(null), n = ae(this), r = z(void 0), o;
    try {
      let i = this.get(Je, Ne, { self: true });
      for (let s of i)
        s();
    } finally {
      ae(n), z(r), g(t);
    }
  }
  toString() {
    return "R3Injector[...]";
  }
  processProvider(t) {
    t = W(t);
    let n = Un(t) ? t : W(t && t.provide), r = jd(t);
    if (!Un(t) && t.multi === true) {
      let o = this.records.get(n);
      o || (o = yt(void 0, Vn, true), o.factory = () => zo(o.multi), this.records.set(n, o)), n = t, o.multi.push(t);
    }
    this.records.set(n, r);
  }
  hydrate(t, n, r) {
    let o = g(null);
    try {
      if (n.value === Wa)
        throw si("");
      return n.value === Vn && (n.value = Wa, n.value = n.factory(void 0, r)), typeof n.value == "object" && n.value && Vd(n.value) && this._ngOnDestroyHooks.add(n.value), n.value;
    } finally {
      g(o);
    }
  }
  injectableDefInScope(t) {
    if (!t.providedIn)
      return false;
    let n = W(t.providedIn);
    return typeof n == "string" ? n === "any" || this.scopes.has(n) : this.injectorDefTypes.has(n);
  }
  removeOnDestroy(t) {
    let n = this._onDestroyHooks.indexOf(t);
    n !== -1 && this._onDestroyHooks.splice(n, 1);
  }
};
function Wo(e12) {
  let t = Kn(e12), n = t !== null ? t.factory : vt(e12);
  if (n !== null)
    return n;
  if (e12 instanceof D)
    throw new v(-204, false);
  if (e12 instanceof Function)
    return Fd(e12);
  throw new v(-204, false);
}
function Fd(e12) {
  if (e12.length > 0)
    throw new v(-204, false);
  let n = Cd(e12);
  return n !== null ? () => n.factory(e12) : () => new e12();
}
function jd(e12) {
  if (sc(e12))
    return yt(void 0, e12.useValue);
  {
    let t = ac(e12);
    return yt(t, Vn);
  }
}
function ac(e12, t, n) {
  let r;
  if (Un(e12)) {
    let o = W(e12);
    return vt(o) || Wo(o);
  } else if (sc(e12))
    r = () => W(e12.useValue);
  else if (Ld(e12))
    r = () => e12.useFactory(...zo(e12.deps || []));
  else if (Pd(e12))
    r = (o, i) => w(W(e12.useExisting), i !== void 0 && i & 8 ? 8 : void 0);
  else {
    let o = W(e12 && (e12.useClass || e12.provide));
    if (Hd(e12))
      r = () => new o(...zo(e12.deps));
    else
      return vt(o) || Wo(o);
  }
  return r;
}
function Ut(e12) {
  if (e12.destroyed)
    throw new v(-205, false);
}
function yt(e12, t, n = false) {
  return { factory: e12, value: t, multi: n ? [] : void 0 };
}
function Hd(e12) {
  return !!e12.deps;
}
function Vd(e12) {
  return e12 !== null && typeof e12 == "object" && typeof e12.ngOnDestroy == "function";
}
function Bd(e12) {
  return typeof e12 == "function" || typeof e12 == "object" && e12.ngMetadataName === "InjectionToken";
}
function Go(e12, t) {
  for (let n of e12)
    Array.isArray(n) ? Go(n, t) : n && Xo(n) ? Go(n.\u0275providers, t) : t(n);
}
function nr(e12, t) {
  let n;
  e12 instanceof qe ? (Ut(e12), n = e12) : n = new Uo(e12);
  let r, o = ae(n), i = z(void 0);
  try {
    return t();
  } finally {
    ae(o), z(i);
  }
}
function cc() {
  return Ja() !== void 0 || Hn() != null;
}
var ne = 0;
var m = 1;
var y = 2;
var R = 3;
var K = 4;
var J = 5;
var It = 6;
var Dt = 7;
var x = 8;
var De = 9;
var le = 10;
var O = 11;
var wt = 12;
var pi = 13;
var Xe = 14;
var X = 15;
var Oe = 16;
var et = 17;
var ue = 18;
var we = 19;
var hi = 20;
var Ee = 21;
var rr = 22;
var xe = 23;
var G = 24;
var or = 25;
var ke = 26;
var F = 27;
var lc = 1;
var gi = 6;
var Pe = 7;
var Jt = 8;
var tt = 9;
var S = 10;
function Le(e12) {
  return Array.isArray(e12) && typeof e12[lc] == "object";
}
function re(e12) {
  return Array.isArray(e12) && e12[lc] === true;
}
function mi(e12) {
  return (e12.flags & 4) !== 0;
}
function bt(e12) {
  return e12.componentOffset > -1;
}
function yi(e12) {
  return (e12.flags & 1) === 1;
}
function Ct(e12) {
  return !!e12.template;
}
function Tt(e12) {
  return (e12[y] & 512) !== 0;
}
function nt(e12) {
  return (e12[y] & 256) === 256;
}
var uc = "svg";
var dc = "math";
function ee(e12) {
  for (; Array.isArray(e12); )
    e12 = e12[ne];
  return e12;
}
function vi(e12, t) {
  return ee(t[e12]);
}
function de(e12, t) {
  return ee(t[e12.index]);
}
function ir(e12, t) {
  return e12.data[t];
}
function be(e12, t) {
  let n = t[e12];
  return Le(n) ? n : n[ne];
}
function fc(e12) {
  return (e12[y] & 4) === 4;
}
function sr(e12) {
  return (e12[y] & 128) === 128;
}
function pc(e12) {
  return re(e12[R]);
}
function fe(e12, t) {
  return t == null ? null : e12[t];
}
function Ei(e12) {
  e12[et] = 0;
}
function Ii(e12) {
  e12[y] & 1024 || (e12[y] |= 1024, sr(e12) && Mt(e12));
}
function hc(e12, t) {
  for (; e12 > 0; )
    t = t[Xe], e12--;
  return t;
}
function Xt(e12) {
  return !!(e12[y] & 9216 || e12[G]?.dirty);
}
function ar(e12) {
  e12[le].changeDetectionScheduler?.notify(8), e12[y] & 64 && (e12[y] |= 1024), Xt(e12) && Mt(e12);
}
function Mt(e12) {
  e12[le].changeDetectionScheduler?.notify(0);
  let t = Ae(e12);
  for (; t !== null && !(t[y] & 8192 || (t[y] |= 8192, !sr(t))); )
    t = Ae(t);
}
function Di(e12, t) {
  if (nt(e12))
    throw new v(911, false);
  e12[Ee] === null && (e12[Ee] = []), e12[Ee].push(t);
}
function gc(e12, t) {
  if (e12[Ee] === null)
    return;
  let n = e12[Ee].indexOf(t);
  n !== -1 && e12[Ee].splice(n, 1);
}
function Ae(e12) {
  let t = e12[R];
  return re(t) ? t[R] : t;
}
function wi(e12) {
  return e12[Dt] ??= [];
}
function bi(e12) {
  return e12.cleanup ??= [];
}
function mc(e12, t, n, r) {
  let o = wi(t);
  o.push(n), e12.firstCreatePass && bi(e12).push(r, o.length - 1);
}
var I = { lFrame: Rc(null), bindingsEnabled: true, skipHydrationRootTNode: null };
var qo = false;
function yc() {
  return I.lFrame.elementDepthCount;
}
function vc() {
  I.lFrame.elementDepthCount++;
}
function Ec() {
  I.lFrame.elementDepthCount--;
}
function Ic() {
  return I.skipHydrationRootTNode !== null;
}
function Dc(e12) {
  return I.skipHydrationRootTNode === e12;
}
function wc() {
  I.skipHydrationRootTNode = null;
}
function M() {
  return I.lFrame.lView;
}
function oe() {
  return I.lFrame.tView;
}
function pe() {
  let e12 = Ci();
  for (; e12 !== null && e12.type === 64; )
    e12 = e12.parent;
  return e12;
}
function Ci() {
  return I.lFrame.currentTNode;
}
function bc() {
  let e12 = I.lFrame, t = e12.currentTNode;
  return e12.isParent ? t : t.parent;
}
function _t(e12, t) {
  let n = I.lFrame;
  n.currentTNode = e12, n.isParent = t;
}
function Ti() {
  return I.lFrame.isParent;
}
function Cc() {
  I.lFrame.isParent = false;
}
function Mi() {
  return qo;
}
function Wt(e12) {
  let t = qo;
  return qo = e12, t;
}
function Tc(e12) {
  return I.lFrame.bindingIndex = e12;
}
function en() {
  return I.lFrame.bindingIndex++;
}
function Mc(e12) {
  let t = I.lFrame, n = t.bindingIndex;
  return t.bindingIndex = t.bindingIndex + e12, n;
}
function _c() {
  return I.lFrame.inI18n;
}
function Sc(e12, t) {
  let n = I.lFrame;
  n.bindingIndex = n.bindingRootIndex = e12, cr(t);
}
function Nc() {
  return I.lFrame.currentDirectiveIndex;
}
function cr(e12) {
  I.lFrame.currentDirectiveIndex = e12;
}
function xc(e12) {
  let t = I.lFrame.currentDirectiveIndex;
  return t === -1 ? null : e12[t];
}
function _i() {
  return I.lFrame.currentQueryIndex;
}
function lr(e12) {
  I.lFrame.currentQueryIndex = e12;
}
function $d(e12) {
  let t = e12[m];
  return t.type === 2 ? t.declTNode : t.type === 1 ? e12[J] : null;
}
function Si(e12, t, n) {
  if (n & 4) {
    let o = t, i = e12;
    for (; o = o.parent, o === null && !(n & 1); )
      if (o = $d(i), o === null || (i = i[Xe], o.type & 10))
        break;
    if (o === null)
      return false;
    t = o, e12 = i;
  }
  let r = I.lFrame = Ac();
  return r.currentTNode = t, r.lView = e12, true;
}
function ur(e12) {
  let t = Ac(), n = e12[m];
  I.lFrame = t, t.currentTNode = n.firstChild, t.lView = e12, t.tView = n, t.contextLView = e12, t.bindingIndex = n.bindingStartIndex, t.inI18n = false;
}
function Ac() {
  let e12 = I.lFrame, t = e12 === null ? null : e12.child;
  return t === null ? Rc(e12) : t;
}
function Rc(e12) {
  let t = { currentTNode: null, isParent: true, lView: null, tView: null, selectedIndex: -1, contextLView: null, elementDepthCount: 0, currentNamespace: null, currentDirectiveIndex: -1, bindingRootIndex: -1, bindingIndex: -1, currentQueryIndex: 0, parent: e12, child: null, inI18n: false };
  return e12 !== null && (e12.child = t), t;
}
function Oc() {
  let e12 = I.lFrame;
  return I.lFrame = e12.parent, e12.currentTNode = null, e12.lView = null, e12;
}
var Ni = Oc;
function dr() {
  let e12 = Oc();
  e12.isParent = true, e12.tView = null, e12.selectedIndex = -1, e12.contextLView = null, e12.elementDepthCount = 0, e12.currentDirectiveIndex = -1, e12.currentNamespace = null, e12.bindingRootIndex = -1, e12.bindingIndex = -1, e12.currentQueryIndex = 0;
}
function kc(e12) {
  return (I.lFrame.contextLView = hc(e12, I.lFrame.contextLView))[x];
}
function Fe() {
  return I.lFrame.selectedIndex;
}
function je(e12) {
  I.lFrame.selectedIndex = e12;
}
function Pc() {
  let e12 = I.lFrame;
  return ir(e12.tView, e12.selectedIndex);
}
function Lc() {
  return I.lFrame.currentNamespace;
}
var Fc = true;
function fr() {
  return Fc;
}
function pr(e12) {
  Fc = e12;
}
function Zo(e12, t = null, n = null, r) {
  let o = jc(e12, t, n, r);
  return o.resolveInjectorInitializers(), o;
}
function jc(e12, t = null, n = null, r, o = /* @__PURE__ */ new Set()) {
  let i = [n || Ne, oc(e12)], s;
  return new qe(i, t || Kt(), s || null, o);
}
var ce = class e2 {
  static THROW_IF_NOT_FOUND = We;
  static NULL = new zt();
  static create(t, n) {
    if (Array.isArray(t))
      return Zo({ name: "" }, n, t, "");
    {
      let r = t.name ?? "";
      return Zo({ name: r }, t.parent, t.providers, r);
    }
  }
  static \u0275prov = _({ token: e2, providedIn: "any", factory: () => w(li) });
  static __NG_ELEMENT_ID__ = -1;
};
var U = new D("");
var St = /* @__PURE__ */ (() => {
  class e12 {
    static __NG_ELEMENT_ID__ = Ud;
    static __NG_ENV_ID__ = (n) => n;
  }
  return e12;
})();
var zn = class extends St {
  _lView;
  constructor(t) {
    super(), this._lView = t;
  }
  get destroyed() {
    return nt(this._lView);
  }
  onDestroy(t) {
    let n = this._lView;
    return Di(n, t), () => gc(n, t);
  }
};
function Ud() {
  return new zn(M());
}
var Hc = false;
var Vc = new D("");
var Nt = (() => {
  class e12 {
    taskId = 0;
    pendingTasks = /* @__PURE__ */ new Set();
    destroyed = false;
    pendingTask = new $t(false);
    debugTaskTracker = E(Vc, { optional: true });
    get hasPendingTasks() {
      return this.destroyed ? false : this.pendingTask.value;
    }
    get hasPendingTasksObservable() {
      return this.destroyed ? new gt((n) => {
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
    static \u0275prov = _({ token: e12, providedIn: "root", factory: () => new e12() });
  }
  return e12;
})();
var Qo = class extends ye {
  __isAsync;
  destroyRef = void 0;
  pendingTasks = void 0;
  constructor(t = false) {
    super(), this.__isAsync = t, cc() && (this.destroyRef = E(St, { optional: true }) ?? void 0, this.pendingTasks = E(Nt, { optional: true }) ?? void 0);
  }
  emit(t) {
    let n = g(null);
    try {
      super.next(t);
    } finally {
      g(n);
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
    return t instanceof H && t.add(a), a;
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
var ve = Qo;
function Wn(...e12) {
}
function xi(e12) {
  let t, n;
  function r() {
    e12 = Wn;
    try {
      n !== void 0 && typeof cancelAnimationFrame == "function" && cancelAnimationFrame(n), t !== void 0 && clearTimeout(t);
    } catch {
    }
  }
  return t = setTimeout(() => {
    e12(), r();
  }), typeof requestAnimationFrame == "function" && (n = requestAnimationFrame(() => {
    e12(), r();
  })), () => r();
}
function Bc(e12) {
  return queueMicrotask(() => e12()), () => {
    e12 = Wn;
  };
}
var Ai = "isAngularZone";
var Gt = Ai + "_ID";
var zd = 0;
var Y = class e3 {
  hasPendingMacrotasks = false;
  hasPendingMicrotasks = false;
  isStable = true;
  onUnstable = new ve(false);
  onMicrotaskEmpty = new ve(false);
  onStable = new ve(false);
  onError = new ve(false);
  constructor(t) {
    let { enableLongStackTrace: n = false, shouldCoalesceEventChangeDetection: r = false, shouldCoalesceRunChangeDetection: o = false, scheduleInRootZone: i = Hc } = t;
    if (typeof Zone > "u")
      throw new v(908, false);
    Zone.assertZonePatched();
    let s = this;
    s._nesting = 0, s._outer = s._inner = Zone.current, Zone.TaskTrackingZoneSpec && (s._inner = s._inner.fork(new Zone.TaskTrackingZoneSpec())), n && Zone.longStackTraceZoneSpec && (s._inner = s._inner.fork(Zone.longStackTraceZoneSpec)), s.shouldCoalesceEventChangeDetection = !o && r, s.shouldCoalesceRunChangeDetection = o, s.callbackScheduled = false, s.scheduleInRootZone = i, qd(s);
  }
  static isInAngularZone() {
    return typeof Zone < "u" && Zone.current.get(Ai) === true;
  }
  static assertInAngularZone() {
    if (!e3.isInAngularZone())
      throw new v(909, false);
  }
  static assertNotInAngularZone() {
    if (e3.isInAngularZone())
      throw new v(909, false);
  }
  run(t, n, r) {
    return this._inner.run(t, n, r);
  }
  runTask(t, n, r, o) {
    let i = this._inner, s = i.scheduleEventTask("NgZoneEvent: " + o, t, Wd, Wn, Wn);
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
var Wd = {};
function Ri(e12) {
  if (e12._nesting == 0 && !e12.hasPendingMicrotasks && !e12.isStable)
    try {
      e12._nesting++, e12.onMicrotaskEmpty.emit(null);
    } finally {
      if (e12._nesting--, !e12.hasPendingMicrotasks)
        try {
          e12.runOutsideAngular(() => e12.onStable.emit(null));
        } finally {
          e12.isStable = true;
        }
    }
}
function Gd(e12) {
  if (e12.isCheckStableRunning || e12.callbackScheduled)
    return;
  e12.callbackScheduled = true;
  function t() {
    xi(() => {
      e12.callbackScheduled = false, Yo(e12), e12.isCheckStableRunning = true, Ri(e12), e12.isCheckStableRunning = false;
    });
  }
  e12.scheduleInRootZone ? Zone.root.run(() => {
    t();
  }) : e12._outer.run(() => {
    t();
  }), Yo(e12);
}
function qd(e12) {
  let t = () => {
    Gd(e12);
  }, n = zd++;
  e12._inner = e12._inner.fork({ name: "angular", properties: { [Ai]: true, [Gt]: n, [Gt + n]: true }, onInvokeTask: (r, o, i, s, a, c) => {
    if (Zd(c))
      return r.invokeTask(i, s, a, c);
    try {
      return Ga(e12), r.invokeTask(i, s, a, c);
    } finally {
      (e12.shouldCoalesceEventChangeDetection && s.type === "eventTask" || e12.shouldCoalesceRunChangeDetection) && t(), qa(e12);
    }
  }, onInvoke: (r, o, i, s, a, c, l) => {
    try {
      return Ga(e12), r.invoke(i, s, a, c, l);
    } finally {
      e12.shouldCoalesceRunChangeDetection && !e12.callbackScheduled && !Qd(c) && t(), qa(e12);
    }
  }, onHasTask: (r, o, i, s) => {
    r.hasTask(i, s), o === i && (s.change == "microTask" ? (e12._hasPendingMicrotasks = s.microTask, Yo(e12), Ri(e12)) : s.change == "macroTask" && (e12.hasPendingMacrotasks = s.macroTask));
  }, onHandleError: (r, o, i, s) => (r.handleError(i, s), e12.runOutsideAngular(() => e12.onError.emit(s)), false) });
}
function Yo(e12) {
  e12._hasPendingMicrotasks || (e12.shouldCoalesceEventChangeDetection || e12.shouldCoalesceRunChangeDetection) && e12.callbackScheduled === true ? e12.hasPendingMicrotasks = true : e12.hasPendingMicrotasks = false;
}
function Ga(e12) {
  e12._nesting++, e12.isStable && (e12.isStable = false, e12.onUnstable.emit(null));
}
function qa(e12) {
  e12._nesting--, Ri(e12);
}
var qt = class {
  hasPendingMicrotasks = false;
  hasPendingMacrotasks = false;
  isStable = true;
  onUnstable = new ve();
  onMicrotaskEmpty = new ve();
  onStable = new ve();
  onError = new ve();
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
function Zd(e12) {
  return $c(e12, "__ignore_ng_zone__");
}
function Qd(e12) {
  return $c(e12, "__scheduler_tick__");
}
function $c(e12, t) {
  return !Array.isArray(e12) || e12.length !== 1 ? false : e12[0]?.data?.[t] === true;
}
var Ie = class {
  _console = console;
  handleError(t) {
    this._console.error("ERROR", t);
  }
};
var rt = new D("", { factory: () => {
  let e12 = E(Y), t = E(Q), n;
  return (r) => {
    e12.runOutsideAngular(() => {
      t.destroyed && !n ? setTimeout(() => {
        throw r;
      }) : (n ??= t.get(Ie), n.handleError(r));
    });
  };
} });
var Uc = { provide: Je, useValue: () => {
  let e12 = E(Ie, { optional: true });
}, multi: true };
var Yd = new D("", { factory: () => {
  let e12 = E(U).defaultView;
  if (!e12)
    return;
  let t = E(rt), n = (i) => {
    t(i.reason), i.preventDefault();
  }, r = (i) => {
    i.error ? t(i.error) : t(new Error(i.message, { cause: i })), i.preventDefault();
  }, o = () => {
    e12.addEventListener("unhandledrejection", n), e12.addEventListener("error", r);
  };
  typeof Zone < "u" ? Zone.root.run(o) : o(), E(St).onDestroy(() => {
    e12.removeEventListener("error", r), e12.removeEventListener("unhandledrejection", n);
  });
} });
function Oi() {
  return Qt([rc(() => {
    E(Yd);
  })]);
}
function q(e12, t) {
  let [n, r, o] = Mo(e12, t?.equal), i = n, s = i[Z];
  return i.set = r, i.update = o, i.asReadonly = zc.bind(i), i;
}
function zc() {
  let e12 = this[Z];
  if (e12.readonlyFn === void 0) {
    let t = () => this();
    t[Z] = e12, e12.readonlyFn = t;
  }
  return e12.readonlyFn;
}
var hr = /* @__PURE__ */ (() => {
  class e12 {
    view;
    node;
    constructor(n, r) {
      this.view = n, this.node = r;
    }
    static __NG_ELEMENT_ID__ = Kd;
  }
  return e12;
})();
function Kd() {
  return new hr(M(), pe());
}
var Ze = class {
};
var tn = new D("", { factory: () => true });
var ki = new D("");
var gr = (() => {
  class e12 {
    static \u0275prov = _({ token: e12, providedIn: "root", factory: () => new Ko() });
  }
  return e12;
})();
var Ko = class {
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
var Gn = class {
  [Z];
  constructor(t) {
    this[Z] = t;
  }
  destroy() {
    this[Z].destroy();
  }
};
function Pi(e12, t) {
  let n = t?.injector ?? E(ce), r = t?.manualCleanup !== true ? n.get(St) : null, o, i = n.get(hr, null, { optional: true }), s = n.get(Ze);
  return i !== null ? (o = ef(i.view, s, e12), r instanceof zn && r._lView === i.view && (r = null)) : o = tf(e12, n.get(gr), s), o.injector = n, r !== null && (o.onDestroyFns = [r.onDestroy(() => o.destroy())]), new Gn(o);
}
var Wc = A(N({}, So), { cleanupFns: void 0, zone: null, onDestroyFns: null, run() {
  let e12 = Wt(false);
  try {
    No(this);
  } finally {
    Wt(e12);
  }
}, cleanup() {
  if (!this.cleanupFns?.length)
    return;
  let e12 = g(null);
  try {
    for (; this.cleanupFns.length; )
      this.cleanupFns.pop()();
  } finally {
    this.cleanupFns = [], g(e12);
  }
} });
var Jd = A(N({}, Wc), { consumerMarkedDirty() {
  this.scheduler.schedule(this), this.notifier.notify(12);
}, destroy() {
  if (ut(this), this.onDestroyFns !== null)
    for (let e12 of this.onDestroyFns)
      e12();
  this.cleanup(), this.scheduler.remove(this);
} });
var Xd = A(N({}, Wc), { consumerMarkedDirty() {
  this.view[y] |= 8192, Mt(this.view), this.notifier.notify(13);
}, destroy() {
  if (ut(this), this.onDestroyFns !== null)
    for (let e12 of this.onDestroyFns)
      e12();
  this.cleanup(), this.view[xe]?.delete(this);
} });
function ef(e12, t, n) {
  let r = Object.create(Xd);
  return r.view = e12, r.zone = typeof Zone < "u" ? Zone.current : null, r.notifier = t, r.fn = Gc(r, n), e12[xe] ??= /* @__PURE__ */ new Set(), e12[xe].add(r), r.consumerMarkedDirty(r), r;
}
function tf(e12, t, n) {
  let r = Object.create(Jd);
  return r.fn = Gc(r, e12), r.scheduler = t, r.notifier = n, r.zone = typeof Zone < "u" ? Zone.current : null, r.scheduler.add(r), r.notifier.notify(12), r;
}
function Gc(e12, t) {
  return () => {
    t((n) => (e12.cleanupFns ??= []).push(n));
  };
}
function bl(e12) {
  return { toString: e12 }.toString();
}
function yf(e12) {
  return typeof e12 == "function";
}
function Cl(e12, t, n, r) {
  t !== null ? t.applyValueToInputSignal(t, r) : e12[n] = r;
}
var Cr = class {
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
function vf(e12) {
  return e12.type.prototype.ngOnChanges && (e12.setInput = If), Ef;
}
function Ef() {
  let e12 = Ml(this), t = e12?.current;
  if (t) {
    let n = e12.previous;
    if (n === Ke)
      e12.previous = t;
    else
      for (let r in t)
        n[r] = t[r];
    e12.current = null, this.ngOnChanges(t);
  }
}
function If(e12, t, n, r, o) {
  let i = this.declaredInputs[r], s = Ml(e12) || Df(e12, { previous: Ke, current: null }), a = s.current || (s.current = {}), c = s.previous, l = c[i];
  a[i] = new Cr(l && l.currentValue, n, c === Ke), Cl(e12, t, o, n);
}
var Tl = "__ngSimpleChanges__";
function Ml(e12) {
  return e12[Tl] || null;
}
function Df(e12, t) {
  return e12[Tl] = t;
}
var qc = [];
var T = function(e12, t = null, n) {
  for (let r = 0; r < qc.length; r++) {
    let o = qc[r];
    o(e12, t, n);
  }
};
var b = function(e12) {
  return e12[e12.TemplateCreateStart = 0] = "TemplateCreateStart", e12[e12.TemplateCreateEnd = 1] = "TemplateCreateEnd", e12[e12.TemplateUpdateStart = 2] = "TemplateUpdateStart", e12[e12.TemplateUpdateEnd = 3] = "TemplateUpdateEnd", e12[e12.LifecycleHookStart = 4] = "LifecycleHookStart", e12[e12.LifecycleHookEnd = 5] = "LifecycleHookEnd", e12[e12.OutputStart = 6] = "OutputStart", e12[e12.OutputEnd = 7] = "OutputEnd", e12[e12.BootstrapApplicationStart = 8] = "BootstrapApplicationStart", e12[e12.BootstrapApplicationEnd = 9] = "BootstrapApplicationEnd", e12[e12.BootstrapComponentStart = 10] = "BootstrapComponentStart", e12[e12.BootstrapComponentEnd = 11] = "BootstrapComponentEnd", e12[e12.ChangeDetectionStart = 12] = "ChangeDetectionStart", e12[e12.ChangeDetectionEnd = 13] = "ChangeDetectionEnd", e12[e12.ChangeDetectionSyncStart = 14] = "ChangeDetectionSyncStart", e12[e12.ChangeDetectionSyncEnd = 15] = "ChangeDetectionSyncEnd", e12[e12.AfterRenderHooksStart = 16] = "AfterRenderHooksStart", e12[e12.AfterRenderHooksEnd = 17] = "AfterRenderHooksEnd", e12[e12.ComponentStart = 18] = "ComponentStart", e12[e12.ComponentEnd = 19] = "ComponentEnd", e12[e12.DeferBlockStateStart = 20] = "DeferBlockStateStart", e12[e12.DeferBlockStateEnd = 21] = "DeferBlockStateEnd", e12[e12.DynamicComponentStart = 22] = "DynamicComponentStart", e12[e12.DynamicComponentEnd = 23] = "DynamicComponentEnd", e12[e12.HostBindingsUpdateStart = 24] = "HostBindingsUpdateStart", e12[e12.HostBindingsUpdateEnd = 25] = "HostBindingsUpdateEnd", e12;
}(b || {});
function wf(e12, t, n) {
  let { ngOnChanges: r, ngOnInit: o, ngDoCheck: i } = t.type.prototype;
  if (r) {
    let s = vf(t);
    (n.preOrderHooks ??= []).push(e12, s), (n.preOrderCheckHooks ??= []).push(e12, s);
  }
  o && (n.preOrderHooks ??= []).push(0 - e12, o), i && ((n.preOrderHooks ??= []).push(e12, i), (n.preOrderCheckHooks ??= []).push(e12, i));
}
function bf(e12, t) {
  for (let n = t.directiveStart, r = t.directiveEnd; n < r; n++) {
    let i = e12.data[n].type.prototype, { ngAfterContentInit: s, ngAfterContentChecked: a, ngAfterViewInit: c, ngAfterViewChecked: l, ngOnDestroy: u } = i;
    s && (e12.contentHooks ??= []).push(-n, s), a && ((e12.contentHooks ??= []).push(n, a), (e12.contentCheckHooks ??= []).push(n, a)), c && (e12.viewHooks ??= []).push(-n, c), l && ((e12.viewHooks ??= []).push(n, l), (e12.viewCheckHooks ??= []).push(n, l)), u != null && (e12.destroyHooks ??= []).push(n, u);
  }
}
function Ir(e12, t, n) {
  _l(e12, t, 3, n);
}
function Dr(e12, t, n, r) {
  (e12[y] & 3) === n && _l(e12, t, n, r);
}
function Li(e12, t) {
  let n = e12[y];
  (n & 3) === t && (n &= 16383, n += 1, e12[y] = n);
}
function _l(e12, t, n, r) {
  let o = r !== void 0 ? e12[et] & 65535 : 0, i = r ?? -1, s = t.length - 1, a = 0;
  for (let c = o; c < s; c++)
    if (typeof t[c + 1] == "number") {
      if (a = t[c], r != null && a >= r)
        break;
    } else
      t[c] < 0 && (e12[et] += 65536), (a < i || i == -1) && (Cf(e12, n, t, c), e12[et] = (e12[et] & 4294901760) + c + 2), c++;
}
function Zc(e12, t) {
  T(b.LifecycleHookStart, e12, t);
  let n = g(null);
  try {
    t.call(e12);
  } finally {
    g(n), T(b.LifecycleHookEnd, e12, t);
  }
}
function Cf(e12, t, n, r) {
  let o = n[r] < 0, i = n[r + 1], s = o ? -n[r] : n[r], a = e12[s];
  o ? e12[y] >> 14 < e12[et] >> 16 && (e12[y] & 3) === t && (e12[y] += 16384, Zc(a, i)) : Zc(a, i);
}
var At = -1;
var sn = class {
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
function Tf(e12, t, n) {
  let r = 0;
  for (; r < n.length; ) {
    let o = n[r];
    if (typeof o == "number") {
      if (o !== 0)
        break;
      r++;
      let i = n[r++], s = n[r++], a = n[r++];
      e12.setAttribute(t, s, a, i);
    } else {
      let i = o, s = n[++r];
      Mf(i) ? e12.setProperty(t, i, s) : e12.setAttribute(t, i, s), r++;
    }
  }
  return r;
}
function Mf(e12) {
  return e12.charCodeAt(0) === 64;
}
function Fr(e12, t) {
  if (!(t === null || t.length === 0))
    if (e12 === null || e12.length === 0)
      e12 = t.slice();
    else {
      let n = -1;
      for (let r = 0; r < t.length; r++) {
        let o = t[r];
        typeof o == "number" ? n = o : n === 0 || (n === -1 || n === 2 ? Qc(e12, n, o, null, t[++r]) : Qc(e12, n, o, null, null));
      }
    }
  return e12;
}
function Qc(e12, t, n, r, o) {
  let i = 0, s = e12.length;
  if (t === -1)
    s = -1;
  else
    for (; i < e12.length; ) {
      let a = e12[i++];
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
  for (; i < e12.length; ) {
    let a = e12[i];
    if (typeof a == "number")
      break;
    if (a === n) {
      o !== null && (e12[i + 1] = o);
      return;
    }
    i++, o !== null && i++;
  }
  s !== -1 && (e12.splice(s, 0, t), i = s + 1), e12.splice(i++, 0, n), o !== null && e12.splice(i++, 0, o);
}
function Sl(e12) {
  return e12 !== At;
}
function Tr(e12) {
  return e12 & 32767;
}
function _f(e12) {
  return e12 >> 16;
}
function Mr(e12, t) {
  let n = _f(e12), r = t;
  for (; n > 0; )
    r = r[Xe], n--;
  return r;
}
var Ui = true;
function Yc(e12) {
  let t = Ui;
  return Ui = e12, t;
}
var Sf = 256;
var Nl = Sf - 1;
var xl = 5;
var Nf = 0;
var he = {};
function xf(e12, t, n) {
  let r;
  typeof n == "string" ? r = n.charCodeAt(0) || 0 : n.hasOwnProperty(Qe) && (r = n[Qe]), r == null && (r = n[Qe] = Nf++);
  let o = r & Nl, i = 1 << o;
  t.data[e12 + (o >> xl)] |= i;
}
function Al(e12, t) {
  let n = Rl(e12, t);
  if (n !== -1)
    return n;
  let r = t[m];
  r.firstCreatePass && (e12.injectorIndex = t.length, Fi(r.data, e12), Fi(t, null), Fi(r.blueprint, null));
  let o = _s(e12, t), i = e12.injectorIndex;
  if (Sl(o)) {
    let s = Tr(o), a = Mr(o, t), c = a[m].data;
    for (let l = 0; l < 8; l++)
      t[i + l] = a[s + l] | c[s + l];
  }
  return t[i + 8] = o, i;
}
function Fi(e12, t) {
  e12.push(0, 0, 0, 0, 0, 0, 0, 0, t);
}
function Rl(e12, t) {
  return e12.injectorIndex === -1 || e12.parent && e12.parent.injectorIndex === e12.injectorIndex || t[e12.injectorIndex + 8] === null ? -1 : e12.injectorIndex;
}
function _s(e12, t) {
  if (e12.parent && e12.parent.injectorIndex !== -1)
    return e12.parent.injectorIndex;
  let n = 0, r = null, o = t;
  for (; o !== null; ) {
    if (r = Fl(o), r === null)
      return At;
    if (n++, o = o[Xe], r.injectorIndex !== -1)
      return r.injectorIndex | n << 16;
  }
  return At;
}
function Af(e12, t, n) {
  xf(e12, t, n);
}
function Ol(e12, t, n) {
  if (n & 8 || e12 !== void 0)
    return e12;
  Xn(t, "NodeInjector");
}
function kl(e12, t, n, r) {
  if (n & 8 && r === void 0 && (r = null), (n & 3) === 0) {
    let o = e12[De], i = z(void 0);
    try {
      return o ? o.get(t, r, n & 8) : ai(t, r, n & 8);
    } finally {
      z(i);
    }
  }
  return Ol(r, t, n);
}
function Pl(e12, t, n, r = 0, o) {
  if (e12 !== null) {
    if (t[y] & 2048 && !(r & 2)) {
      let s = Pf(e12, t, n, r, he);
      if (s !== he)
        return s;
    }
    let i = Ll(e12, t, n, r, he);
    if (i !== he)
      return i;
  }
  return kl(t, n, r, o);
}
function Ll(e12, t, n, r, o) {
  let i = Of(n);
  if (typeof i == "function") {
    if (!Si(t, e12, r))
      return r & 1 ? Ol(o, n, r) : kl(t, n, r, o);
    try {
      let s;
      if (s = i(r), s == null && !(r & 8))
        Xn(n);
      else
        return s;
    } finally {
      Ni();
    }
  } else if (typeof i == "number") {
    let s = null, a = Rl(e12, t), c = At, l = r & 1 ? t[X][J] : null;
    for ((a === -1 || r & 4) && (c = a === -1 ? _s(e12, t) : t[a + 8], c === At || !Jc(r, false) ? a = -1 : (s = t[m], a = Tr(c), t = Mr(c, t))); a !== -1; ) {
      let u = t[m];
      if (Kc(i, a, u.data)) {
        let d = Rf(a, t, n, s, r, l);
        if (d !== he)
          return d;
      }
      c = t[a + 8], c !== At && Jc(r, t[m].data[a + 8] === l) && Kc(i, a, t) ? (s = u, a = Tr(c), t = Mr(c, t)) : a = -1;
    }
  }
  return o;
}
function Rf(e12, t, n, r, o, i) {
  let s = t[m], a = s.data[e12 + 8], c = r == null ? bt(a) && Ui : r != s && (a.type & 3) !== 0, l = o & 1 && i === a, u = wr(a, s, n, c, l);
  return u !== null ? _r(t, s, u, a, o) : he;
}
function wr(e12, t, n, r, o) {
  let i = e12.providerIndexes, s = t.data, a = i & 1048575, c = e12.directiveStart, l = e12.directiveEnd, u = i >> 20, d = r ? a : a + u, f = o ? a + u : l;
  for (let p = d; p < f; p++) {
    let h = s[p];
    if (p < c && n === h || p >= c && h.type === n)
      return p;
  }
  if (o) {
    let p = s[c];
    if (p && Ct(p) && p.type === n)
      return c;
  }
  return null;
}
function _r(e12, t, n, r, o) {
  let i = e12[n], s = t.data;
  if (i instanceof sn) {
    let a = i;
    if (a.resolving)
      throw si("");
    let c = Yc(a.canSeeViewProviders);
    a.resolving = true;
    let l = s[n].type || s[n], u, d = a.injectImpl ? z(a.injectImpl) : null, f = Si(e12, r, 0);
    try {
      i = e12[n] = a.factory(void 0, o, s, e12, r), t.firstCreatePass && n >= r.directiveStart && wf(n, s[n], t);
    } finally {
      d !== null && z(d), Yc(c), a.resolving = false, Ni();
    }
  }
  return i;
}
function Of(e12) {
  if (typeof e12 == "string")
    return e12.charCodeAt(0) || 0;
  let t = e12.hasOwnProperty(Qe) ? e12[Qe] : void 0;
  return typeof t == "number" ? t >= 0 ? t & Nl : kf : t;
}
function Kc(e12, t, n) {
  let r = 1 << e12;
  return !!(n[t + (e12 >> xl)] & r);
}
function Jc(e12, t) {
  return !(e12 & 2) && !(e12 & 1 && t);
}
var ot = class {
  _tNode;
  _lView;
  constructor(t, n) {
    this._tNode = t, this._lView = n;
  }
  get(t, n, r) {
    return Pl(this._tNode, this._lView, t, Ge(r), n);
  }
};
function kf() {
  return new ot(pe(), M());
}
function Pf(e12, t, n, r, o) {
  let i = e12, s = t;
  for (; i !== null && s !== null && s[y] & 2048 && !Tt(s); ) {
    let a = Ll(i, s, n, r | 2, he);
    if (a !== he)
      return a;
    let c = i.parent;
    if (!c) {
      let l = s[hi];
      if (l) {
        let u = l.get(n, he, r & -5);
        if (u !== he)
          return u;
      }
      c = Fl(s), s = s[Xe];
    }
    i = c;
  }
  return o;
}
function Fl(e12) {
  let t = e12[m], n = t.type;
  return n === 2 ? t.declTNode : n === 1 ? e12[J] : null;
}
function Lf() {
  return Pt(pe(), M());
}
function Pt(e12, t) {
  return new hn(de(e12, t));
}
var hn = /* @__PURE__ */ (() => {
  class e12 {
    nativeElement;
    constructor(n) {
      this.nativeElement = n;
    }
    static __NG_ELEMENT_ID__ = Lf;
  }
  return e12;
})();
function Ff(e12) {
  return e12 instanceof hn ? e12.nativeElement : e12;
}
function jf() {
  return this._results[Symbol.iterator]();
}
var Sr = class {
  _emitDistinctChangesOnly;
  dirty = true;
  _onDirty = void 0;
  _results = [];
  _changesDetected = false;
  _changes = void 0;
  length = 0;
  first = void 0;
  last = void 0;
  get changes() {
    return this._changes ??= new ye();
  }
  constructor(t = false) {
    this._emitDistinctChangesOnly = t;
  }
  get(t) {
    return this._results[t];
  }
  map(t) {
    return this._results.map(t);
  }
  filter(t) {
    return this._results.filter(t);
  }
  find(t) {
    return this._results.find(t);
  }
  reduce(t, n) {
    return this._results.reduce(t, n);
  }
  forEach(t) {
    this._results.forEach(t);
  }
  some(t) {
    return this._results.some(t);
  }
  toArray() {
    return this._results.slice();
  }
  toString() {
    return this._results.toString();
  }
  reset(t, n) {
    this.dirty = false;
    let r = ec(t);
    (this._changesDetected = !Xa(this._results, r, n)) && (this._results = r, this.length = r.length, this.last = r[this.length - 1], this.first = r[0]);
  }
  notifyOnChanges() {
    this._changes !== void 0 && (this._changesDetected || !this._emitDistinctChangesOnly) && this._changes.next(this);
  }
  onDirty(t) {
    this._onDirty = t;
  }
  setDirty() {
    this.dirty = true, this._onDirty?.();
  }
  destroy() {
    this._changes !== void 0 && (this._changes.complete(), this._changes.unsubscribe());
  }
  [Symbol.iterator] = jf;
};
function jl(e12) {
  return (e12.flags & 128) === 128;
}
var Ss = function(e12) {
  return e12[e12.OnPush = 0] = "OnPush", e12[e12.Eager = 1] = "Eager", e12[e12.Default = 1] = "Default", e12;
}(Ss || {});
var Hl = /* @__PURE__ */ new Map();
var Hf = 0;
function Vf() {
  return Hf++;
}
function Bf(e12) {
  Hl.set(e12[we], e12);
}
function zi(e12) {
  Hl.delete(e12[we]);
}
var Xc = "__ngContext__";
function Rt(e12, t) {
  Le(t) ? (e12[Xc] = t[we], Bf(t)) : e12[Xc] = t;
}
function Vl(e12) {
  return $l(e12[wt]);
}
function Bl(e12) {
  return $l(e12[K]);
}
function $l(e12) {
  for (; e12 !== null && !re(e12); )
    e12 = e12[K];
  return e12;
}
var Wi;
function Ns(e12) {
  Wi = e12;
}
function Ul() {
  if (Wi !== void 0)
    return Wi;
  if (typeof document < "u")
    return document;
  throw new v(210, false);
}
var jr = new D("", { factory: () => $f });
var $f = "ng";
var Hr = new D("");
var gn = new D("", { providedIn: "platform", factory: () => "unknown" });
var Vr = new D("", { factory: () => E(U).body?.querySelector("[ngCspNonce]")?.getAttribute("ngCspNonce") || null });
var zl = "r";
var Wl = "di";
var Gl = false;
var ql = new D("", { factory: () => Gl });
var el = /* @__PURE__ */ new WeakMap();
function Uf(e12, t) {
  if (e12 == null || typeof e12 != "object")
    return;
  let n = el.get(e12);
  n || (n = /* @__PURE__ */ new WeakSet(), el.set(e12, n)), n.add(t);
}
var zf = (e12, t, n, r) => {
};
function Wf(e12, t, n, r) {
  zf(e12, t, n, r);
}
function xs(e12) {
  return (e12.flags & 32) === 32;
}
var Gf = () => null;
function Zl(e12, t, n = false) {
  return Gf(e12, t, n);
}
function Ql(e12, t) {
  let n = e12.contentQueries;
  if (n !== null) {
    let r = g(null);
    try {
      for (let o = 0; o < n.length; o += 2) {
        let i = n[o], s = n[o + 1];
        if (s !== -1) {
          let a = e12.data[s];
          lr(i), a.contentQueries(2, t[s], s);
        }
      }
    } finally {
      g(r);
    }
  }
}
function Gi(e12, t, n) {
  lr(0);
  let r = g(null);
  try {
    t(e12, n);
  } finally {
    g(r);
  }
}
function qf(e12, t, n) {
  if (mi(t)) {
    let r = g(null);
    try {
      let o = t.directiveStart, i = t.directiveEnd;
      for (let s = o; s < i; s++) {
        let a = e12.data[s];
        if (a.contentQueries) {
          let c = n[s];
          a.contentQueries(1, c, s);
        }
      }
    } finally {
      g(r);
    }
  }
}
var ie = function(e12) {
  return e12[e12.Emulated = 0] = "Emulated", e12[e12.None = 2] = "None", e12[e12.ShadowDom = 3] = "ShadowDom", e12[e12.ExperimentalIsolatedShadowDom = 4] = "ExperimentalIsolatedShadowDom", e12;
}(ie || {});
var mr;
function Zf() {
  if (mr === void 0 && (mr = null, Re.trustedTypes))
    try {
      mr = Re.trustedTypes.createPolicy("angular", { createHTML: (e12) => e12, createScript: (e12) => e12, createScriptURL: (e12) => e12 });
    } catch {
    }
  return mr;
}
function Br(e12) {
  return Zf()?.createHTML(e12) || e12;
}
var yr;
function Qf() {
  if (yr === void 0 && (yr = null, Re.trustedTypes))
    try {
      yr = Re.trustedTypes.createPolicy("angular#unsafe-bypass", { createHTML: (e12) => e12, createScript: (e12) => e12, createScriptURL: (e12) => e12 });
    } catch {
    }
  return yr;
}
function tl(e12) {
  return Qf()?.createHTML(e12) || e12;
}
var Ce = class {
  changingThisBreaksApplicationSecurity;
  constructor(t) {
    this.changingThisBreaksApplicationSecurity = t;
  }
  toString() {
    return `SafeValue must use [property]=binding: ${this.changingThisBreaksApplicationSecurity} (see ${qn})`;
  }
};
var qi = class extends Ce {
  getTypeName() {
    return "HTML";
  }
};
var Zi = class extends Ce {
  getTypeName() {
    return "Style";
  }
};
var Qi = class extends Ce {
  getTypeName() {
    return "Script";
  }
};
var Yi = class extends Ce {
  getTypeName() {
    return "URL";
  }
};
var Ki = class extends Ce {
  getTypeName() {
    return "ResourceURL";
  }
};
function Me(e12) {
  return e12 instanceof Ce ? e12.changingThisBreaksApplicationSecurity : e12;
}
function He(e12, t) {
  let n = Yl(e12);
  if (n != null && n !== t) {
    if (n === "ResourceURL" && t === "URL")
      return true;
    throw new Error(`Required a safe ${t}, got a ${n} (see ${qn})`);
  }
  return n === t;
}
function Yl(e12) {
  return e12 instanceof Ce && e12.getTypeName() || null;
}
function As(e12) {
  return new qi(e12);
}
function Rs(e12) {
  return new Zi(e12);
}
function Os(e12) {
  return new Qi(e12);
}
function ks(e12) {
  return new Yi(e12);
}
function Ps(e12) {
  return new Ki(e12);
}
function Yf(e12) {
  let t = new Xi(e12);
  return Kf() ? new Ji(t) : t;
}
var Ji = class {
  inertDocumentHelper;
  constructor(t) {
    this.inertDocumentHelper = t;
  }
  getInertBodyElement(t) {
    t = "<body><remove></remove>" + t;
    try {
      let n = new window.DOMParser().parseFromString(Br(t), "text/html").body;
      return n === null ? this.inertDocumentHelper.getInertBodyElement(t) : (n.firstChild?.remove(), n);
    } catch {
      return null;
    }
  }
};
var Xi = class {
  defaultDoc;
  inertDocument;
  constructor(t) {
    this.defaultDoc = t, this.inertDocument = this.defaultDoc.implementation.createHTMLDocument("sanitization-inert");
  }
  getInertBodyElement(t) {
    let n = this.inertDocument.createElement("template");
    return n.innerHTML = Br(t), n;
  }
};
function Kf() {
  try {
    return !!new window.DOMParser().parseFromString(Br(""), "text/html");
  } catch {
    return false;
  }
}
var Jf = /^(?!javascript:)(?:[a-z0-9+.-]+:|[^&:\/?#]*(?:[\/?#]|$))/i;
function $r(e12) {
  return e12 = String(e12), e12.match(Jf) ? e12 : "unsafe:" + e12;
}
function _e(e12) {
  let t = {};
  for (let n of e12.split(","))
    t[n] = true;
  return t;
}
function mn(...e12) {
  let t = {};
  for (let n of e12)
    for (let r in n)
      n.hasOwnProperty(r) && (t[r] = true);
  return t;
}
var Kl = _e("area,br,col,hr,img,wbr");
var Jl = _e("colgroup,dd,dt,li,p,tbody,td,tfoot,th,thead,tr");
var Xl = _e("rp,rt");
var Xf = mn(Xl, Jl);
var ep = mn(Jl, _e("address,article,aside,blockquote,caption,center,del,details,dialog,dir,div,dl,figure,figcaption,footer,h1,h2,h3,h4,h5,h6,header,hgroup,hr,ins,main,map,menu,nav,ol,pre,section,summary,table,ul"));
var tp = mn(Xl, _e("a,abbr,acronym,audio,b,bdi,bdo,big,br,cite,code,del,dfn,em,font,i,img,ins,kbd,label,map,mark,picture,q,ruby,rp,rt,s,samp,small,source,span,strike,strong,sub,sup,time,track,tt,u,var,video"));
var nl = mn(Kl, ep, tp, Xf);
var eu = _e("background,cite,href,itemtype,longdesc,poster,src,xlink:href");
var np = _e("abbr,accesskey,align,alt,autoplay,axis,bgcolor,border,cellpadding,cellspacing,class,clear,color,cols,colspan,compact,controls,coords,datetime,default,dir,download,face,headers,height,hidden,hreflang,hspace,ismap,itemscope,itemprop,kind,label,lang,language,loop,media,muted,nohref,nowrap,open,preload,rel,rev,role,rows,rowspan,rules,scope,scrolling,shape,size,sizes,span,srclang,srcset,start,summary,tabindex,target,title,translate,type,usemap,valign,value,vspace,width");
var rp = _e("aria-activedescendant,aria-atomic,aria-autocomplete,aria-busy,aria-checked,aria-colcount,aria-colindex,aria-colspan,aria-controls,aria-current,aria-describedby,aria-details,aria-disabled,aria-dropeffect,aria-errormessage,aria-expanded,aria-flowto,aria-grabbed,aria-haspopup,aria-hidden,aria-invalid,aria-keyshortcuts,aria-label,aria-labelledby,aria-level,aria-live,aria-modal,aria-multiline,aria-multiselectable,aria-orientation,aria-owns,aria-placeholder,aria-posinset,aria-pressed,aria-readonly,aria-relevant,aria-required,aria-roledescription,aria-rowcount,aria-rowindex,aria-rowspan,aria-selected,aria-setsize,aria-sort,aria-valuemax,aria-valuemin,aria-valuenow,aria-valuetext");
var op = mn(eu, np, rp);
var ip = _e("script,style,template");
var es = class {
  sanitizedSomething = false;
  buf = [];
  sanitizeChildren(t) {
    let n = t.firstChild, r = true, o = [];
    for (; n; ) {
      if (n.nodeType === Node.ELEMENT_NODE ? r = this.startElement(n) : n.nodeType === Node.TEXT_NODE ? this.chars(n.nodeValue) : this.sanitizedSomething = true, r && n.firstChild) {
        o.push(n), n = cp(n);
        continue;
      }
      for (; n; ) {
        n.nodeType === Node.ELEMENT_NODE && this.endElement(n);
        let i = ap(n);
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
    let n = rl(t).toLowerCase();
    if (!nl.hasOwnProperty(n))
      return this.sanitizedSomething = true, !ip.hasOwnProperty(n);
    this.buf.push("<"), this.buf.push(n);
    let r = t.attributes;
    for (let o = 0; o < r.length; o++) {
      let i = r.item(o), s = i.name, a = s.toLowerCase();
      if (!op.hasOwnProperty(a)) {
        this.sanitizedSomething = true;
        continue;
      }
      let c = i.value;
      eu[a] && (c = $r(c)), this.buf.push(" ", s, '="', ol(c), '"');
    }
    return this.buf.push(">"), true;
  }
  endElement(t) {
    let n = rl(t).toLowerCase();
    nl.hasOwnProperty(n) && !Kl.hasOwnProperty(n) && (this.buf.push("</"), this.buf.push(n), this.buf.push(">"));
  }
  chars(t) {
    this.buf.push(ol(t));
  }
};
function sp(e12, t) {
  return (e12.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_CONTAINED_BY) !== Node.DOCUMENT_POSITION_CONTAINED_BY;
}
function ap(e12) {
  let t = e12.nextSibling;
  if (t && e12 !== t.previousSibling)
    throw tu(t);
  return t;
}
function cp(e12) {
  let t = e12.firstChild;
  if (t && sp(e12, t))
    throw tu(t);
  return t;
}
function rl(e12) {
  let t = e12.nodeName;
  return typeof t == "string" ? t : "FORM";
}
function tu(e12) {
  return new Error(`Failed to sanitize html because the element is clobbered: ${e12.outerHTML}`);
}
var lp = /[\uD800-\uDBFF][\uDC00-\uDFFF]/g;
var up = /([^\#-~ |!])/g;
function ol(e12) {
  return e12.replace(/&/g, "&amp;").replace(lp, function(t) {
    let n = t.charCodeAt(0), r = t.charCodeAt(1);
    return "&#" + ((n - 55296) * 1024 + (r - 56320) + 65536) + ";";
  }).replace(up, function(t) {
    return "&#" + t.charCodeAt(0) + ";";
  }).replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
var vr;
function Ur(e12, t) {
  let n = null;
  try {
    vr = vr || Yf(e12);
    let r = t ? String(t) : "";
    n = vr.getInertBodyElement(r);
    let o = 5, i = r;
    do {
      if (o === 0)
        throw new Error("Failed to sanitize html because the input is unstable");
      o--, r = i, i = n.innerHTML, n = vr.getInertBodyElement(r);
    } while (r !== i);
    let a = new es().sanitizeChildren(il(n) || n);
    return Br(a);
  } finally {
    if (n) {
      let r = il(n) || n;
      for (; r.firstChild; )
        r.firstChild.remove();
    }
  }
}
function il(e12) {
  return "content" in e12 && dp(e12) ? e12.content : null;
}
function dp(e12) {
  return e12.nodeType === Node.ELEMENT_NODE && e12.nodeName === "TEMPLATE";
}
function fp(e12, t) {
  return e12.createText(t);
}
function pp(e12, t, n) {
  e12.setValue(t, n);
}
function nu(e12, t, n) {
  return e12.createElement(t, n);
}
function Nr(e12, t, n, r, o) {
  e12.insertBefore(t, n, r, o);
}
function ru(e12, t, n) {
  e12.appendChild(t, n);
}
function sl(e12, t, n, r, o) {
  r !== null ? Nr(e12, t, n, r, o) : ru(e12, t, n);
}
function ou(e12, t, n, r) {
  e12.removeChild(null, t, n, r);
}
function hp(e12, t, n) {
  e12.setAttribute(t, "style", n);
}
function gp(e12, t, n) {
  n === "" ? e12.removeAttribute(t, "class") : e12.setAttribute(t, "class", n);
}
function iu(e12, t, n) {
  let { mergedAttrs: r, classes: o, styles: i } = n;
  r !== null && Tf(e12, t, r), o !== null && gp(e12, t, o), i !== null && hp(e12, t, i);
}
var ge = function(e12) {
  return e12[e12.NONE = 0] = "NONE", e12[e12.HTML = 1] = "HTML", e12[e12.STYLE = 2] = "STYLE", e12[e12.SCRIPT = 3] = "SCRIPT", e12[e12.URL = 4] = "URL", e12[e12.RESOURCE_URL = 5] = "RESOURCE_URL", e12;
}(ge || {});
function Ls(e12) {
  let t = mp();
  return t ? tl(t.sanitize(ge.HTML, e12) || "") : He(e12, "HTML") ? tl(Me(e12)) : Ur(Ul(), ii(e12));
}
function mp() {
  let e12 = M();
  return e12 && e12[le].sanitizer;
}
var yp = "ng-template";
function vp(e12) {
  return e12.type === 4 && e12.value !== yp;
}
function ts(e12) {
  return (e12 & 1) === 0;
}
function al(e12, t) {
  return e12 ? ":not(" + t.trim() + ")" : t;
}
function Ep(e12) {
  let t = e12[0], n = 1, r = 2, o = "", i = false;
  for (; n < e12.length; ) {
    let s = e12[n];
    if (typeof s == "string")
      if (r & 2) {
        let a = e12[++n];
        o += "[" + s + (a.length > 0 ? '="' + a + '"' : "") + "]";
      } else
        r & 8 ? o += "." + s : r & 4 && (o += " " + s);
    else
      o !== "" && !ts(s) && (t += al(i, o), o = ""), r = s, i = i || !ts(r);
    n++;
  }
  return o !== "" && (t += al(i, o)), t;
}
function Ip(e12) {
  return e12.map(Ep).join(",");
}
function Dp(e12) {
  let t = [], n = [], r = 1, o = 2;
  for (; r < e12.length; ) {
    let i = e12[r];
    if (typeof i == "string")
      o === 2 ? i !== "" && t.push(i, e12[++r]) : o === 8 && n.push(i);
    else {
      if (!ts(o))
        break;
      o = i;
    }
    r++;
  }
  return n.length && t.push(1, ...n), t;
}
var Se = {};
function Fs(e12, t, n, r, o, i, s, a, c, l, u) {
  let d = F + r, f = d + o, p = wp(d, f), h = typeof l == "function" ? l() : l;
  return p[m] = { type: e12, blueprint: p, template: n, queries: null, viewQuery: a, declTNode: t, data: p.slice().fill(null, d), bindingStartIndex: d, expandoStartIndex: f, hostBindingOpCodes: null, firstCreatePass: true, firstUpdatePass: true, staticViewQueries: false, staticContentQueries: false, preOrderHooks: null, preOrderCheckHooks: null, contentHooks: null, contentCheckHooks: null, viewHooks: null, viewCheckHooks: null, destroyHooks: null, cleanup: null, contentQueries: null, components: null, directiveRegistry: typeof i == "function" ? i() : i, pipeRegistry: typeof s == "function" ? s() : s, firstChild: null, schemas: c, consts: h, incompleteFirstPass: false, ssrId: u };
}
function wp(e12, t) {
  let n = [];
  for (let r = 0; r < t; r++)
    n.push(r < e12 ? null : Se);
  return n;
}
function bp(e12) {
  let t = e12.tView;
  return t === null || t.incompleteFirstPass ? e12.tView = Fs(1, null, e12.template, e12.decls, e12.vars, e12.directiveDefs, e12.pipeDefs, e12.viewQuery, e12.schemas, e12.consts, e12.id) : t;
}
function js(e12, t, n, r, o, i, s, a, c, l, u) {
  let d = t.blueprint.slice();
  return d[ne] = o, d[y] = r | 4 | 128 | 8 | 64 | 1024, (l !== null || e12 && e12[y] & 2048) && (d[y] |= 2048), Ei(d), d[R] = d[Xe] = e12, d[x] = n, d[le] = s || e12 && e12[le], d[O] = a || e12 && e12[O], d[De] = c || e12 && e12[De] || null, d[J] = i, d[we] = Vf(), d[It] = u, d[hi] = l, d[X] = t.type == 2 ? e12[X] : d, d;
}
function Cp(e12, t, n) {
  let r = de(t, e12), o = bp(n), i = e12[le].rendererFactory, s = Hs(e12, js(e12, o, null, su(n), r, t, null, i.createRenderer(r, n), null, null, null));
  return e12[t.index] = s;
}
function su(e12) {
  let t = 16;
  return e12.signals ? t = 4096 : e12.onPush && (t = 64), t;
}
function au(e12, t, n, r) {
  if (n === 0)
    return -1;
  let o = t.length;
  for (let i = 0; i < n; i++)
    t.push(r), e12.blueprint.push(r), e12.data.push(null);
  return o;
}
function Hs(e12, t) {
  return e12[wt] ? e12[pi][K] = t : e12[wt] = t, e12[pi] = t, t;
}
function V(e12 = 1) {
  cu(oe(), M(), Fe() + e12, false);
}
function cu(e12, t, n, r) {
  if (!r)
    if ((t[y] & 3) === 3) {
      let i = e12.preOrderCheckHooks;
      i !== null && Ir(t, i, n);
    } else {
      let i = e12.preOrderHooks;
      i !== null && Dr(t, i, 0, n);
    }
  je(n);
}
var zr = function(e12) {
  return e12[e12.None = 0] = "None", e12[e12.SignalBased = 1] = "SignalBased", e12[e12.HasDecoratorInputTransform = 2] = "HasDecoratorInputTransform", e12;
}(zr || {});
function ns(e12, t, n, r) {
  let o = g(null);
  try {
    let [i, s, a] = e12.inputs[n], c = null;
    (s & zr.SignalBased) !== 0 && (c = t[i][Z]), c !== null && c.transformFn !== void 0 ? r = c.transformFn(r) : a !== null && (r = a.call(t, r)), e12.setInput !== null ? e12.setInput(t, c, r, n, i) : Cl(t, c, i, r);
  } finally {
    g(o);
  }
}
var Te = function(e12) {
  return e12[e12.Important = 1] = "Important", e12[e12.DashCase = 2] = "DashCase", e12;
}(Te || {});
var Tp;
function Vs(e12, t) {
  return Tp(e12, t);
}
var $E = typeof document < "u" && typeof document?.documentElement?.getAnimations == "function";
var rs = /* @__PURE__ */ new WeakMap();
var nn = /* @__PURE__ */ new WeakSet();
function Mp(e12, t) {
  let n = rs.get(e12);
  if (!n || n.length === 0)
    return;
  let r = t.parentNode, o = t.previousSibling;
  for (let i = n.length - 1; i >= 0; i--) {
    let s = n[i], a = s.parentNode;
    s === t ? (n.splice(i, 1), nn.add(s), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } }))) : (o && s === o || a && r && a !== r) && (n.splice(i, 1), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } })), s.parentNode?.removeChild(s));
  }
}
function _p(e12, t) {
  let n = rs.get(e12);
  n ? n.includes(t) || n.push(t) : rs.set(e12, [t]);
}
var it = /* @__PURE__ */ new Set();
var Bs = function(e12) {
  return e12[e12.CHANGE_DETECTION = 0] = "CHANGE_DETECTION", e12[e12.AFTER_NEXT_RENDER = 1] = "AFTER_NEXT_RENDER", e12;
}(Bs || {});
var Lt = new D("");
var cl = /* @__PURE__ */ new Set();
function Ft(e12) {
  cl.has(e12) || (cl.add(e12), performance?.mark?.("mark_feature_usage", { detail: { feature: e12 } }));
}
var lu = (() => {
  class e12 {
    impl = null;
    execute() {
      this.impl?.execute();
    }
    static \u0275prov = _({ token: e12, providedIn: "root", factory: () => new e12() });
  }
  return e12;
})();
var uu = new D("", { factory: () => ({ queue: /* @__PURE__ */ new Set(), isScheduled: false, scheduler: null, injector: E(Q) }) });
function du(e12, t, n) {
  let r = e12.get(uu);
  if (Array.isArray(t))
    for (let o of t)
      r.queue.add(o), n?.detachedLeaveAnimationFns?.push(o);
  else
    r.queue.add(t), n?.detachedLeaveAnimationFns?.push(t);
  r.scheduler && r.scheduler(e12);
}
function Sp(e12, t) {
  let n = e12.get(uu);
  if (t.detachedLeaveAnimationFns) {
    for (let r of t.detachedLeaveAnimationFns)
      n.queue.delete(r);
    t.detachedLeaveAnimationFns = void 0;
  }
}
function Np(e12, t) {
  for (let [n, r] of t)
    du(e12, r.animateFns);
}
function ll(e12, t, n, r) {
  let o = e12?.[ke]?.enter;
  t !== null && o && o.has(n.index) && Np(r, o);
}
function xt(e12, t, n, r, o, i, s, a) {
  if (o != null) {
    let c, l = false;
    re(o) ? c = o : Le(o) && (l = true, o = o[ne]);
    let u = ee(o);
    e12 === 0 && r !== null ? (ll(a, r, i, n), s == null ? ru(t, r, u) : Nr(t, r, u, s || null, true)) : e12 === 1 && r !== null ? (ll(a, r, i, n), Nr(t, r, u, s || null, true), Mp(i, u)) : e12 === 2 ? (a?.[ke]?.leave?.has(i.index) && _p(i, u), nn.delete(u), ul(a, i, n, (d) => {
      if (nn.has(u)) {
        nn.delete(u);
        return;
      }
      ou(t, u, l, d);
    })) : e12 === 3 && (nn.delete(u), ul(a, i, n, () => {
      t.destroyNode(u);
    })), c != null && $p(t, e12, n, c, i, r, s);
  }
}
function xp(e12, t) {
  fu(e12, t), t[ne] = null, t[J] = null;
}
function Ap(e12, t, n, r, o, i) {
  r[ne] = o, r[J] = t, Gr(e12, r, n, 1, o, i);
}
function fu(e12, t) {
  t[le].changeDetectionScheduler?.notify(9), Gr(e12, t, t[O], 2, null, null);
}
function Rp(e12) {
  let t = e12[wt];
  if (!t)
    return ji(e12[m], e12);
  for (; t; ) {
    let n = null;
    if (Le(t))
      n = t[wt];
    else {
      let r = t[S];
      r && (n = r);
    }
    if (!n) {
      for (; t && !t[K] && t !== e12; )
        Le(t) && ji(t[m], t), t = t[R];
      t === null && (t = e12), Le(t) && ji(t[m], t), n = t && t[K];
    }
    t = n;
  }
}
function $s(e12, t) {
  let n = e12[tt], r = n.indexOf(t);
  n.splice(r, 1);
}
function Wr(e12, t) {
  if (nt(t))
    return;
  let n = t[O];
  n.destroyNode && Gr(e12, t, n, 3, null, null), Rp(t);
}
function ji(e12, t) {
  if (nt(t))
    return;
  let n = g(null);
  try {
    t[y] &= -129, t[y] |= 256, t[G] && ut(t[G]), Pp(e12, t), kp(e12, t), t[m].type === 1 && t[O].destroy();
    let r = t[Oe];
    if (r !== null && re(t[R])) {
      r !== t[R] && $s(r, t);
      let o = t[ue];
      o !== null && o.detachView(e12);
    }
    zi(t);
  } finally {
    g(n);
  }
}
function ul(e12, t, n, r) {
  let o = e12?.[ke];
  if (o == null || o.leave == null || !o.leave.has(t.index))
    return r(false);
  e12 && it.add(e12[we]), du(n, () => {
    if (o.leave && o.leave.has(t.index)) {
      let s = o.leave.get(t.index), a = [];
      if (s) {
        for (let c = 0; c < s.animateFns.length; c++) {
          let l = s.animateFns[c], { promise: u } = l();
          a.push(u);
        }
        o.detachedLeaveAnimationFns = void 0;
      }
      o.running = Promise.allSettled(a), Op(e12, r);
    } else
      e12 && it.delete(e12[we]), r(false);
  }, o);
}
function Op(e12, t) {
  let n = e12[ke]?.running;
  if (n) {
    n.then(() => {
      e12[ke].running = void 0, it.delete(e12[we]), t(true);
    });
    return;
  }
  t(false);
}
function kp(e12, t) {
  let n = e12.cleanup, r = t[Dt];
  if (n !== null)
    for (let s = 0; s < n.length - 1; s += 2)
      if (typeof n[s] == "string") {
        let a = n[s + 3];
        a >= 0 ? r[a]() : r[-a].unsubscribe(), s += 2;
      } else {
        let a = r[n[s + 1]];
        n[s].call(a);
      }
  r !== null && (t[Dt] = null);
  let o = t[Ee];
  if (o !== null) {
    t[Ee] = null;
    for (let s = 0; s < o.length; s++) {
      let a = o[s];
      a();
    }
  }
  let i = t[xe];
  if (i !== null) {
    t[xe] = null;
    for (let s of i)
      s.destroy();
  }
}
function Pp(e12, t) {
  let n;
  if (e12 != null && (n = e12.destroyHooks) != null)
    for (let r = 0; r < n.length; r += 2) {
      let o = t[n[r]];
      if (!(o instanceof sn)) {
        let i = n[r + 1];
        if (Array.isArray(i))
          for (let s = 0; s < i.length; s += 2) {
            let a = o[i[s]], c = i[s + 1];
            T(b.LifecycleHookStart, a, c);
            try {
              c.call(a);
            } finally {
              T(b.LifecycleHookEnd, a, c);
            }
          }
        else {
          T(b.LifecycleHookStart, o, i);
          try {
            i.call(o);
          } finally {
            T(b.LifecycleHookEnd, o, i);
          }
        }
      }
    }
}
function Lp(e12, t, n) {
  return Fp(e12, t.parent, n);
}
function Fp(e12, t, n) {
  let r = t;
  for (; r !== null && r.type & 168; )
    t = r, r = t.parent;
  if (r === null)
    return n[ne];
  if (bt(r)) {
    let { encapsulation: o } = e12.data[r.directiveStart + r.componentOffset];
    if (o === ie.None || o === ie.Emulated)
      return null;
  }
  return de(r, n);
}
function jp(e12, t, n) {
  return Vp(e12, t, n);
}
function Hp(e12, t, n) {
  return e12.type & 40 ? de(e12, n) : null;
}
var Vp = Hp;
var dl;
function Us(e12, t, n, r) {
  let o = Lp(e12, r, t), i = t[O], s = r.parent || t[J], a = jp(s, r, t);
  if (o != null)
    if (Array.isArray(n))
      for (let c = 0; c < n.length; c++)
        sl(i, o, n[c], a, false);
    else
      sl(i, o, n, a, false);
  dl !== void 0 && dl(i, r, t, n, o);
}
function rn(e12, t) {
  if (t !== null) {
    let n = t.type;
    if (n & 3)
      return de(t, e12);
    if (n & 4)
      return os(-1, e12[t.index]);
    if (n & 8) {
      let r = t.child;
      if (r !== null)
        return rn(e12, r);
      {
        let o = e12[t.index];
        return re(o) ? os(-1, o) : ee(o);
      }
    } else {
      if (n & 128)
        return rn(e12, t.next);
      if (n & 32)
        return Vs(t, e12)() || ee(e12[t.index]);
      {
        let r = pu(e12, t);
        if (r !== null) {
          if (Array.isArray(r))
            return r[0];
          let o = Ae(e12[X]);
          return rn(o, r);
        } else
          return rn(e12, t.next);
      }
    }
  }
  return null;
}
function pu(e12, t) {
  if (t !== null) {
    let r = e12[X][J], o = t.projection;
    return r.projection[o];
  }
  return null;
}
function os(e12, t) {
  let n = S + e12 + 1;
  if (n < t.length) {
    let r = t[n], o = r[m].firstChild;
    if (o !== null)
      return rn(r, o);
  }
  return t[Pe];
}
function zs(e12, t, n, r, o, i, s) {
  for (; n != null; ) {
    let a = r[De];
    if (n.type === 128) {
      n = n.next;
      continue;
    }
    let c = r[n.index], l = n.type;
    if (s && t === 0 && (c && Rt(ee(c), r), n.flags |= 2), !xs(n))
      if (l & 8)
        zs(e12, t, n.child, r, o, i, false), xt(t, e12, a, o, c, n, i, r);
      else if (l & 32) {
        let u = Vs(n, r), d;
        for (; d = u(); )
          xt(t, e12, a, o, d, n, i, r);
        xt(t, e12, a, o, c, n, i, r);
      } else
        l & 16 ? Bp(e12, t, r, n, o, i) : xt(t, e12, a, o, c, n, i, r);
    n = s ? n.projectionNext : n.next;
  }
}
function Gr(e12, t, n, r, o, i) {
  zs(n, r, e12.firstChild, t, o, i, false);
}
function Bp(e12, t, n, r, o, i) {
  let s = n[X], c = s[J].projection[r.projection];
  if (Array.isArray(c))
    for (let l = 0; l < c.length; l++) {
      let u = c[l];
      xt(t, e12, n[De], o, u, r, i, n);
    }
  else {
    let l = c, u = s[R];
    jl(r) && (l.flags |= 128), zs(e12, t, l, u, o, i, true);
  }
}
function $p(e12, t, n, r, o, i, s) {
  let a = r[Pe], c = ee(r);
  a !== c && xt(t, e12, n, i, a, o, s);
  for (let l = S; l < r.length; l++) {
    let u = r[l];
    Gr(u[m], u, e12, t, i, a);
  }
}
function Up(e12, t, n, r, o) {
  if (t)
    o ? e12.addClass(n, r) : e12.removeClass(n, r);
  else {
    let i = r.indexOf("-") === -1 ? void 0 : Te.DashCase;
    o == null ? e12.removeStyle(n, r, i) : (typeof o == "string" && o.endsWith("!important") && (o = o.slice(0, -10), i |= Te.Important), e12.setStyle(n, r, o, i));
  }
}
function hu(e12, t, n, r, o) {
  let i = Fe(), s = r & 2;
  try {
    je(-1), s && t.length > F && cu(e12, t, F, false);
    let a = s ? b.TemplateUpdateStart : b.TemplateCreateStart;
    T(a, o, n), n(r, o);
  } finally {
    je(i);
    let a = s ? b.TemplateUpdateEnd : b.TemplateCreateEnd;
    T(a, o, n);
  }
}
function zp(e12, t, n) {
  Qp(e12, t, n), (n.flags & 64) === 64 && Yp(e12, t, n);
}
function gu(e12, t, n = de) {
  let r = t.localNames;
  if (r !== null) {
    let o = t.index + 1;
    for (let i = 0; i < r.length; i += 2) {
      let s = r[i + 1], a = s === -1 ? n(t, e12) : e12[s];
      e12[o++] = a;
    }
  }
}
function Wp(e12, t, n, r) {
  let i = r.get(ql, Gl) || n === ie.ShadowDom || n === ie.ExperimentalIsolatedShadowDom, s = e12.selectRootElement(t, i);
  return Gp(s), s;
}
function Gp(e12) {
  qp(e12);
}
var qp = () => null;
function Zp(e12, t, n, r, o, i) {
  if (e12.type & 3) {
    let s = de(e12, t);
    r = i != null ? i(r, e12.value || "", n) : r, o.setProperty(s, n, r);
  } else
    e12.type & 12;
}
function Qp(e12, t, n) {
  let r = n.directiveStart, o = n.directiveEnd;
  bt(n) && Cp(t, n, e12.data[r + n.componentOffset]), e12.firstCreatePass || Al(n, t);
  let i = n.initialInputs;
  for (let s = r; s < o; s++) {
    let a = e12.data[s], c = _r(t, e12, s, n);
    if (Rt(c, t), i !== null && Jp(t, s - r, c, a, n, i), Ct(a)) {
      let l = be(n.index, t);
      l[x] = _r(t, e12, s, n);
    }
  }
}
function Yp(e12, t, n) {
  let r = n.directiveStart, o = n.directiveEnd, i = n.index, s = Nc();
  try {
    je(i);
    for (let a = r; a < o; a++) {
      let c = e12.data[a], l = t[a];
      cr(a), (c.hostBindings !== null || c.hostVars !== 0 || c.hostAttrs !== null) && Kp(c, l);
    }
  } finally {
    je(-1), cr(s);
  }
}
function Kp(e12, t) {
  e12.hostBindings !== null && e12.hostBindings(1, t);
}
function Jp(e12, t, n, r, o, i) {
  let s = i[t];
  if (s !== null)
    for (let a = 0; a < s.length; a += 2) {
      let c = s[a], l = s[a + 1];
      ns(r, n, c, l);
    }
}
function Xp(e12, t, n, r, o) {
  let i = F + n, s = t[m], a = o(s, t, e12, r, n);
  t[i] = a, _t(e12, true);
  let c = e12.type === 2;
  return c ? (iu(t[O], a, e12), (yc() === 0 || yi(e12)) && Rt(a, t), vc()) : Rt(a, t), fr() && (!c || !xs(e12)) && Us(s, t, a, e12), e12;
}
function eh(e12) {
  let t = e12;
  return Ti() ? Cc() : (t = t.parent, _t(t, false)), t;
}
function th(e12, t) {
  let n = e12[De];
  if (!n)
    return;
  let r;
  try {
    r = n.get(rt, null);
  } catch {
    r = null;
  }
  r?.(t);
}
function nh(e12, t, n, r, o) {
  let i = e12.inputs?.[r], s = e12.hostDirectiveInputs?.[r], a = false;
  if (s)
    for (let c = 0; c < s.length; c += 2) {
      let l = s[c], u = s[c + 1], d = t.data[l];
      ns(d, n[l], u, o), a = true;
    }
  if (i)
    for (let c of i) {
      let l = n[c], u = t.data[c];
      ns(u, l, r, o), a = true;
    }
  return a;
}
function rh(e12, t) {
  let n = be(t, e12), r = n[m];
  oh(r, n);
  let o = n[ne];
  o !== null && n[It] === null && (n[It] = Zl(o, n[De])), T(b.ComponentStart);
  try {
    Ws(r, n, n[x]);
  } finally {
    T(b.ComponentEnd, n[x]);
  }
}
function oh(e12, t) {
  for (let n = t.length; n < e12.blueprint.length; n++)
    t.push(e12.blueprint[n]);
}
function Ws(e12, t, n) {
  ur(t);
  try {
    let r = e12.viewQuery;
    r !== null && Gi(1, r, n);
    let o = e12.template;
    o !== null && hu(e12, t, o, 1, n), e12.firstCreatePass && (e12.firstCreatePass = false), t[ue]?.finishViewCreation(e12), e12.staticContentQueries && Ql(e12, t), e12.staticViewQueries && Gi(2, e12.viewQuery, n);
    let i = e12.components;
    i !== null && ih(t, i);
  } catch (r) {
    throw e12.firstCreatePass && (e12.incompleteFirstPass = true, e12.firstCreatePass = false), r;
  } finally {
    t[y] &= -5, dr();
  }
}
function ih(e12, t) {
  for (let n = 0; n < t.length; n++)
    rh(e12, t[n]);
}
function qr(e12, t, n, r) {
  let o = g(null);
  try {
    let i = t.tView, a = e12[y] & 4096 ? 4096 : 16, c = js(e12, i, n, a, null, t, null, null, r?.injector ?? null, r?.embeddedViewInjector ?? null, r?.dehydratedView ?? null), l = e12[t.index];
    c[Oe] = l;
    let u = e12[ue];
    return u !== null && (c[ue] = u.createEmbeddedView(i)), Ws(i, c, n), c;
  } finally {
    g(o);
  }
}
function an(e12, t) {
  return !t || t.firstChild === null || jl(e12);
}
function cn(e12, t, n, r, o = false) {
  for (; n !== null; ) {
    if (n.type === 128) {
      n = o ? n.projectionNext : n.next;
      continue;
    }
    let i = t[n.index];
    i !== null && r.push(ee(i)), re(i) && mu(i, r);
    let s = n.type;
    if (s & 8)
      cn(e12, t, n.child, r);
    else if (s & 32) {
      let a = Vs(n, t), c;
      for (; c = a(); )
        r.push(c);
    } else if (s & 16) {
      let a = pu(t, n);
      if (Array.isArray(a))
        r.push(...a);
      else {
        let c = Ae(t[X]);
        cn(c[m], c, a, r, true);
      }
    }
    n = o ? n.projectionNext : n.next;
  }
  return r;
}
function mu(e12, t) {
  for (let n = S; n < e12.length; n++) {
    let r = e12[n], o = r[m].firstChild;
    o !== null && cn(r[m], r, o, t);
  }
  e12[Pe] !== e12[ne] && t.push(e12[Pe]);
}
function yu(e12) {
  if (e12[or] !== null) {
    for (let t of e12[or])
      t.impl.addSequence(t);
    e12[or].length = 0;
  }
}
var vu = [];
function sh(e12) {
  return e12[G] ?? ah(e12);
}
function ah(e12) {
  let t = vu.pop() ?? Object.create(lh);
  return t.lView = e12, t;
}
function ch(e12) {
  e12.lView[G] !== e12 && (e12.lView = null, vu.push(e12));
}
var lh = A(N({}, lt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e12) => {
  Mt(e12.lView);
}, consumerOnSignalRead() {
  this.lView[G] = this;
} });
function uh(e12) {
  let t = e12[G] ?? Object.create(dh);
  return t.lView = e12, t;
}
var dh = A(N({}, lt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e12) => {
  let t = Ae(e12.lView);
  for (; t && !Eu(t[m]); )
    t = Ae(t);
  t && Ii(t);
}, consumerOnSignalRead() {
  this.lView[G] = this;
} });
function Eu(e12) {
  return e12.type !== 2;
}
function Iu(e12) {
  if (e12[xe] === null)
    return;
  let t = true;
  for (; t; ) {
    let n = false;
    for (let r of e12[xe])
      r.dirty && (n = true, r.zone === null || Zone.current === r.zone ? r.run() : r.zone.run(() => r.run()));
    t = n && !!(e12[y] & 8192);
  }
}
var fh = 100;
function Du(e12, t = 0) {
  let r = e12[le].rendererFactory, o = false;
  o || r.begin?.();
  try {
    ph(e12, t);
  } finally {
    o || r.end?.();
  }
}
function ph(e12, t) {
  let n = Mi();
  try {
    Wt(true), is(e12, t);
    let r = 0;
    for (; Xt(e12); ) {
      if (r === fh)
        throw new v(103, false);
      r++, is(e12, 1);
    }
  } finally {
    Wt(n);
  }
}
function hh(e12, t, n, r) {
  if (nt(t))
    return;
  let o = t[y], i = false, s = false;
  ur(t);
  let a = true, c = null, l = null;
  i || (Eu(e12) ? (l = sh(t), c = Vt(l)) : xn() === null ? (a = false, l = uh(t), c = Vt(l)) : t[G] && (ut(t[G]), t[G] = null));
  try {
    Ei(t), Tc(e12.bindingStartIndex), n !== null && hu(e12, t, n, 2, r);
    let u = (o & 3) === 3;
    if (!i)
      if (u) {
        let p = e12.preOrderCheckHooks;
        p !== null && Ir(t, p, null);
      } else {
        let p = e12.preOrderHooks;
        p !== null && Dr(t, p, 0, null), Li(t, 0);
      }
    if (s || gh(t), Iu(t), wu(t, 0), e12.contentQueries !== null && Ql(e12, t), !i)
      if (u) {
        let p = e12.contentCheckHooks;
        p !== null && Ir(t, p);
      } else {
        let p = e12.contentHooks;
        p !== null && Dr(t, p, 1), Li(t, 1);
      }
    yh(e12, t);
    let d = e12.components;
    d !== null && Cu(t, d, 0);
    let f = e12.viewQuery;
    if (f !== null && Gi(2, f, r), !i)
      if (u) {
        let p = e12.viewCheckHooks;
        p !== null && Ir(t, p);
      } else {
        let p = e12.viewHooks;
        p !== null && Dr(t, p, 2), Li(t, 2);
      }
    if (e12.firstUpdatePass === true && (e12.firstUpdatePass = false), t[rr]) {
      for (let p of t[rr])
        p();
      t[rr] = null;
    }
    i || (yu(t), t[y] &= -73);
  } catch (u) {
    throw i || Mt(t), u;
  } finally {
    l !== null && (An(l, c), a && ch(l)), dr();
  }
}
function wu(e12, t) {
  for (let n = Vl(e12); n !== null; n = Bl(n))
    for (let r = S; r < n.length; r++) {
      let o = n[r];
      bu(o, t);
    }
}
function gh(e12) {
  for (let t = Vl(e12); t !== null; t = Bl(t)) {
    if (!(t[y] & 2))
      continue;
    let n = t[tt];
    for (let r = 0; r < n.length; r++) {
      let o = n[r];
      Ii(o);
    }
  }
}
function mh(e12, t, n) {
  T(b.ComponentStart);
  let r = be(t, e12);
  try {
    bu(r, n);
  } finally {
    T(b.ComponentEnd, r[x]);
  }
}
function bu(e12, t) {
  sr(e12) && is(e12, t);
}
function is(e12, t) {
  let r = e12[m], o = e12[y], i = e12[G], s = !!(t === 0 && o & 16);
  if (s ||= !!(o & 64 && t === 0), s ||= !!(o & 1024), s ||= !!(i?.dirty && Rn(i)), s ||= false, i && (i.dirty = false), e12[y] &= -9217, s)
    hh(r, e12, r.template, e12[x]);
  else if (o & 8192) {
    let a = g(null);
    try {
      Iu(e12), wu(e12, 1);
      let c = r.components;
      c !== null && Cu(e12, c, 1), yu(e12);
    } finally {
      g(a);
    }
  }
}
function Cu(e12, t, n) {
  for (let r = 0; r < t.length; r++)
    mh(e12, t[r], n);
}
function yh(e12, t) {
  let n = e12.hostBindingOpCodes;
  if (n !== null)
    try {
      for (let r = 0; r < n.length; r++) {
        let o = n[r];
        if (o < 0)
          je(~o);
        else {
          let i = o, s = n[++r], a = n[++r];
          Sc(s, i);
          let c = t[i];
          T(b.HostBindingsUpdateStart, c);
          try {
            a(2, c);
          } finally {
            T(b.HostBindingsUpdateEnd, c);
          }
        }
      }
    } finally {
      je(-1);
    }
}
function Gs(e12, t) {
  let n = Mi() ? 64 : 1088;
  for (e12[le].changeDetectionScheduler?.notify(t); e12; ) {
    e12[y] |= n;
    let r = Ae(e12);
    if (Tt(e12) && !r)
      return e12;
    e12 = r;
  }
  return null;
}
function Tu(e12, t, n, r) {
  return [e12, true, 0, t, null, r, null, n, null, null];
}
function Mu(e12, t) {
  let n = S + t;
  if (n < e12.length)
    return e12[n];
}
function Zr(e12, t, n, r = true) {
  let o = t[m];
  if (vh(o, t, e12, n), r) {
    let s = os(n, e12), a = t[O], c = a.parentNode(e12[Pe]);
    c !== null && Ap(o, e12[J], a, t, c, s);
  }
  let i = t[It];
  i !== null && i.firstChild !== null && (i.firstChild = null);
}
function _u(e12, t) {
  let n = ln(e12, t);
  return n !== void 0 && Wr(n[m], n), n;
}
function ln(e12, t) {
  if (e12.length <= S)
    return;
  let n = S + t, r = e12[n];
  if (r) {
    let o = r[Oe];
    o !== null && o !== e12 && $s(o, r), t > 0 && (e12[n - 1][K] = r[K]);
    let i = Zt(e12, S + t);
    xp(r[m], r);
    let s = i[ue];
    s !== null && s.detachView(i[m]), r[R] = null, r[K] = null, r[y] &= -129;
  }
  return r;
}
function vh(e12, t, n, r) {
  let o = S + r, i = n.length;
  r > 0 && (n[o - 1][K] = t), r < i - S ? (t[K] = n[o], ci(n, S + r, t)) : (n.push(t), t[K] = null), t[R] = n;
  let s = t[Oe];
  s !== null && n !== s && Su(s, t);
  let a = t[ue];
  a !== null && a.insertView(e12), ar(t), t[y] |= 128;
}
function Su(e12, t) {
  let n = e12[tt], r = t[R];
  if (Le(r))
    e12[y] |= 2;
  else {
    let o = r[R][X];
    t[X] !== o && (e12[y] |= 2);
  }
  n === null ? e12[tt] = [t] : n.push(t);
}
var Ot = class {
  _lView;
  _cdRefInjectingView;
  _appRef = null;
  _attachedToViewContainer = false;
  exhaustive;
  get rootNodes() {
    let t = this._lView, n = t[m];
    return cn(n, t, n.firstChild, []);
  }
  constructor(t, n) {
    this._lView = t, this._cdRefInjectingView = n;
  }
  get context() {
    return this._lView[x];
  }
  set context(t) {
    this._lView[x] = t;
  }
  get destroyed() {
    return nt(this._lView);
  }
  destroy() {
    if (this._appRef)
      this._appRef.detachView(this);
    else if (this._attachedToViewContainer) {
      let t = this._lView[R];
      if (re(t)) {
        let n = t[Jt], r = n ? n.indexOf(this) : -1;
        r > -1 && (ln(t, r), Zt(n, r));
      }
      this._attachedToViewContainer = false;
    }
    Wr(this._lView[m], this._lView);
  }
  onDestroy(t) {
    Di(this._lView, t);
  }
  markForCheck() {
    Gs(this._cdRefInjectingView || this._lView, 4);
  }
  detach() {
    this._lView[y] &= -129;
  }
  reattach() {
    ar(this._lView), this._lView[y] |= 128;
  }
  detectChanges() {
    this._lView[y] |= 1024, Du(this._lView);
  }
  checkNoChanges() {
  }
  attachToViewContainerRef() {
    if (this._appRef)
      throw new v(902, false);
    this._attachedToViewContainer = true;
  }
  detachFromAppRef() {
    this._appRef = null;
    let t = Tt(this._lView), n = this._lView[Oe];
    n !== null && !t && $s(n, this._lView), fu(this._lView[m], this._lView);
  }
  attachToAppRef(t) {
    if (this._attachedToViewContainer)
      throw new v(902, false);
    this._appRef = t;
    let n = Tt(this._lView), r = this._lView[Oe];
    r !== null && !n && Su(r, this._lView), ar(this._lView);
  }
};
var un = /* @__PURE__ */ (() => {
  class e12 {
    _declarationLView;
    _declarationTContainer;
    elementRef;
    static __NG_ELEMENT_ID__ = Eh;
    constructor(n, r, o) {
      this._declarationLView = n, this._declarationTContainer = r, this.elementRef = o;
    }
    get ssrId() {
      return this._declarationTContainer.tView?.ssrId || null;
    }
    createEmbeddedView(n, r) {
      return this.createEmbeddedViewImpl(n, r);
    }
    createEmbeddedViewImpl(n, r, o) {
      let i = qr(this._declarationLView, this._declarationTContainer, n, { embeddedViewInjector: r, dehydratedView: o });
      return new Ot(i);
    }
  }
  return e12;
})();
function Eh() {
  return qs(pe(), M());
}
function qs(e12, t) {
  return e12.type & 4 ? new un(t, e12, Pt(e12, t)) : null;
}
function Qr(e12, t, n, r, o) {
  let i = e12.data[t];
  if (i === null)
    i = Ih(e12, t, n, r, o), _c() && (i.flags |= 32);
  else if (i.type & 64) {
    i.type = n, i.value = r, i.attrs = o;
    let s = bc();
    i.injectorIndex = s === null ? -1 : s.injectorIndex;
  }
  return _t(i, true), i;
}
function Ih(e12, t, n, r, o) {
  let i = Ci(), s = Ti(), a = s ? i : i && i.parent, c = e12.data[t] = wh(e12, a, n, t, r, o);
  return Dh(e12, c, i, s), c;
}
function Dh(e12, t, n, r) {
  e12.firstChild === null && (e12.firstChild = t), n !== null && (r ? n.child == null && t.parent !== null && (n.child = t) : n.next === null && (n.next = t, t.prev = n));
}
function wh(e12, t, n, r, o, i) {
  let s = t ? t.injectorIndex : -1, a = 0;
  return Ic() && (a |= 128), { type: n, index: r, insertBeforeIndex: null, injectorIndex: s, directiveStart: -1, directiveEnd: -1, directiveStylingLast: -1, componentOffset: -1, controlDirectiveIndex: -1, customControlIndex: -1, propertyBindings: null, flags: a, providerIndexes: 0, value: o, attrs: i, mergedAttrs: null, localNames: null, initialInputs: null, inputs: null, hostDirectiveInputs: null, outputs: null, hostDirectiveOutputs: null, directiveToIndex: null, tView: null, next: null, prev: null, projectionNext: null, child: null, parent: t, projection: null, styles: null, stylesWithoutHost: null, residualStyles: void 0, classes: null, classesWithoutHost: null, residualClasses: void 0, classBindings: 0, styleBindings: 0 };
}
function bh(e12) {
  let t = e12[gi] ?? [], r = e12[R][O], o = [];
  for (let i of t)
    i.data[Wl] !== void 0 ? o.push(i) : Ch(i, r);
  e12[gi] = o;
}
function Ch(e12, t) {
  let n = 0, r = e12.firstChild;
  if (r) {
    let o = e12.data[zl];
    for (; n < o; ) {
      let i = r.nextSibling;
      ou(t, r, false), r = i, n++;
    }
  }
}
var Th = () => null;
var Mh = () => null;
function ss(e12, t) {
  return Th(e12, t);
}
function Nu(e12, t, n) {
  return Mh(e12, t, n);
}
var xu = class {
};
var Yr = class {
};
var as = class {
  resolveComponentFactory(t) {
    throw new v(917, false);
  }
};
var Kr = class {
  static NULL = new as();
};
var st = class {
};
var Au = (() => {
  class e12 {
    static \u0275prov = _({ token: e12, providedIn: "root", factory: () => null });
  }
  return e12;
})();
var br = {};
var cs = class {
  injector;
  parentInjector;
  constructor(t, n) {
    this.injector = t, this.parentInjector = n;
  }
  get(t, n, r) {
    let o = this.injector.get(t, br, r);
    return o !== br || n === br ? o : this.parentInjector.get(t, n, r);
  }
};
function xr(e12, t, n) {
  let r = n ? e12.styles : null, o = n ? e12.classes : null, i = 0;
  if (t !== null)
    for (let s = 0; s < t.length; s++) {
      let a = t[s];
      if (typeof a == "number")
        i = a;
      else if (i == 1)
        o = Jo(o, a);
      else if (i == 2) {
        let c = a, l = t[++s];
        r = Jo(r, c + ": " + l + ";");
      }
    }
  n ? e12.styles = r : e12.stylesWithoutHost = r, n ? e12.classes = o : e12.classesWithoutHost = o;
}
function Ru(e12, t = 0) {
  let n = M();
  if (n === null)
    return w(e12, t);
  let r = pe();
  return Pl(r, n, W(e12), t);
}
function _h(e12, t, n, r, o) {
  let i = r === null ? null : { "": -1 }, s = o(e12, n);
  if (s !== null) {
    let a = s, c = null, l = null;
    for (let u of s)
      if (u.resolveHostDirectives !== null) {
        [a, c, l] = u.resolveHostDirectives(s);
        break;
      }
    xh(e12, t, n, a, i, c, l);
  }
  i !== null && r !== null && Sh(n, r, i);
}
function Sh(e12, t, n) {
  let r = e12.localNames = [];
  for (let o = 0; o < t.length; o += 2) {
    let i = n[t[o + 1]];
    if (i == null)
      throw new v(-301, false);
    r.push(t[o], i);
  }
}
function Nh(e12, t, n) {
  t.componentOffset = n, (e12.components ??= []).push(t.index);
}
function xh(e12, t, n, r, o, i, s) {
  let a = r.length, c = null;
  for (let f = 0; f < a; f++) {
    let p = r[f];
    c === null && Ct(p) && (c = p, Nh(e12, n, f)), Af(Al(n, t), e12, p.type);
  }
  Lh(n, e12.data.length, a), c?.viewProvidersResolver && c.viewProvidersResolver(c);
  for (let f = 0; f < a; f++) {
    let p = r[f];
    p.providersResolver && p.providersResolver(p);
  }
  let l = false, u = false, d = au(e12, t, a, null);
  a > 0 && (n.directiveToIndex = /* @__PURE__ */ new Map());
  for (let f = 0; f < a; f++) {
    let p = r[f];
    if (n.mergedAttrs = Fr(n.mergedAttrs, p.hostAttrs), Rh(e12, n, t, d, p), Ph(d, p, o), s !== null && s.has(p)) {
      let [k, P] = s.get(p);
      n.directiveToIndex.set(p.type, [d, k + n.directiveStart, P + n.directiveStart]);
    } else
      (i === null || !i.has(p)) && n.directiveToIndex.set(p.type, d);
    p.contentQueries !== null && (n.flags |= 4), (p.hostBindings !== null || p.hostAttrs !== null || p.hostVars !== 0) && (n.flags |= 64);
    let h = p.type.prototype;
    !l && (h.ngOnChanges || h.ngOnInit || h.ngDoCheck) && ((e12.preOrderHooks ??= []).push(n.index), l = true), !u && (h.ngOnChanges || h.ngDoCheck) && ((e12.preOrderCheckHooks ??= []).push(n.index), u = true), d++;
  }
  Ah(e12, n, i);
}
function Ah(e12, t, n) {
  for (let r = t.directiveStart; r < t.directiveEnd; r++) {
    let o = e12.data[r];
    if (n === null || !n.has(o))
      fl(0, t, o, r), fl(1, t, o, r), hl(t, r, false);
    else {
      let i = n.get(o);
      pl(0, t, i, r), pl(1, t, i, r), hl(t, r, true);
    }
  }
}
function fl(e12, t, n, r) {
  let o = e12 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s;
      e12 === 0 ? s = t.inputs ??= {} : s = t.outputs ??= {}, s[i] ??= [], s[i].push(r), Ou(t, i);
    }
}
function pl(e12, t, n, r) {
  let o = e12 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s = o[i], a;
      e12 === 0 ? a = t.hostDirectiveInputs ??= {} : a = t.hostDirectiveOutputs ??= {}, a[s] ??= [], a[s].push(r, i), Ou(t, s);
    }
}
function Ou(e12, t) {
  t === "class" ? e12.flags |= 8 : t === "style" && (e12.flags |= 16);
}
function hl(e12, t, n) {
  let { attrs: r, inputs: o, hostDirectiveInputs: i } = e12;
  if (r === null || !n && o === null || n && i === null || vp(e12)) {
    e12.initialInputs ??= [], e12.initialInputs.push(null);
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
  e12.initialInputs ??= [], e12.initialInputs.push(s);
}
function Rh(e12, t, n, r, o) {
  e12.data[r] = o;
  let i = o.factory || (o.factory = vt(o.type, true)), s = new sn(i, Ct(o), Ru, null);
  e12.blueprint[r] = s, n[r] = s, Oh(e12, t, r, au(e12, n, o.hostVars, Se), o);
}
function Oh(e12, t, n, r, o) {
  let i = o.hostBindings;
  if (i) {
    let s = e12.hostBindingOpCodes;
    s === null && (s = e12.hostBindingOpCodes = []);
    let a = ~t.index;
    kh(s) != a && s.push(a), s.push(n, r, i);
  }
}
function kh(e12) {
  let t = e12.length;
  for (; t > 0; ) {
    let n = e12[--t];
    if (typeof n == "number" && n < 0)
      return n;
  }
  return 0;
}
function Ph(e12, t, n) {
  if (n) {
    if (t.exportAs)
      for (let r = 0; r < t.exportAs.length; r++)
        n[t.exportAs[r]] = e12;
    Ct(t) && (n[""] = e12);
  }
}
function Lh(e12, t, n) {
  e12.flags |= 1, e12.directiveStart = t, e12.directiveEnd = t + n, e12.providerIndexes = t;
}
function Fh(e12, t, n, r, o, i, s, a) {
  let c = t[m], l = c.consts, u = fe(l, s), d = Qr(c, e12, n, r, u);
  return i && _h(c, t, d, fe(l, a), o), d.mergedAttrs = Fr(d.mergedAttrs, d.attrs), d.attrs !== null && xr(d, d.attrs, false), d.mergedAttrs !== null && xr(d, d.mergedAttrs, true), c.queries !== null && c.queries.elementStart(c, d), d;
}
function jh(e12, t) {
  bf(e12, t), mi(t) && e12.queries.elementEnd(t);
}
function Hh(e12, t, n, r, o, i) {
  let s = t.consts, a = fe(s, o), c = Qr(t, e12, n, r, a);
  if (c.mergedAttrs = Fr(c.mergedAttrs, c.attrs), i != null) {
    let l = fe(s, i);
    c.localNames = [];
    for (let u = 0; u < l.length; u += 2)
      c.localNames.push(l[u], -1);
  }
  return c.attrs !== null && xr(c, c.attrs, false), c.mergedAttrs !== null && xr(c, c.mergedAttrs, true), t.queries !== null && t.queries.elementStart(t, c), c;
}
function yn(e12, t, n) {
  if (n === Se)
    return false;
  let r = e12[t];
  return Object.is(r, n) ? false : (e12[t] = n, true);
}
function Vh(e12, t, n) {
  return function r(o) {
    let i = r.__ngNativeEl__;
    i !== void 0 && Uf(o, i);
    let s = bt(e12) ? be(e12.index, t) : t;
    Gs(s, 5);
    let a = t[x], c = gl(t, a, n, o), l = r.__ngNextListenerFn__;
    for (; l; )
      c = gl(t, a, l, o) && c, l = l.__ngNextListenerFn__;
    return c;
  };
}
function gl(e12, t, n, r) {
  let o = g(null);
  try {
    return T(b.OutputStart, t, n), n(r) !== false;
  } catch (i) {
    return th(e12, i), false;
  } finally {
    T(b.OutputEnd, t, n), g(o);
  }
}
function Bh(e12, t, n, r, o, i, s, a) {
  let c = yi(e12), l = false, u = null;
  if (!r && c && (u = Uh(t, n, i, e12.index)), u !== null) {
    let d = u.__ngLastListenerFn__ || u;
    d.__ngNextListenerFn__ = s, u.__ngLastListenerFn__ = s, l = true;
  } else {
    let d = de(e12, n), f = r ? r(d) : d;
    Wf(n, f, i, a), r || (a.__ngNativeEl__ = d);
    let p = o.listen(f, i, a);
    if (!$h(i)) {
      let h = r ? (k) => r(ee(k[e12.index])) : e12.index;
      zh(h, t, n, i, a, p, false);
    }
  }
  return l;
}
function $h(e12) {
  return e12.startsWith("animation") || e12.startsWith("transition");
}
function Uh(e12, t, n, r) {
  let o = e12.cleanup;
  if (o != null)
    for (let i = 0; i < o.length - 1; i += 2) {
      let s = o[i];
      if (s === n && o[i + 1] === r) {
        let a = t[Dt], c = o[i + 2];
        return a && a.length > c ? a[c] : null;
      }
      typeof s == "string" && (i += 2);
    }
  return null;
}
function zh(e12, t, n, r, o, i, s) {
  let a = t.firstCreatePass ? bi(t) : null, c = wi(n), l = c.length;
  c.push(o, i), a && a.push(r, e12, l, (l + 1) * (s ? -1 : 1));
}
var ls = Symbol("BINDING");
function Wh(e12) {
  return e12.debugInfo?.className || e12.type.name || null;
}
var us = class extends Kr {
  ngModule;
  constructor(t) {
    super(), this.ngModule = t;
  }
  resolveComponentFactory(t) {
    let n = Ye(t);
    return new dn(n, this.ngModule);
  }
};
function Gh(e12) {
  return Object.keys(e12).map((t) => {
    let [n, r, o] = e12[t], i = { propName: n, templateName: t, isSignal: (r & zr.SignalBased) !== 0 };
    return o && (i.transform = o), i;
  });
}
function qh(e12) {
  return Object.keys(e12).map((t) => ({ propName: e12[t], templateName: t }));
}
function Zh(e12, t, n) {
  let r = t instanceof Q ? t : t?.injector;
  return r && e12.getStandaloneInjector !== null && (r = e12.getStandaloneInjector(r) || r), r ? new cs(n, r) : n;
}
function Qh(e12) {
  let t = e12.get(st, null);
  if (t === null)
    throw new v(407, false);
  let n = e12.get(Au, null), r = e12.get(Ze, null), o = e12.get(Lt, null, { optional: true });
  return { rendererFactory: t, sanitizer: n, changeDetectionScheduler: r, ngReflect: false, tracingService: o };
}
function Yh(e12, t) {
  let n = ku(e12);
  return nu(t, n, n === "svg" ? uc : n === "math" ? dc : null);
}
function ku(e12) {
  return (e12.selectors[0][0] || "div").toLowerCase();
}
var dn = class extends Yr {
  componentDef;
  ngModule;
  selector;
  componentType;
  ngContentSelectors;
  isBoundToModule;
  cachedInputs = null;
  cachedOutputs = null;
  get inputs() {
    return this.cachedInputs ??= Gh(this.componentDef.inputs), this.cachedInputs;
  }
  get outputs() {
    return this.cachedOutputs ??= qh(this.componentDef.outputs), this.cachedOutputs;
  }
  constructor(t, n) {
    super(), this.componentDef = t, this.ngModule = n, this.componentType = t.type, this.selector = Ip(t.selectors), this.ngContentSelectors = t.ngContentSelectors ?? [], this.isBoundToModule = !!n;
  }
  create(t, n, r, o, i, s) {
    T(b.DynamicComponentStart);
    let a = g(null);
    try {
      let c = this.componentDef, l = Zh(c, o || this.ngModule, t), u = Qh(l), d = u.tracingService;
      return d && d.componentCreate ? d.componentCreate(Wh(c), () => this.createComponentRef(u, l, n, r, i, s)) : this.createComponentRef(u, l, n, r, i, s);
    } finally {
      g(a);
    }
  }
  createComponentRef(t, n, r, o, i, s) {
    let a = this.componentDef, c = Kh(o, a, s, i), l = t.rendererFactory.createRenderer(null, a), u = o ? Wp(l, o, a.encapsulation, n) : Yh(a, l), d = s?.some(ml) || i?.some((h) => typeof h != "function" && h.bindings.some(ml)), f = js(null, c, null, 512 | su(a), null, null, t, l, n, null, Zl(u, n, true));
    f[F] = u, ur(f);
    let p = null;
    try {
      let h = Fh(F, f, 2, "#host", () => c.directiveRegistry, true, 0);
      iu(l, u, h), Rt(u, f), zp(c, f, h), qf(c, h, f), jh(c, h), r !== void 0 && Xh(h, this.ngContentSelectors, r), p = be(h.index, f), f[x] = p[x], Ws(c, f, null);
    } catch (h) {
      throw p !== null && zi(p), zi(f), h;
    } finally {
      T(b.DynamicComponentEnd), dr();
    }
    return new Ar(this.componentType, f, !!d);
  }
};
function Kh(e12, t, n, r) {
  let o = e12 ? ["ng-version", "21.2.11"] : Dp(t.selectors[0]), i = null, s = null, a = 0;
  if (n)
    for (let u of n)
      a += u[ls].requiredVars, u.create && (u.targetIdx = 0, (i ??= []).push(u)), u.update && (u.targetIdx = 0, (s ??= []).push(u));
  if (r)
    for (let u = 0; u < r.length; u++) {
      let d = r[u];
      if (typeof d != "function")
        for (let f of d.bindings) {
          a += f[ls].requiredVars;
          let p = u + 1;
          f.create && (f.targetIdx = p, (i ??= []).push(f)), f.update && (f.targetIdx = p, (s ??= []).push(f));
        }
    }
  let c = [t];
  if (r)
    for (let u of r) {
      let d = typeof u == "function" ? u : u.type, f = ri(d);
      c.push(f);
    }
  return Fs(0, null, Jh(i, s), 1, a, c, null, null, null, [o], null);
}
function Jh(e12, t) {
  return !e12 && !t ? null : (n) => {
    if (n & 1 && e12)
      for (let r of e12)
        r.create();
    if (n & 2 && t)
      for (let r of t)
        r.update();
  };
}
function ml(e12) {
  let t = e12[ls].kind;
  return t === "input" || t === "twoWay";
}
var Ar = class extends xu {
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
    super(), this._rootLView = n, this._hasInputBindings = r, this._tNode = ir(n[m], F), this.location = Pt(this._tNode, n), this.instance = be(this._tNode.index, n)[x], this.hostView = this.changeDetectorRef = new Ot(n, void 0), this.componentType = t;
  }
  setInput(t, n) {
    this._hasInputBindings;
    let r = this._tNode;
    if (this.previousInputValues ??= /* @__PURE__ */ new Map(), this.previousInputValues.has(t) && Object.is(this.previousInputValues.get(t), n))
      return;
    let o = this._rootLView, i = nh(r, o[m], o, t, n);
    this.previousInputValues.set(t, n);
    let s = be(r.index, o);
    Gs(s, 1);
  }
  get injector() {
    return new ot(this._tNode, this._rootLView);
  }
  destroy() {
    this.hostView.destroy();
  }
  onDestroy(t) {
    this.hostView.onDestroy(t);
  }
};
function Xh(e12, t, n) {
  let r = e12.projection = [];
  for (let o = 0; o < t.length; o++) {
    let i = n[o];
    r.push(i != null && i.length ? Array.from(i) : null);
  }
}
var Jr = /* @__PURE__ */ (() => {
  class e12 {
    static __NG_ELEMENT_ID__ = eg;
  }
  return e12;
})();
function eg() {
  let e12 = pe();
  return Pu(e12, M());
}
var ds = class e4 extends Jr {
  _lContainer;
  _hostTNode;
  _hostLView;
  constructor(t, n, r) {
    super(), this._lContainer = t, this._hostTNode = n, this._hostLView = r;
  }
  get element() {
    return Pt(this._hostTNode, this._hostLView);
  }
  get injector() {
    return new ot(this._hostTNode, this._hostLView);
  }
  get parentInjector() {
    let t = _s(this._hostTNode, this._hostLView);
    if (Sl(t)) {
      let n = Mr(t, this._hostLView), r = Tr(t), o = n[m].data[r + 8];
      return new ot(o, n);
    } else
      return new ot(null, this._hostLView);
  }
  clear() {
    for (; this.length > 0; )
      this.remove(this.length - 1);
  }
  get(t) {
    let n = yl(this._lContainer);
    return n !== null && n[t] || null;
  }
  get length() {
    return this._lContainer.length - S;
  }
  createEmbeddedView(t, n, r) {
    let o, i;
    typeof r == "number" ? o = r : r != null && (o = r.index, i = r.injector);
    let s = ss(this._lContainer, t.ssrId), a = t.createEmbeddedViewImpl(n || {}, i, s);
    return this.insertImpl(a, o, an(this._hostTNode, s)), a;
  }
  createComponent(t, n, r, o, i, s, a) {
    let c = t && !yf(t), l;
    if (c)
      l = n;
    else {
      let P = n || {};
      l = P.index, r = P.injector, o = P.projectableNodes, i = P.environmentInjector || P.ngModuleRef, s = P.directives, a = P.bindings;
    }
    let u = c ? t : new dn(Ye(t)), d = r || this.parentInjector;
    if (!i && u.ngModule == null) {
      let ct = (c ? d : this.parentInjector).get(Q, null);
      ct && (i = ct);
    }
    let f = Ye(u.componentType ?? {}), p = ss(this._lContainer, f?.id ?? null), h = p?.firstChild ?? null, k = u.create(d, o, h, i, s, a);
    return this.insertImpl(k.hostView, l, an(this._hostTNode, p)), k;
  }
  insert(t, n) {
    return this.insertImpl(t, n, true);
  }
  insertImpl(t, n, r) {
    let o = t._lView;
    if (pc(o)) {
      let a = this.indexOf(t);
      if (a !== -1)
        this.detach(a);
      else {
        let c = o[R], l = new e4(c, c[J], c[R]);
        l.detach(l.indexOf(t));
      }
    }
    let i = this._adjustIndex(n), s = this._lContainer;
    return Zr(s, o, i, r), t.attachToViewContainerRef(), ci(Hi(s), i, t), t;
  }
  move(t, n) {
    return this.insert(t, n);
  }
  indexOf(t) {
    let n = yl(this._lContainer);
    return n !== null ? n.indexOf(t) : -1;
  }
  remove(t) {
    let n = this._adjustIndex(t, -1), r = ln(this._lContainer, n);
    r && (Zt(Hi(this._lContainer), n), Wr(r[m], r));
  }
  detach(t) {
    let n = this._adjustIndex(t, -1), r = ln(this._lContainer, n);
    return r && Zt(Hi(this._lContainer), n) != null ? new Ot(r) : null;
  }
  _adjustIndex(t, n = 0) {
    return t ?? this.length + n;
  }
};
function yl(e12) {
  return e12[Jt];
}
function Hi(e12) {
  return e12[Jt] || (e12[Jt] = []);
}
function Pu(e12, t) {
  let n, r = t[e12.index];
  return re(r) ? n = r : (n = Tu(r, t, null, e12), t[e12.index] = n, Hs(t, n)), ng(n, t, e12, r), new ds(n, e12, t);
}
function tg(e12, t) {
  let n = e12[O], r = n.createComment(""), o = de(t, e12), i = n.parentNode(o);
  return Nr(n, i, r, n.nextSibling(o), false), r;
}
var ng = ig;
var rg = () => false;
function og(e12, t, n) {
  return rg(e12, t, n);
}
function ig(e12, t, n, r) {
  if (e12[Pe])
    return;
  let o;
  n.type & 8 ? o = ee(r) : o = tg(t, n), e12[Pe] = o;
}
var fs = class e5 {
  queryList;
  matches = null;
  constructor(t) {
    this.queryList = t;
  }
  clone() {
    return new e5(this.queryList);
  }
  setDirty() {
    this.queryList.setDirty();
  }
};
var ps = class e6 {
  queries;
  constructor(t = []) {
    this.queries = t;
  }
  createEmbeddedView(t) {
    let n = t.queries;
    if (n !== null) {
      let r = t.contentQueries !== null ? t.contentQueries[0] : n.length, o = [];
      for (let i = 0; i < r; i++) {
        let s = n.getByIndex(i), a = this.queries[s.indexInDeclarationView];
        o.push(a.clone());
      }
      return new e6(o);
    }
    return null;
  }
  insertView(t) {
    this.dirtyQueriesWithMatches(t);
  }
  detachView(t) {
    this.dirtyQueriesWithMatches(t);
  }
  finishViewCreation(t) {
    this.dirtyQueriesWithMatches(t);
  }
  dirtyQueriesWithMatches(t) {
    for (let n = 0; n < this.queries.length; n++)
      Zs(t, n).matches !== null && this.queries[n].setDirty();
  }
};
var hs = class {
  flags;
  read;
  predicate;
  constructor(t, n, r = null) {
    this.flags = n, this.read = r, typeof t == "string" ? this.predicate = pg(t) : this.predicate = t;
  }
};
var gs = class e7 {
  queries;
  constructor(t = []) {
    this.queries = t;
  }
  elementStart(t, n) {
    for (let r = 0; r < this.queries.length; r++)
      this.queries[r].elementStart(t, n);
  }
  elementEnd(t) {
    for (let n = 0; n < this.queries.length; n++)
      this.queries[n].elementEnd(t);
  }
  embeddedTView(t) {
    let n = null;
    for (let r = 0; r < this.length; r++) {
      let o = n !== null ? n.length : 0, i = this.getByIndex(r).embeddedTView(t, o);
      i && (i.indexInDeclarationView = r, n !== null ? n.push(i) : n = [i]);
    }
    return n !== null ? new e7(n) : null;
  }
  template(t, n) {
    for (let r = 0; r < this.queries.length; r++)
      this.queries[r].template(t, n);
  }
  getByIndex(t) {
    return this.queries[t];
  }
  get length() {
    return this.queries.length;
  }
  track(t) {
    this.queries.push(t);
  }
};
var ms = class e8 {
  metadata;
  matches = null;
  indexInDeclarationView = -1;
  crossesNgTemplate = false;
  _declarationNodeIndex;
  _appliesToNextNode = true;
  constructor(t, n = -1) {
    this.metadata = t, this._declarationNodeIndex = n;
  }
  elementStart(t, n) {
    this.isApplyingToNode(n) && this.matchTNode(t, n);
  }
  elementEnd(t) {
    this._declarationNodeIndex === t.index && (this._appliesToNextNode = false);
  }
  template(t, n) {
    this.elementStart(t, n);
  }
  embeddedTView(t, n) {
    return this.isApplyingToNode(t) ? (this.crossesNgTemplate = true, this.addMatch(-t.index, n), new e8(this.metadata)) : null;
  }
  isApplyingToNode(t) {
    if (this._appliesToNextNode && (this.metadata.flags & 1) !== 1) {
      let n = this._declarationNodeIndex, r = t.parent;
      for (; r !== null && r.type & 8 && r.index !== n; )
        r = r.parent;
      return n === (r !== null ? r.index : -1);
    }
    return this._appliesToNextNode;
  }
  matchTNode(t, n) {
    let r = this.metadata.predicate;
    if (Array.isArray(r))
      for (let o = 0; o < r.length; o++) {
        let i = r[o];
        this.matchTNodeWithReadOption(t, n, sg(n, i)), this.matchTNodeWithReadOption(t, n, wr(n, t, i, false, false));
      }
    else
      r === un ? n.type & 4 && this.matchTNodeWithReadOption(t, n, -1) : this.matchTNodeWithReadOption(t, n, wr(n, t, r, false, false));
  }
  matchTNodeWithReadOption(t, n, r) {
    if (r !== null) {
      let o = this.metadata.read;
      if (o !== null)
        if (o === hn || o === Jr || o === un && n.type & 4)
          this.addMatch(n.index, -2);
        else {
          let i = wr(n, t, o, false, false);
          i !== null && this.addMatch(n.index, i);
        }
      else
        this.addMatch(n.index, r);
    }
  }
  addMatch(t, n) {
    this.matches === null ? this.matches = [t, n] : this.matches.push(t, n);
  }
};
function sg(e12, t) {
  let n = e12.localNames;
  if (n !== null) {
    for (let r = 0; r < n.length; r += 2)
      if (n[r] === t)
        return n[r + 1];
  }
  return null;
}
function ag(e12, t) {
  return e12.type & 11 ? Pt(e12, t) : e12.type & 4 ? qs(e12, t) : null;
}
function cg(e12, t, n, r) {
  return n === -1 ? ag(t, e12) : n === -2 ? lg(e12, t, r) : _r(e12, e12[m], n, t);
}
function lg(e12, t, n) {
  if (n === hn)
    return Pt(t, e12);
  if (n === un)
    return qs(t, e12);
  if (n === Jr)
    return Pu(t, e12);
}
function Lu(e12, t, n, r) {
  let o = t[ue].queries[r];
  if (o.matches === null) {
    let i = e12.data, s = n.matches, a = [];
    for (let c = 0; s !== null && c < s.length; c += 2) {
      let l = s[c];
      if (l < 0)
        a.push(null);
      else {
        let u = i[l];
        a.push(cg(t, u, s[c + 1], n.metadata.read));
      }
    }
    o.matches = a;
  }
  return o.matches;
}
function ys(e12, t, n, r) {
  let o = e12.queries.getByIndex(n), i = o.matches;
  if (i !== null) {
    let s = Lu(e12, t, o, n);
    for (let a = 0; a < i.length; a += 2) {
      let c = i[a];
      if (c > 0)
        r.push(s[a / 2]);
      else {
        let l = i[a + 1], u = t[-c];
        for (let d = S; d < u.length; d++) {
          let f = u[d];
          f[Oe] === f[R] && ys(f[m], f, l, r);
        }
        if (u[tt] !== null) {
          let d = u[tt];
          for (let f = 0; f < d.length; f++) {
            let p = d[f];
            ys(p[m], p, l, r);
          }
        }
      }
    }
  }
  return r;
}
function ug(e12, t) {
  return e12[ue].queries[t].queryList;
}
function dg(e12, t, n) {
  let r = new Sr((n & 4) === 4);
  return mc(e12, t, r, r.destroy), (t[ue] ??= new ps()).queries.push(new fs(r)) - 1;
}
function fg(e12, t, n) {
  let r = oe();
  return r.firstCreatePass && (hg(r, new hs(e12, t, n), -1), (t & 2) === 2 && (r.staticViewQueries = true)), dg(r, M(), t);
}
function pg(e12) {
  return e12.split(",").map((t) => t.trim());
}
function hg(e12, t, n) {
  e12.queries === null && (e12.queries = new gs()), e12.queries.track(new ms(t, n));
}
function Zs(e12, t) {
  return e12.queries.getByIndex(t);
}
function gg(e12, t) {
  let n = e12[m], r = Zs(n, t);
  return r.crossesNgTemplate ? ys(n, e12, t, []) : Lu(n, e12, r, t);
}
var Rr = class {
};
var fn = class extends Rr {
  injector;
  componentFactoryResolver = new us(this);
  instance = null;
  constructor(t) {
    super();
    let n = new qe([...t.providers, { provide: Rr, useValue: this }, { provide: Kr, useValue: this.componentFactoryResolver }], t.parent || Kt(), t.debugName, /* @__PURE__ */ new Set(["environment"]));
    this.injector = n, t.runEnvironmentInitializers && n.resolveInjectorInitializers();
  }
  destroy() {
    this.injector.destroy();
  }
  onDestroy(t) {
    this.injector.onDestroy(t);
  }
};
function Fu(e12, t, n = null) {
  return new fn({ providers: e12, parent: t, debugName: n, runEnvironmentInitializers: true }).injector;
}
var mg = (() => {
  class e12 {
    _injector;
    cachedInjectors = /* @__PURE__ */ new Map();
    constructor(n) {
      this._injector = n;
    }
    getOrCreateStandaloneInjector(n) {
      if (!n.standalone)
        return null;
      if (!this.cachedInjectors.has(n)) {
        let r = di(false, n.type), o = r.length > 0 ? Fu([r], this._injector, "") : null;
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
    static \u0275prov = _({ token: e12, providedIn: "environment", factory: () => new e12(w(Q)) });
  }
  return e12;
})();
function Qs(e12) {
  return bl(() => {
    let t = Ig(e12), n = A(N({}, t), { decls: e12.decls, vars: e12.vars, template: e12.template, consts: e12.consts || null, ngContentSelectors: e12.ngContentSelectors, onPush: e12.changeDetection === Ss.OnPush, directiveDefs: null, pipeDefs: null, dependencies: t.standalone && e12.dependencies || null, getStandaloneInjector: t.standalone ? (o) => o.get(mg).getOrCreateStandaloneInjector(n) : null, getExternalStyles: null, signals: e12.signals ?? false, data: e12.data || {}, encapsulation: e12.encapsulation || ie.Emulated, styles: e12.styles || Ne, _: null, schemas: e12.schemas || null, tView: null, id: "" });
    t.standalone && Ft("NgStandalone"), Dg(n);
    let r = e12.dependencies;
    return n.directiveDefs = vl(r, yg), n.pipeDefs = vl(r, Qa), n.id = wg(n), n;
  });
}
function yg(e12) {
  return Ye(e12) || ri(e12);
}
function vg(e12, t) {
  if (e12 == null)
    return Ke;
  let n = {};
  for (let r in e12)
    if (e12.hasOwnProperty(r)) {
      let o = e12[r], i, s, a, c;
      Array.isArray(o) ? (a = o[0], i = o[1], s = o[2] ?? i, c = o[3] || null) : (i = o, s = o, a = zr.None, c = null), n[i] = [r, a, c], t[i] = s;
    }
  return n;
}
function Eg(e12) {
  if (e12 == null)
    return Ke;
  let t = {};
  for (let n in e12)
    e12.hasOwnProperty(n) && (t[e12[n]] = n);
  return t;
}
function Ig(e12) {
  let t = {};
  return { type: e12.type, providersResolver: null, viewProvidersResolver: null, factory: null, hostBindings: e12.hostBindings || null, hostVars: e12.hostVars || 0, hostAttrs: e12.hostAttrs || null, contentQueries: e12.contentQueries || null, declaredInputs: t, inputConfig: e12.inputs || Ke, exportAs: e12.exportAs || null, standalone: e12.standalone ?? true, signals: e12.signals === true, selectors: e12.selectors || Ne, viewQuery: e12.viewQuery || null, features: e12.features || null, setInput: null, resolveHostDirectives: null, hostDirectives: null, controlDef: null, inputs: vg(e12.inputs, t), outputs: Eg(e12.outputs), debugInfo: null };
}
function Dg(e12) {
  e12.features?.forEach((t) => t(e12));
}
function vl(e12, t) {
  return e12 ? () => {
    let n = typeof e12 == "function" ? e12() : e12, r = [];
    for (let o of n) {
      let i = t(o);
      i !== null && r.push(i);
    }
    return r;
  } : null;
}
function wg(e12) {
  let t = 0, n = typeof e12.consts == "function" ? "" : e12.consts, r = [e12.selectors, e12.ngContentSelectors, e12.hostVars, e12.hostAttrs, n, e12.vars, e12.decls, e12.encapsulation, e12.standalone, e12.signals, e12.exportAs, JSON.stringify(e12.inputs), JSON.stringify(e12.outputs), Object.getOwnPropertyNames(e12.type.prototype), !!e12.contentQueries, !!e12.viewQuery];
  for (let i of r.join("|"))
    t = Math.imul(31, t) + i.charCodeAt(0) << 0;
  return t += 2147483648, "c" + t;
}
function bg(e12, t, n, r, o, i, s, a) {
  if (n.firstCreatePass) {
    e12.mergedAttrs = Fr(e12.mergedAttrs, e12.attrs);
    let u = e12.tView = Fs(2, e12, o, i, s, n.directiveRegistry, n.pipeRegistry, null, n.schemas, n.consts, null);
    n.queries !== null && (n.queries.template(n, e12), u.queries = n.queries.embeddedTView(e12));
  }
  a && (e12.flags |= a), _t(e12, false);
  let c = Cg(n, t, e12, r);
  fr() && Us(n, t, c, e12), Rt(c, t);
  let l = Tu(c, t, c, e12);
  t[r + F] = l, Hs(t, l), og(l, e12, t);
}
function Or(e12, t, n, r, o, i, s, a, c, l, u) {
  let d = n + F, f;
  if (t.firstCreatePass) {
    if (f = Qr(t, d, 4, s || null, a || null), l != null) {
      let p = fe(t.consts, l);
      f.localNames = [];
      for (let h = 0; h < p.length; h += 2)
        f.localNames.push(p[h], -1);
    }
  } else
    f = t.data[d];
  return bg(f, e12, t, n, r, o, i, c), l != null && gu(e12, f, u), f;
}
var Cg = Tg;
function Tg(e12, t, n, r) {
  return pr(true), t[O].createComment("");
}
var Ys = new D("");
function Ks(e12) {
  return !!e12 && typeof e12.then == "function";
}
function ju(e12) {
  return !!e12 && typeof e12.subscribe == "function";
}
var Hu = new D("");
var Js = (() => {
  class e12 {
    resolve;
    reject;
    initialized = false;
    done = false;
    donePromise = new Promise((n, r) => {
      this.resolve = n, this.reject = r;
    });
    appInits = E(Hu, { optional: true }) ?? [];
    injector = E(ce);
    constructor() {
    }
    runInitializers() {
      if (this.initialized)
        return;
      let n = [];
      for (let o of this.appInits) {
        let i = nr(this.injector, o);
        if (Ks(i))
          n.push(i);
        else if (ju(i)) {
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
      return new (r || e12)();
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac, providedIn: "root" });
  }
  return e12;
})();
var Vu = new D("");
function Bu() {
  To(() => {
    let e12 = "";
    throw new v(600, e12);
  });
}
function $u(e12) {
  return e12.isBoundToModule;
}
var Mg = 10;
var vn = (() => {
  class e12 {
    _runningTick = false;
    _destroyed = false;
    _destroyListeners = [];
    _views = [];
    internalErrorHandler = E(rt);
    afterRenderManager = E(lu);
    zonelessEnabled = E(tn);
    rootEffectScheduler = E(gr);
    dirtyFlags = 0;
    tracingSnapshot = null;
    allTestViews = /* @__PURE__ */ new Set();
    autoDetectTestViews = /* @__PURE__ */ new Set();
    includeAllTestViews = false;
    afterTick = new ye();
    get allViews() {
      return [...(this.includeAllTestViews ? this.allTestViews : this.autoDetectTestViews).keys(), ...this._views];
    }
    get destroyed() {
      return this._destroyed;
    }
    componentTypes = [];
    components = [];
    internalPendingTask = E(Nt);
    get isStable() {
      return this.internalPendingTask.hasPendingTasksObservable.pipe(Fo((n) => !n));
    }
    constructor() {
      E(Lt, { optional: true });
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
    _injector = E(Q);
    _rendererFactory = null;
    get injector() {
      return this._injector;
    }
    bootstrap(n, r) {
      return this.bootstrapImpl(n, r);
    }
    bootstrapImpl(n, r, o = ce.NULL) {
      return this._injector.get(Y).run(() => {
        T(b.BootstrapComponentStart);
        let s = n instanceof Yr;
        if (!this._injector.get(Js).done) {
          let h = "";
          throw new v(405, h);
        }
        let c;
        s ? c = n : c = this._injector.get(Kr).resolveComponentFactory(n), this.componentTypes.push(c.componentType);
        let l = $u(c) ? void 0 : this._injector.get(Rr), u = r || c.selector, d = c.create(o, [], u, l), f = d.location.nativeElement, p = d.injector.get(Ys, null);
        return p?.registerApplication(f), d.onDestroy(() => {
          this.detachView(d.hostView), on(this.components, d), p?.unregisterApplication(f);
        }), this._loadComponent(d), T(b.BootstrapComponentEnd, d), d;
      });
    }
    tick() {
      this.zonelessEnabled || (this.dirtyFlags |= 1), this._tick();
    }
    _tick() {
      T(b.ChangeDetectionStart), this.tracingSnapshot !== null ? this.tracingSnapshot.run(Bs.CHANGE_DETECTION, this.tickImpl) : this.tickImpl();
    }
    tickImpl = () => {
      if (this._runningTick)
        throw T(b.ChangeDetectionEnd), new v(101, false);
      let n = g(null);
      try {
        this._runningTick = true, this.synchronize();
      } finally {
        this._runningTick = false, this.tracingSnapshot?.dispose(), this.tracingSnapshot = null, g(n), this.afterTick.next(), T(b.ChangeDetectionEnd);
      }
    };
    synchronize() {
      this._rendererFactory === null && !this._injector.destroyed && (this._rendererFactory = this._injector.get(st, null, { optional: true }));
      let n = 0;
      for (; this.dirtyFlags !== 0 && n++ < Mg; ) {
        T(b.ChangeDetectionSyncStart);
        try {
          this.synchronizeOnce();
        } finally {
          T(b.ChangeDetectionSyncEnd);
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
          if (!r && !Xt(o))
            continue;
          let i = r && !this.zonelessEnabled ? 0 : 1;
          Du(o, i), n = true;
        }
        if (this.dirtyFlags &= -5, this.syncDirtyFlagsWithViews(), this.dirtyFlags & 23)
          return;
      }
      n || (this._rendererFactory?.begin?.(), this._rendererFactory?.end?.()), this.dirtyFlags & 8 && (this.dirtyFlags &= -9, this.afterRenderManager.execute()), this.syncDirtyFlagsWithViews();
    }
    syncDirtyFlagsWithViews() {
      if (this.allViews.some(({ _lView: n }) => Xt(n))) {
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
      on(this._views, r), r.detachFromAppRef();
    }
    _loadComponent(n) {
      this.attachView(n.hostView);
      try {
        this.tick();
      } catch (o) {
        this.internalErrorHandler(o);
      }
      this.components.push(n), this._injector.get(Vu, []).forEach((o) => o(n));
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
      return this._destroyListeners.push(n), () => on(this._destroyListeners, n);
    }
    destroy() {
      if (this._destroyed)
        throw new v(406, false);
      let n = this._injector;
      n.destroy && !n.destroyed && n.destroy();
    }
    get viewCount() {
      return this._views.length;
    }
    static \u0275fac = function(r) {
      return new (r || e12)();
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac, providedIn: "root" });
  }
  return e12;
})();
function on(e12, t) {
  let n = e12.indexOf(t);
  n > -1 && e12.splice(n, 1);
}
var vs = class {
  destroy(t) {
  }
  updateValue(t, n) {
  }
  swap(t, n) {
    let r = Math.min(t, n), o = Math.max(t, n), i = this.detach(o);
    if (o - r > 1) {
      let s = this.detach(r);
      this.attach(r, i), this.attach(o, s);
    } else
      this.attach(r, i);
  }
  move(t, n) {
    this.attach(n, this.detach(t));
  }
};
function Vi(e12, t, n, r, o) {
  return e12 === n && Object.is(t, r) ? 1 : Object.is(o(e12, t), o(n, r)) ? -1 : 0;
}
function _g(e12, t, n, r) {
  let o, i, s = 0, a = e12.length - 1, c = void 0;
  if (Array.isArray(t)) {
    g(r);
    let l = t.length - 1;
    for (g(null); s <= a && s <= l; ) {
      let u = e12.at(s), d = t[s], f = Vi(s, u, s, d, n);
      if (f !== 0) {
        f < 0 && e12.updateValue(s, d), s++;
        continue;
      }
      let p = e12.at(a), h = t[l], k = Vi(a, p, l, h, n);
      if (k !== 0) {
        k < 0 && e12.updateValue(a, h), a--, l--;
        continue;
      }
      let P = n(s, u), ct = n(a, p), Ht = n(s, d);
      if (Object.is(Ht, ct)) {
        let po = n(l, h);
        Object.is(po, P) ? (e12.swap(s, a), e12.updateValue(a, h), l--, a--) : e12.move(a, s), e12.updateValue(s, d), s++;
        continue;
      }
      if (o ??= new kr(), i ??= Il(e12, s, a, n), Es(e12, o, s, Ht))
        e12.updateValue(s, d), s++, a++;
      else if (i.has(Ht))
        o.set(P, e12.detach(s)), a--;
      else {
        let po = e12.create(s, t[s]);
        e12.attach(s, po), s++, a++;
      }
    }
    for (; s <= l; )
      El(e12, o, n, s, t[s]), s++;
  } else if (t != null) {
    g(r);
    let l = t[Symbol.iterator]();
    g(null);
    let u = l.next();
    for (; !u.done && s <= a; ) {
      let d = e12.at(s), f = u.value, p = Vi(s, d, s, f, n);
      if (p !== 0)
        p < 0 && e12.updateValue(s, f), s++, u = l.next();
      else {
        o ??= new kr(), i ??= Il(e12, s, a, n);
        let h = n(s, f);
        if (Es(e12, o, s, h))
          e12.updateValue(s, f), s++, a++, u = l.next();
        else if (!i.has(h))
          e12.attach(s, e12.create(s, f)), s++, a++, u = l.next();
        else {
          let k = n(s, d);
          o.set(k, e12.detach(s)), a--;
        }
      }
    }
    for (; !u.done; )
      El(e12, o, n, e12.length, u.value), u = l.next();
  }
  for (; s <= a; )
    e12.destroy(e12.detach(a--));
  o?.forEach((l) => {
    e12.destroy(l);
  });
}
function Es(e12, t, n, r) {
  return t !== void 0 && t.has(r) ? (e12.attach(n, t.get(r)), t.delete(r), true) : false;
}
function El(e12, t, n, r, o) {
  if (Es(e12, t, r, n(r, o)))
    e12.updateValue(r, o);
  else {
    let i = e12.create(r, o);
    e12.attach(r, i);
  }
}
function Il(e12, t, n, r) {
  let o = /* @__PURE__ */ new Set();
  for (let i = t; i <= n; i++)
    o.add(r(i, e12.at(i)));
  return o;
}
var kr = class {
  kvMap = /* @__PURE__ */ new Map();
  _vMap = void 0;
  has(t) {
    return this.kvMap.has(t);
  }
  delete(t) {
    if (!this.has(t))
      return false;
    let n = this.kvMap.get(t);
    return this._vMap !== void 0 && this._vMap.has(n) ? (this.kvMap.set(t, this._vMap.get(n)), this._vMap.delete(n)) : this.kvMap.delete(t), true;
  }
  get(t) {
    return this.kvMap.get(t);
  }
  set(t, n) {
    if (this.kvMap.has(t)) {
      let r = this.kvMap.get(t);
      this._vMap === void 0 && (this._vMap = /* @__PURE__ */ new Map());
      let o = this._vMap;
      for (; o.has(r); )
        r = o.get(r);
      o.set(r, n);
    } else
      this.kvMap.set(t, n);
  }
  forEach(t) {
    for (let [n, r] of this.kvMap)
      if (t(r, n), this._vMap !== void 0) {
        let o = this._vMap;
        for (; o.has(r); )
          r = o.get(r), t(r, n);
      }
  }
};
function Xs(e12, t, n, r, o, i, s, a) {
  Ft("NgControlFlow");
  let c = M(), l = oe(), u = fe(l.consts, i);
  return Or(c, l, e12, t, n, r, o, u, 256, s, a), ea;
}
function ea(e12, t, n, r, o, i, s, a) {
  Ft("NgControlFlow");
  let c = M(), l = oe(), u = fe(l.consts, i);
  return Or(c, l, e12, t, n, r, o, u, 512, s, a), ea;
}
function ta(e12, t) {
  Ft("NgControlFlow");
  let n = M(), r = en(), o = n[r] !== Se ? n[r] : -1, i = o !== -1 ? Pr(n, F + o) : void 0, s = 0;
  if (yn(n, r, e12)) {
    let a = g(null);
    try {
      if (i !== void 0 && _u(i, s), e12 !== -1) {
        let c = F + e12, l = Pr(n, c), u = bs(n[m], c), d = Nu(l, u, n), f = qr(n, u, t, { dehydratedView: d });
        Zr(l, f, s, an(u, d));
      }
    } finally {
      g(a);
    }
  } else if (i !== void 0) {
    let a = Mu(i, s);
    a !== void 0 && (a[x] = t);
  }
}
var Is = class {
  lContainer;
  $implicit;
  $index;
  constructor(t, n, r) {
    this.lContainer = t, this.$implicit = n, this.$index = r;
  }
  get $count() {
    return this.lContainer.length - S;
  }
};
function Xr(e12, t) {
  return t;
}
var Ds = class {
  hasEmptyBlock;
  trackByFn;
  liveCollection;
  constructor(t, n, r) {
    this.hasEmptyBlock = t, this.trackByFn = n, this.liveCollection = r;
  }
};
function eo(e12, t, n, r, o, i, s, a, c, l, u, d, f) {
  Ft("NgControlFlow");
  let p = M(), h = oe(), k = c !== void 0, P = M(), ct = a ? s.bind(P[X][x]) : s, Ht = new Ds(k, ct);
  P[F + e12] = Ht, Or(p, h, e12 + 1, t, n, r, o, fe(h.consts, i), 256), k && Or(p, h, e12 + 2, c, l, u, d, fe(h.consts, f), 512);
}
var ws = class extends vs {
  lContainer;
  hostLView;
  templateTNode;
  operationsCounter = void 0;
  needsIndexUpdate = false;
  constructor(t, n, r) {
    super(), this.lContainer = t, this.hostLView = n, this.templateTNode = r;
  }
  get length() {
    return this.lContainer.length - S;
  }
  at(t) {
    return this.getLView(t)[x].$implicit;
  }
  attach(t, n) {
    let r = n[It];
    this.needsIndexUpdate ||= t !== this.length, Zr(this.lContainer, n, t, an(this.templateTNode, r)), Sg(this.lContainer, t);
  }
  detach(t) {
    return this.needsIndexUpdate ||= t !== this.length - 1, Ng(this.lContainer, t), xg(this.lContainer, t);
  }
  create(t, n) {
    let r = ss(this.lContainer, this.templateTNode.tView.ssrId);
    return qr(this.hostLView, this.templateTNode, new Is(this.lContainer, n, t), { dehydratedView: r });
  }
  destroy(t) {
    Wr(t[m], t);
  }
  updateValue(t, n) {
    this.getLView(t)[x].$implicit = n;
  }
  reset() {
    this.needsIndexUpdate = false;
  }
  updateIndexes() {
    if (this.needsIndexUpdate)
      for (let t = 0; t < this.length; t++)
        this.getLView(t)[x].$index = t;
  }
  getLView(t) {
    return Ag(this.lContainer, t);
  }
};
function to(e12) {
  let t = g(null), n = Fe();
  try {
    let r = M(), o = r[m], i = r[n], s = n + 1, a = Pr(r, s);
    if (i.liveCollection === void 0) {
      let l = bs(o, s);
      i.liveCollection = new ws(a, r, l);
    } else
      i.liveCollection.reset();
    let c = i.liveCollection;
    if (_g(c, e12, i.trackByFn, t), c.updateIndexes(), i.hasEmptyBlock) {
      let l = en(), u = c.length === 0;
      if (yn(r, l, u)) {
        let d = n + 2, f = Pr(r, d);
        if (u) {
          let p = bs(o, d), h = Nu(f, p, r), k = qr(r, p, void 0, { dehydratedView: h });
          Zr(f, k, 0, an(p, h));
        } else
          o.firstUpdatePass && bh(f), _u(f, 0);
      }
    }
  } finally {
    g(t);
  }
}
function Pr(e12, t) {
  return e12[t];
}
function Sg(e12, t) {
  if (e12.length <= S)
    return;
  let n = S + t, r = e12[n], o = r ? r[ke] : void 0;
  if (r && o && o.detachedLeaveAnimationFns && o.detachedLeaveAnimationFns.length > 0) {
    let i = r[De];
    Sp(i, o), it.delete(r[we]), o.detachedLeaveAnimationFns = void 0;
  }
}
function Ng(e12, t) {
  if (e12.length <= S)
    return;
  let n = S + t, r = e12[n], o = r ? r[ke] : void 0;
  o && o.leave && o.leave.size > 0 && (o.detachedLeaveAnimationFns = []);
}
function xg(e12, t) {
  return ln(e12, t);
}
function Ag(e12, t) {
  return Mu(e12, t);
}
function bs(e12, t) {
  return ir(e12, t);
}
function j(e12, t, n, r) {
  let o = M(), i = o[m], s = e12 + F, a = i.firstCreatePass ? Hh(s, i, 2, t, n, r) : i.data[s];
  return Xp(a, o, e12, t, Rg), r != null && gu(o, a), j;
}
function B() {
  let e12 = pe(), t = eh(e12);
  return Dc(t) && wc(), Ec(), B;
}
var Rg = (e12, t, n, r, o) => (pr(true), nu(t[O], r, Lc()));
function me(e12, t, n) {
  let r = M(), o = en();
  if (yn(r, o, t)) {
    let i = oe(), s = Pc();
    Zp(s, r, e12, t, r[O], n);
  }
  return me;
}
var En = "en-US";
var Og = En;
function Uu(e12) {
  typeof e12 == "string" && (Og = e12.toLowerCase().replace(/_/g, "-"));
}
function Ve(e12, t, n) {
  let r = M(), o = oe(), i = pe();
  return (i.type & 3 || n) && Bh(i, o, r, n, r[O], e12, t, Vh(i, r, t)), Ve;
}
function na(e12 = 1) {
  return kc(e12);
}
function no(e12, t, n) {
  return fg(e12, t, n), no;
}
function ra(e12) {
  let t = M(), n = oe(), r = _i();
  lr(r + 1);
  let o = Zs(n, r);
  if (e12.dirty && fc(t) === ((o.metadata.flags & 2) === 2)) {
    if (o.matches === null)
      e12.reset([]);
    else {
      let i = gg(t, r);
      e12.reset(i, Ff), e12.notifyOnChanges();
    }
    return true;
  }
  return false;
}
function oa() {
  return ug(M(), _i());
}
function Er(e12, t) {
  return e12 << 17 | t << 2;
}
function at(e12) {
  return e12 >> 17 & 32767;
}
function kg(e12) {
  return (e12 & 2) == 2;
}
function Pg(e12, t) {
  return e12 & 131071 | t << 17;
}
function Cs(e12) {
  return e12 | 2;
}
function kt(e12) {
  return (e12 & 131068) >> 2;
}
function Bi(e12, t) {
  return e12 & -131069 | t << 2;
}
function Lg(e12) {
  return (e12 & 1) === 1;
}
function Ts(e12) {
  return e12 | 1;
}
function Fg(e12, t, n, r, o, i) {
  let s = i ? t.classBindings : t.styleBindings, a = at(s), c = kt(s);
  e12[r] = n;
  let l = false, u;
  if (Array.isArray(n)) {
    let d = n;
    u = d[1], (u === null || Et(d, u) > 0) && (l = true);
  } else
    u = n;
  if (o)
    if (c !== 0) {
      let f = at(e12[a + 1]);
      e12[r + 1] = Er(f, a), f !== 0 && (e12[f + 1] = Bi(e12[f + 1], r)), e12[a + 1] = Pg(e12[a + 1], r);
    } else
      e12[r + 1] = Er(a, 0), a !== 0 && (e12[a + 1] = Bi(e12[a + 1], r)), a = r;
  else
    e12[r + 1] = Er(c, 0), a === 0 ? a = r : e12[c + 1] = Bi(e12[c + 1], r), c = r;
  l && (e12[r + 1] = Cs(e12[r + 1])), Dl(e12, u, r, true), Dl(e12, u, r, false), jg(t, u, e12, r, i), s = Er(a, c), i ? t.classBindings = s : t.styleBindings = s;
}
function jg(e12, t, n, r, o) {
  let i = o ? e12.residualClasses : e12.residualStyles;
  i != null && typeof t == "string" && Et(i, t) >= 0 && (n[r + 1] = Ts(n[r + 1]));
}
function Dl(e12, t, n, r) {
  let o = e12[n + 1], i = t === null, s = r ? at(o) : kt(o), a = false;
  for (; s !== 0 && (a === false || i); ) {
    let c = e12[s], l = e12[s + 1];
    Hg(c, t) && (a = true, e12[s + 1] = r ? Ts(l) : Cs(l)), s = r ? at(l) : kt(l);
  }
  a && (e12[n + 1] = r ? Cs(o) : Ts(o));
}
function Hg(e12, t) {
  return e12 === null || t == null || (Array.isArray(e12) ? e12[1] : e12) === t ? true : Array.isArray(e12) && typeof t == "string" ? Et(e12, t) >= 0 : false;
}
function ro(e12, t) {
  return Vg(e12, t, null, true), ro;
}
function Vg(e12, t, n, r) {
  let o = M(), i = oe(), s = Mc(2);
  if (i.firstUpdatePass && $g(i, e12, s, r), t !== Se && yn(o, s, t)) {
    let a = i.data[Fe()];
    qg(i, a, o, o[O], e12, o[s + 1] = Zg(t, n), r, s);
  }
}
function Bg(e12, t) {
  return t >= e12.expandoStartIndex;
}
function $g(e12, t, n, r) {
  let o = e12.data;
  if (o[n + 1] === null) {
    let i = o[Fe()], s = Bg(e12, n);
    Qg(i, r) && t === null && !s && (t = false), t = Ug(o, i, t, r), Fg(o, i, t, n, s, r);
  }
}
function Ug(e12, t, n, r) {
  let o = xc(e12), i = r ? t.residualClasses : t.residualStyles;
  if (o === null)
    (r ? t.classBindings : t.styleBindings) === 0 && (n = $i(null, e12, t, n, r), n = pn(n, t.attrs, r), i = null);
  else {
    let s = t.directiveStylingLast;
    if (s === -1 || e12[s] !== o)
      if (n = $i(o, e12, t, n, r), i === null) {
        let c = zg(e12, t, r);
        c !== void 0 && Array.isArray(c) && (c = $i(null, e12, t, c[1], r), c = pn(c, t.attrs, r), Wg(e12, t, r, c));
      } else
        i = Gg(e12, t, r);
  }
  return i !== void 0 && (r ? t.residualClasses = i : t.residualStyles = i), n;
}
function zg(e12, t, n) {
  let r = n ? t.classBindings : t.styleBindings;
  if (kt(r) !== 0)
    return e12[at(r)];
}
function Wg(e12, t, n, r) {
  let o = n ? t.classBindings : t.styleBindings;
  e12[at(o)] = r;
}
function Gg(e12, t, n) {
  let r, o = t.directiveEnd;
  for (let i = 1 + t.directiveStylingLast; i < o; i++) {
    let s = e12[i].hostAttrs;
    r = pn(r, s, n);
  }
  return pn(r, t.attrs, n);
}
function $i(e12, t, n, r, o) {
  let i = null, s = n.directiveEnd, a = n.directiveStylingLast;
  for (a === -1 ? a = n.directiveStart : a++; a < s && (i = t[a], r = pn(r, i.hostAttrs, o), i !== e12); )
    a++;
  return e12 !== null && (n.directiveStylingLast = a), r;
}
function pn(e12, t, n) {
  let r = n ? 1 : 2, o = -1;
  if (t !== null)
    for (let i = 0; i < t.length; i++) {
      let s = t[i];
      typeof s == "number" ? o = s : o === r && (Array.isArray(e12) || (e12 = e12 === void 0 ? [] : ["", e12]), nc(e12, s, n ? true : t[++i]));
    }
  return e12 === void 0 ? null : e12;
}
function qg(e12, t, n, r, o, i, s, a) {
  if (!(t.type & 3))
    return;
  let c = e12.data, l = c[a + 1], u = Lg(l) ? wl(c, t, n, o, kt(l), s) : void 0;
  if (!Lr(u)) {
    Lr(i) || kg(l) && (i = wl(c, null, n, o, a, s));
    let d = vi(Fe(), n);
    Up(r, s, d, o, i);
  }
}
function wl(e12, t, n, r, o, i) {
  let s = t === null, a;
  for (; o > 0; ) {
    let c = e12[o], l = Array.isArray(c), u = l ? c[1] : c, d = u === null, f = n[o + 1];
    f === Se && (f = d ? Ne : void 0);
    let p = d ? tr(f, r) : u === r ? f : void 0;
    if (l && !Lr(p) && (p = tr(c, r)), Lr(p) && (a = p, s))
      return a;
    let h = e12[o + 1];
    o = s ? at(h) : kt(h);
  }
  if (t !== null) {
    let c = i ? t.residualClasses : t.residualStyles;
    c != null && (a = tr(c, r));
  }
  return a;
}
function Lr(e12) {
  return e12 !== void 0;
}
function Zg(e12, t) {
  return e12 == null || e12 === "" || (typeof t == "string" ? e12 = e12 + t : typeof e12 == "object" && (e12 = Qn(Me(e12)))), e12;
}
function Qg(e12, t) {
  return (e12.flags & (t ? 8 : 16)) !== 0;
}
function se(e12, t = "") {
  let n = M(), r = oe(), o = e12 + F, i = r.firstCreatePass ? Qr(r, o, 1, t, null) : r.data[o], s = Yg(r, n, i, t);
  n[o] = s, fr() && Us(r, n, s, i), _t(i, false);
}
var Yg = (e12, t, n, r) => (pr(true), fp(t[O], r));
function Kg(e12, t, n, r = "") {
  return yn(e12, en(), n) ? t + ii(n) + r : Se;
}
function Be(e12) {
  return ia("", e12), Be;
}
function ia(e12, t, n) {
  let r = M(), o = Kg(r, e12, t, n);
  return o !== Se && Jg(r, Fe(), o), ia;
}
function Jg(e12, t, n) {
  let r = vi(t, e12);
  pp(e12[O], r, n);
}
var zu = (() => {
  class e12 {
    applicationErrorHandler = E(rt);
    appRef = E(vn);
    taskService = E(Nt);
    ngZone = E(Y);
    zonelessEnabled = E(tn);
    tracing = E(Lt, { optional: true });
    zoneIsDefined = typeof Zone < "u" && !!Zone.root.run;
    schedulerTickApplyArgs = [{ data: { __scheduler_tick__: true } }];
    subscriptions = new H();
    angularZoneId = this.zoneIsDefined ? this.ngZone._inner?.get(Gt) : null;
    scheduleInRootZone = !this.zonelessEnabled && this.zoneIsDefined && (E(ki, { optional: true }) ?? false);
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
      let r = this.useMicrotaskScheduler ? Bc : xi;
      this.pendingRenderTaskId = this.taskService.add(), this.scheduleInRootZone ? this.cancelScheduledCallback = Zone.root.run(() => r(() => this.tick())) : this.cancelScheduledCallback = this.ngZone.runOutsideAngular(() => r(() => this.tick()));
    }
    shouldScheduleTick() {
      return !(this.appRef.destroyed || this.pendingRenderTaskId !== null || this.runningTick || this.appRef._runningTick || !this.zonelessEnabled && this.zoneIsDefined && Zone.current.get(Gt + this.angularZoneId));
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
      return new (r || e12)();
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac, providedIn: "root" });
  }
  return e12;
})();
function Wu() {
  return [{ provide: Ze, useExisting: zu }, { provide: Y, useClass: qt }, { provide: tn, useValue: true }];
}
function Xg() {
  return typeof $localize < "u" && $localize.locale || En;
}
var sa = new D("", { factory: () => E(sa, { optional: true, skipSelf: true }) || Xg() });
function $e(e12, t) {
  return On(e12, t?.equal);
}
var aa = new D("");
var lm = new D("");
function In(e12) {
  return !e12.moduleRef;
}
function um(e12) {
  let t = In(e12) ? e12.r3Injector : e12.moduleRef.injector, n = t.get(Y);
  return n.run(() => {
    In(e12) ? e12.r3Injector.resolveInjectorInitializers() : e12.moduleRef.resolveInjectorInitializers();
    let r = t.get(rt), o;
    if (n.runOutsideAngular(() => {
      o = n.onError.subscribe({ next: r });
    }), In(e12)) {
      let i = () => t.destroy(), s = e12.platformInjector.get(aa);
      s.add(i), t.onDestroy(() => {
        o.unsubscribe(), s.delete(i);
      });
    } else {
      let i = () => e12.moduleRef.destroy(), s = e12.platformInjector.get(aa);
      s.add(i), e12.moduleRef.onDestroy(() => {
        on(e12.allPlatformModules, e12.moduleRef), o.unsubscribe(), s.delete(i);
      });
    }
    return fm(r, n, () => {
      let i = t.get(Nt), s = i.add(), a = t.get(Js);
      return a.runInitializers(), a.donePromise.then(() => {
        let c = t.get(sa, En);
        if (Uu(c || En), !t.get(lm, true))
          return In(e12) ? t.get(vn) : (e12.allPlatformModules.push(e12.moduleRef), e12.moduleRef);
        if (In(e12)) {
          let u = t.get(vn);
          return e12.rootComponent !== void 0 && u.bootstrap(e12.rootComponent), u;
        } else
          return dm?.(e12.moduleRef, e12.allPlatformModules), e12.moduleRef;
      }).finally(() => {
        i.remove(s);
      });
    });
  });
}
var dm;
function fm(e12, t, n) {
  try {
    let r = n();
    return Ks(r) ? r.catch((o) => {
      throw t.runOutsideAngular(() => e12(o)), o;
    }) : r;
  } catch (r) {
    throw t.runOutsideAngular(() => e12(r)), r;
  }
}
var oo = null;
function pm(e12 = [], t) {
  return ce.create({ name: t, providers: [{ provide: Yt, useValue: "platform" }, { provide: aa, useValue: /* @__PURE__ */ new Set([() => oo = null]) }, ...e12] });
}
function hm(e12 = []) {
  if (oo)
    return oo;
  let t = pm(e12);
  return oo = t, Bu(), gm(t), t;
}
function gm(e12) {
  let t = e12.get(Hr, null);
  nr(e12, () => {
    t?.forEach((n) => n());
  });
}
var mm = 1e4;
var VM = mm - 1e3;
function qu(e12) {
  let { rootComponent: t, appProviders: n, platformProviders: r, platformRef: o } = e12;
  T(b.BootstrapApplicationStart);
  try {
    let i = o?.injector ?? hm(r), s = [Wu(), Uc, ...n || []], a = new fn({ providers: s, parent: i, debugName: "", runEnvironmentInitializers: false });
    return um({ r3Injector: a.injector, platformInjector: i, rootComponent: t });
  } catch (i) {
    return Promise.reject(i);
  } finally {
    T(b.BootstrapApplicationEnd);
  }
}
var Zu = null;
function jt() {
  return Zu;
}
function ca(e12) {
  Zu ??= e12;
}
var wn = class {
};
function la(e12, t) {
  t = encodeURIComponent(t);
  for (let n of e12.split(";")) {
    let r = n.indexOf("="), [o, i] = r == -1 ? [n, ""] : [n.slice(0, r), n.slice(r + 1)];
    if (o.trim() === t)
      return decodeURIComponent(i);
  }
  return null;
}
var bn = class {
};
var Qu = "browser";
var Cn = class {
  _doc;
  constructor(t) {
    this._doc = t;
  }
  manager;
};
var io = (() => {
  class e12 extends Cn {
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
      return new (r || e12)(w(U));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var co = new D("");
var pa = (() => {
  class e12 {
    _zone;
    _plugins;
    _eventNameToPlugin = /* @__PURE__ */ new Map();
    constructor(n, r) {
      this._zone = r, n.forEach((s) => {
        s.manager = this;
      });
      let o = n.filter((s) => !(s instanceof io));
      this._plugins = o.slice().reverse();
      let i = n.find((s) => s instanceof io);
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
        throw new v(5101, false);
      return this._eventNameToPlugin.set(n, r), r;
    }
    static \u0275fac = function(r) {
      return new (r || e12)(w(co), w(Y));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var ua = "ng-app-id";
function Yu(e12) {
  for (let t of e12)
    t.remove();
}
function Ku(e12, t) {
  let n = t.createElement("style");
  return n.textContent = e12, n;
}
function ym(e12, t, n, r) {
  let o = e12.head?.querySelectorAll(`style[${ua}="${t}"],link[${ua}="${t}"]`);
  if (o)
    for (let i of o)
      i.removeAttribute(ua), i instanceof HTMLLinkElement ? r.set(i.href.slice(i.href.lastIndexOf("/") + 1), { usage: 0, elements: [i] }) : i.textContent && n.set(i.textContent, { usage: 0, elements: [i] });
}
function fa(e12, t) {
  let n = t.createElement("link");
  return n.setAttribute("rel", "stylesheet"), n.setAttribute("href", e12), n;
}
var ha = (() => {
  class e12 {
    doc;
    appId;
    nonce;
    inline = /* @__PURE__ */ new Map();
    external = /* @__PURE__ */ new Map();
    hosts = /* @__PURE__ */ new Set();
    constructor(n, r, o, i = {}) {
      this.doc = n, this.appId = r, this.nonce = o, ym(n, r, this.inline, this.external), this.hosts.add(n.head);
    }
    addStyles(n, r) {
      for (let o of n)
        this.addUsage(o, this.inline, Ku);
      r?.forEach((o) => this.addUsage(o, this.external, fa));
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
      o && (o.usage--, o.usage <= 0 && (Yu(o.elements), r.delete(n)));
    }
    ngOnDestroy() {
      for (let [, { elements: n }] of [...this.inline, ...this.external])
        Yu(n);
      this.hosts.clear();
    }
    addHost(n) {
      this.hosts.add(n);
      for (let [r, { elements: o }] of this.inline)
        o.push(this.addElement(n, Ku(r, this.doc)));
      for (let [r, { elements: o }] of this.external)
        o.push(this.addElement(n, fa(r, this.doc)));
    }
    removeHost(n) {
      this.hosts.delete(n);
    }
    addElement(n, r) {
      return this.nonce && r.setAttribute("nonce", this.nonce), n.appendChild(r);
    }
    static \u0275fac = function(r) {
      return new (r || e12)(w(U), w(jr), w(Vr, 8), w(gn));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var da = { svg: "http://www.w3.org/2000/svg", xhtml: "http://www.w3.org/1999/xhtml", xlink: "http://www.w3.org/1999/xlink", xml: "http://www.w3.org/XML/1998/namespace", xmlns: "http://www.w3.org/2000/xmlns/", math: "http://www.w3.org/1998/Math/MathML" };
var ga = /%COMP%/g;
var Xu = "%COMP%";
var vm = `_nghost-${Xu}`;
var Em = `_ngcontent-${Xu}`;
var Im = true;
var Dm = new D("", { factory: () => Im });
function wm(e12) {
  return Em.replace(ga, e12);
}
function bm(e12) {
  return vm.replace(ga, e12);
}
function ed(e12, t) {
  return t.map((n) => n.replace(ga, e12));
}
var ma = (() => {
  class e12 {
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
      this.eventManager = n, this.sharedStylesHost = r, this.appId = o, this.removeStylesOnCompDestroy = i, this.doc = s, this.ngZone = a, this.nonce = c, this.tracingService = l, this.defaultRenderer = new Tn(n, s, a, this.tracingService);
    }
    createRenderer(n, r) {
      if (!n || !r)
        return this.defaultRenderer;
      let o = this.getOrCreateRenderer(n, r);
      return o instanceof ao ? o.applyToHost(n) : o instanceof Mn && o.applyStyles(), o;
    }
    getOrCreateRenderer(n, r) {
      let o = this.rendererByCompId, i = o.get(r.id);
      if (!i) {
        let s = this.doc, a = this.ngZone, c = this.eventManager, l = this.sharedStylesHost, u = this.removeStylesOnCompDestroy, d = this.tracingService;
        switch (r.encapsulation) {
          case ie.Emulated:
            i = new ao(c, l, r, this.appId, u, s, a, d);
            break;
          case ie.ShadowDom:
            return new so(c, n, r, s, a, this.nonce, d, l);
          case ie.ExperimentalIsolatedShadowDom:
            return new so(c, n, r, s, a, this.nonce, d);
          default:
            i = new Mn(c, l, r, u, s, a, d);
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
      return new (r || e12)(w(pa), w(ha), w(jr), w(Dm), w(U), w(Y), w(Vr), w(Lt, 8));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var Tn = class {
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
    return n ? this.doc.createElementNS(da[n] || n, t) : this.doc.createElement(t);
  }
  createComment(t) {
    return this.doc.createComment(t);
  }
  createText(t) {
    return this.doc.createTextNode(t);
  }
  appendChild(t, n) {
    (Ju(t) ? t.content : t).appendChild(n);
  }
  insertBefore(t, n, r) {
    t && (Ju(t) ? t.content : t).insertBefore(n, r);
  }
  removeChild(t, n) {
    n.remove();
  }
  selectRootElement(t, n) {
    let r = typeof t == "string" ? this.doc.querySelector(t) : t;
    if (!r)
      throw new v(-5104, false);
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
      let i = da[o];
      i ? t.setAttributeNS(i, n, r) : t.setAttribute(n, r);
    } else
      t.setAttribute(n, r);
  }
  removeAttribute(t, n, r) {
    if (r) {
      let o = da[r];
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
    if (typeof t == "string" && (t = jt().getGlobalEventTarget(this.doc, t), !t))
      throw new v(5102, false);
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
function Ju(e12) {
  return e12.tagName === "TEMPLATE" && e12.content !== void 0;
}
var so = class extends Tn {
  hostEl;
  sharedStylesHost;
  shadowRoot;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, o, i, a), this.hostEl = n, this.sharedStylesHost = c, this.shadowRoot = n.attachShadow({ mode: "open" }), this.sharedStylesHost && this.sharedStylesHost.addHost(this.shadowRoot);
    let l = r.styles;
    l = ed(r.id, l);
    for (let d of l) {
      let f = document.createElement("style");
      s && f.setAttribute("nonce", s), f.textContent = d, this.shadowRoot.appendChild(f);
    }
    let u = r.getExternalStyles?.();
    if (u)
      for (let d of u) {
        let f = fa(d, o);
        s && f.setAttribute("nonce", s), this.shadowRoot.appendChild(f);
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
var Mn = class extends Tn {
  sharedStylesHost;
  removeStylesOnCompDestroy;
  styles;
  styleUrls;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, i, s, a), this.sharedStylesHost = n, this.removeStylesOnCompDestroy = o;
    let l = r.styles;
    this.styles = c ? ed(c, l) : l, this.styleUrls = r.getExternalStyles?.(c);
  }
  applyStyles() {
    this.sharedStylesHost.addStyles(this.styles, this.styleUrls);
  }
  destroy() {
    this.removeStylesOnCompDestroy && it.size === 0 && this.sharedStylesHost.removeStyles(this.styles, this.styleUrls);
  }
};
var ao = class extends Mn {
  contentAttr;
  hostAttr;
  constructor(t, n, r, o, i, s, a, c) {
    let l = o + "-" + r.id;
    super(t, n, r, i, s, a, c, l), this.contentAttr = wm(l), this.hostAttr = bm(l);
  }
  applyToHost(t) {
    this.applyStyles(), this.setAttribute(t, this.hostAttr, "");
  }
  createElement(t, n) {
    let r = super.createElement(t, n);
    return super.setAttribute(r, this.contentAttr, ""), r;
  }
};
var lo = class e9 extends wn {
  supportsDOMEvents = true;
  static makeCurrent() {
    ca(new e9());
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
    let n = Cm();
    return n == null ? null : Tm(n);
  }
  resetBaseElement() {
    _n = null;
  }
  getUserAgent() {
    return window.navigator.userAgent;
  }
  getCookie(t) {
    return la(document.cookie, t);
  }
};
var _n = null;
function Cm() {
  return _n = _n || document.head.querySelector("base"), _n ? _n.getAttribute("href") : null;
}
function Tm(e12) {
  return new URL(e12, document.baseURI).pathname;
}
var Mm = (() => {
  class e12 {
    build() {
      return new XMLHttpRequest();
    }
    static \u0275fac = function(r) {
      return new (r || e12)();
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var td = ["alt", "control", "meta", "shift"];
var _m = { "\b": "Backspace", "	": "Tab", "\x7F": "Delete", "\x1B": "Escape", Del: "Delete", Esc: "Escape", Left: "ArrowLeft", Right: "ArrowRight", Up: "ArrowUp", Down: "ArrowDown", Menu: "ContextMenu", Scroll: "ScrollLock", Win: "OS" };
var Sm = { alt: (e12) => e12.altKey, control: (e12) => e12.ctrlKey, meta: (e12) => e12.metaKey, shift: (e12) => e12.shiftKey };
var nd = (() => {
  class e12 extends Cn {
    constructor(n) {
      super(n);
    }
    supports(n) {
      return e12.parseEventName(n) != null;
    }
    addEventListener(n, r, o, i) {
      let s = e12.parseEventName(r), a = e12.eventCallback(s.fullKey, o, this.manager.getZone());
      return this.manager.getZone().runOutsideAngular(() => jt().onAndCancel(n, s.domEventName, a, i));
    }
    static parseEventName(n) {
      let r = n.toLowerCase().split("."), o = r.shift();
      if (r.length === 0 || !(o === "keydown" || o === "keyup"))
        return null;
      let i = e12._normalizeKey(r.pop()), s = "", a = r.indexOf("code");
      if (a > -1 && (r.splice(a, 1), s = "code."), td.forEach((l) => {
        let u = r.indexOf(l);
        u > -1 && (r.splice(u, 1), s += l + ".");
      }), s += i, r.length != 0 || i.length === 0)
        return null;
      let c = {};
      return c.domEventName = o, c.fullKey = s, c;
    }
    static matchEventFullKeyCode(n, r) {
      let o = _m[n.key] || n.key, i = "";
      return r.indexOf("code.") > -1 && (o = n.code, i = "code."), o == null || !o ? false : (o = o.toLowerCase(), o === " " ? o = "space" : o === "." && (o = "dot"), td.forEach((s) => {
        if (s !== o) {
          let a = Sm[s];
          a(n) && (i += s + ".");
        }
      }), i += o, i === r);
    }
    static eventCallback(n, r, o) {
      return (i) => {
        e12.matchEventFullKeyCode(i, n) && o.runGuarded(() => r(i));
      };
    }
    static _normalizeKey(n) {
      return n === "esc" ? "escape" : n;
    }
    static \u0275fac = function(r) {
      return new (r || e12)(w(U));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
async function ya(e12, t, n) {
  let r = N({ rootComponent: e12 }, Nm(t, n));
  return qu(r);
}
function Nm(e12, t) {
  return { platformRef: t?.platformRef, appProviders: [...km, ...e12?.providers ?? []], platformProviders: Om };
}
function xm() {
  lo.makeCurrent();
}
function Am() {
  return new Ie();
}
function Rm() {
  return Ns(document), document;
}
var Om = [{ provide: gn, useValue: Qu }, { provide: Hr, useValue: xm, multi: true }, { provide: U, useFactory: Rm }];
var km = [{ provide: Yt, useValue: "root" }, { provide: Ie, useFactory: Am }, { provide: co, useClass: io, multi: true }, { provide: co, useClass: nd, multi: true }, ma, ha, pa, { provide: st, useExisting: ma }, { provide: bn, useClass: Mm }, []];
var va = (() => {
  class e12 {
    static \u0275fac = function(r) {
      return new (r || e12)();
    };
    static \u0275prov = _({ token: e12, factory: function(r) {
      let o = null;
      return r ? o = new (r || e12)() : o = w(Pm), o;
    }, providedIn: "root" });
  }
  return e12;
})();
var Pm = (() => {
  class e12 extends va {
    _doc;
    constructor(n) {
      super(), this._doc = n;
    }
    sanitize(n, r) {
      if (r == null)
        return null;
      switch (n) {
        case ge.NONE:
          return r;
        case ge.HTML:
          return He(r, "HTML") ? Me(r) : Ur(this._doc, String(r)).toString();
        case ge.STYLE:
          return He(r, "Style") ? Me(r) : r;
        case ge.SCRIPT:
          if (He(r, "Script"))
            return Me(r);
          throw new v(5200, false);
        case ge.URL:
          return He(r, "URL") ? Me(r) : $r(String(r));
        case ge.RESOURCE_URL:
          if (He(r, "ResourceURL"))
            return Me(r);
          throw new v(5201, false);
        default:
          throw new v(5202, false);
      }
    }
    bypassSecurityTrustHtml(n) {
      return As(n);
    }
    bypassSecurityTrustStyle(n) {
      return Rs(n);
    }
    bypassSecurityTrustScript(n) {
      return Os(n);
    }
    bypassSecurityTrustUrl(n) {
      return ks(n);
    }
    bypassSecurityTrustResourceUrl(n) {
      return Ps(n);
    }
    static \u0275fac = function(r) {
      return new (r || e12)(w(U));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac, providedIn: "root" });
  }
  return e12;
})();
var uo = class e10 {
  constructor(t) {
    this.model = t;
    if (t) {
      this.page.set(t.get("page") ?? 0), this.pageSize.set(t.get("page_size") ?? 10), this.maxColumns.set(t.get("max_columns") ?? 0), this.rowCount.set(t.get("row_count") ?? null), this.tableHtml.set(t.get("table_html") ?? ""), this.sortContext.set(t.get("sort_context") ?? []), this.orderableColumns.set(t.get("orderable_columns") ?? []);
      let n = t.get("error_message") ?? t.get("_error_message") ?? null;
      this.errorMessage.set(n), t.on("change:page", () => {
        this.page.set(t.get("page"));
      }), t.on("change:page_size", () => {
        this.pageSize.set(t.get("page_size"));
      }), t.on("change:max_columns", () => {
        this.maxColumns.set(t.get("max_columns"));
      }), t.on("change:row_count", () => {
        this.rowCount.set(t.get("row_count"));
      }), t.on("change:table_html", () => {
        this.tableHtml.set(t.get("table_html"));
      }), t.on("change:sort_context", () => {
        this.sortContext.set(t.get("sort_context"));
      }), t.on("change:orderable_columns", () => {
        this.orderableColumns.set(t.get("orderable_columns"));
      });
      let r = () => {
        let o = t.get("error_message") ?? t.get("_error_message") ?? null;
        this.errorMessage.set(o);
      };
      t.on("change:error_message", r), t.on("change:_error_message", r);
    }
  }
  page = q(0);
  pageSize = q(10);
  maxColumns = q(0);
  rowCount = q(null);
  tableHtml = q("");
  sortContext = q([]);
  orderableColumns = q([]);
  errorMessage = q(null);
  setPage(t) {
    this.page.set(t), this.model && (this.model.set("page", t), this.model.save_changes());
  }
  setPageSize(t) {
    this.pageSize.set(t), this.model && (this.model.set("page_size", t), this.model.set("page", 0), this.model.save_changes());
  }
  setMaxColumns(t) {
    this.maxColumns.set(t), this.model && (this.model.set("max_columns", t), this.model.save_changes());
  }
  setSortContext(t) {
    this.sortContext.set(t), this.model && (this.model.set("sort_context", t), this.model.save_changes());
  }
  static \u0275fac = function(n) {
    return new (n || e10)(w("ANYWIDGET_MODEL"));
  };
  static \u0275prov = _({ token: e10, factory: e10.\u0275fac, providedIn: "root" });
};
var Lm = ["tableContainer"];
function Fm(e12, t) {
  if (e12 & 1 && (j(0, "div", 2), se(1), B()), e12 & 2) {
    let n = na();
    V(), Be(n.errorMessage());
  }
}
function jm(e12, t) {
  if (e12 & 1 && (j(0, "option", 13), se(1), B()), e12 & 2) {
    let n = t.$implicit;
    me("value", n), V(), Be(n === 0 ? "All" : n);
  }
}
function Hm(e12, t) {
  if (e12 & 1 && (j(0, "option", 13), se(1), B()), e12 & 2) {
    let n = t.$implicit;
    me("value", n), V(), Be(n);
  }
}
var fo = class e11 {
  state = E(uo);
  sanitizer = E(va);
  maxColumnOptions = [5, 10, 15, 20, 0];
  pageSizeOptions = [10, 25, 50, 100];
  errorMessage = this.state.errorMessage;
  maxColumns = this.state.maxColumns;
  pageSize = this.state.pageSize;
  page = this.state.page;
  rowCount = this.state.rowCount;
  sanitizedHtml = $e(() => this.sanitizer.bypassSecurityTrustHtml(this.state.tableHtml()));
  totalPages = $e(() => {
    let t = this.rowCount(), n = this.pageSize();
    return t !== null && n > 0 ? Math.ceil(t / n) : null;
  });
  pageIndicatorText = $e(() => {
    let t = this.page(), n = this.rowCount(), r = this.totalPages(), o = (t + 1).toLocaleString(), i = (r ?? 1).toLocaleString();
    return `Page ${o} of ${i}`;
  });
  rowCountText = $e(() => {
    let t = this.rowCount();
    return t === null ? "Total rows unknown" : t === 0 ? "0 total rows" : `${t.toLocaleString()} total rows`;
  });
  prevPageDisabled = $e(() => this.page() === 0);
  nextPageDisabled = $e(() => {
    let t = this.page(), n = this.rowCount(), r = this.totalPages();
    return n === null ? false : n === 0 ? true : r !== null && t >= r - 1;
  });
  isDarkMode = q(false);
  themeObserver = null;
  isHeightInitialized = false;
  tableContainerRef;
  constructor() {
    Pi(() => {
      let t = this.state.tableHtml(), n = this.state.sortContext(), r = this.state.orderableColumns();
      setTimeout(() => {
        this.applySortIndicators(), this.initializeHeight();
      }, 0);
    });
  }
  ngOnInit() {
    this.initThemeDetection();
  }
  ngOnDestroy() {
    this.themeObserver?.disconnect();
  }
  handlePageChange(t) {
    let n = this.page() + t;
    this.state.setPage(n);
  }
  handlePageSizeChange(t) {
    let n = t.target, r = Number(n.value);
    r && this.state.setPageSize(r);
  }
  handleMaxColumnsChange(t) {
    let n = t.target, r = Number(n.value);
    this.state.setMaxColumns(r);
  }
  handleTableClick(t) {
    let r = t.target.closest("th");
    if (!r)
      return;
    let o = r.querySelector("div.bf-header-content");
    if (!o)
      return;
    let i = o.textContent?.trim() || "", s = this.state.orderableColumns();
    if (!i || !s.includes(i))
      return;
    let a = [...this.state.sortContext()], c = a.findIndex((u) => u.column === i), l = [...a];
    t.shiftKey ? c !== -1 ? l[c].ascending ? l[c] = A(N({}, l[c]), { ascending: false }) : l.splice(c, 1) : l.push({ column: i, ascending: true }) : c !== -1 && l.length === 1 ? l[c].ascending ? l[c] = A(N({}, l[c]), { ascending: false }) : l = [] : l = [{ column: i, ascending: true }], this.state.setSortContext(l);
  }
  applySortIndicators() {
    let t = this.tableContainerRef?.nativeElement;
    if (!t)
      return;
    let n = this.state.orderableColumns(), r = this.state.sortContext() || [], o = (s) => r.findIndex((a) => a.column === s);
    t.querySelectorAll("th").forEach((s) => {
      let a = s.querySelector("div.bf-header-content");
      if (!a)
        return;
      let c = a.textContent?.trim() || "";
      if (c && n.includes(c)) {
        s.style.cursor = "pointer";
        let l = a.querySelector(".sort-indicator");
        l || (l = document.createElement("span"), l.classList.add("sort-indicator"), l.style.paddingLeft = "5px", a.appendChild(l));
        let u = o(c);
        if (u !== -1) {
          let d = r[u].ascending;
          l.textContent = d ? "\u25B2" : "\u25BC", l.style.visibility = "visible";
        } else
          l.textContent = "\u25CF", l.style.visibility = "hidden";
      }
    });
  }
  initializeHeight() {
    if (this.isHeightInitialized)
      return;
    let t = this.tableContainerRef?.nativeElement;
    if (!t)
      return;
    let n = t.querySelector("table");
    if (n) {
      let r = n.offsetHeight;
      r > 0 && (t.style.height = `${r + 2}px`, this.isHeightInitialized = true);
    }
  }
  initThemeDetection() {
    this.updateTheme();
    let t = new MutationObserver(() => this.updateTheme());
    t.observe(document.body, { attributes: true, attributeFilter: ["class", "data-theme", "data-vscode-theme-kind"] }), this.themeObserver = t;
  }
  updateTheme() {
    let t = document.body, n = t.classList.contains("vscode-dark") || t.classList.contains("theme-dark") || t.dataset.theme === "dark" || t.getAttribute("data-vscode-theme-kind") === "vscode-dark";
    this.isDarkMode.set(n);
  }
  static \u0275fac = function(n) {
    return new (n || e11)();
  };
  static \u0275cmp = Qs({ type: e11, selectors: [["app-root"]], viewQuery: function(n, r) {
    if (n & 1 && no(Lm, 7), n & 2) {
      let o;
      ra(o = oa()) && (r.tableContainerRef = o.first);
    }
  }, decls: 27, vars: 10, consts: [["tableContainer", ""], [1, "bigframes-widget"], [1, "bigframes-error-message"], [1, "table-container", 3, "click", "innerHTML"], [1, "footer"], [1, "row-count"], [1, "pagination"], [3, "click", "disabled"], [1, "page-indicator"], [1, "settings"], [1, "max-columns"], ["for", "max-cols-select"], ["id", "max-cols-select", 3, "change", "value"], [3, "value"], [1, "page-size"], ["for", "page-size-select"], ["id", "page-size-select", 3, "change", "value"]], template: function(n, r) {
    n & 1 && (j(0, "div", 1), Xs(1, Fm, 2, 1, "div", 2), j(2, "div", 3, 0), Ve("click", function(i) {
      return r.handleTableClick(i);
    }), B(), j(4, "footer", 4)(5, "span", 5), se(6), B(), j(7, "div", 6)(8, "button", 7), Ve("click", function() {
      return r.handlePageChange(-1);
    }), se(9, "<"), B(), j(10, "span", 8), se(11), B(), j(12, "button", 7), Ve("click", function() {
      return r.handlePageChange(1);
    }), se(13, ">"), B()(), j(14, "div", 9)(15, "div", 10)(16, "label", 11), se(17, "Max columns:"), B(), j(18, "select", 12), Ve("change", function(i) {
      return r.handleMaxColumnsChange(i);
    }), eo(19, jm, 2, 2, "option", 13, Xr), B()(), j(21, "div", 14)(22, "label", 15), se(23, "Page size:"), B(), j(24, "select", 16), Ve("change", function(i) {
      return r.handlePageSizeChange(i);
    }), eo(25, Hm, 2, 2, "option", 13, Xr), B()()()()()), n & 2 && (ro("bigframes-dark-mode", r.isDarkMode()), V(), ta(r.errorMessage() ? 1 : -1), V(), me("innerHTML", r.sanitizedHtml(), Ls), V(4), Be(r.rowCountText()), V(2), me("disabled", r.prevPageDisabled()), V(3), Be(r.pageIndicatorText()), V(), me("disabled", r.nextPageDisabled()), V(6), me("value", r.maxColumns()), V(), to(r.maxColumnOptions), V(5), me("value", r.pageSize()), V(), to(r.pageSizeOptions));
  }, styles: [".bigframes-widget.bigframes-widget[_ngcontent-%COMP%]{--bf-bg: white;--bf-border-color: #ccc;--bf-error-bg: #fbe;--bf-error-border: red;--bf-error-fg: black;--bf-fg: black;--bf-header-bg: #f5f5f5;--bf-null-fg: gray;--bf-row-even-bg: #f5f5f5;--bf-row-odd-bg: white;background-color:var(--bf-bg);box-sizing:border-box;color:var(--bf-fg);display:flex;flex-direction:column;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;margin:0;padding:0}.bigframes-widget[_ngcontent-%COMP%]   *[_ngcontent-%COMP%]{box-sizing:border-box}@media(prefers-color-scheme:dark){.bigframes-widget.bigframes-widget[_ngcontent-%COMP%]{--bf-bg: var(--vscode-editor-background, #202124);--bf-border-color: #444;--bf-error-bg: #511;--bf-error-border: #f88;--bf-error-fg: #fcc;--bf-fg: white;--bf-header-bg: var(--vscode-editor-background, black);--bf-null-fg: #aaa;--bf-row-even-bg: #202124;--bf-row-odd-bg: #383838}}.bigframes-widget.bigframes-dark-mode.bigframes-dark-mode[_ngcontent-%COMP%]{--bf-bg: var(--vscode-editor-background, #202124);--bf-border-color: #444;--bf-error-bg: #511;--bf-error-border: #f88;--bf-error-fg: #fcc;--bf-fg: white;--bf-header-bg: var(--vscode-editor-background, black);--bf-null-fg: #aaa;--bf-row-even-bg: #202124;--bf-row-odd-bg: #383838}.bigframes-widget[_ngcontent-%COMP%]   .table-container[_ngcontent-%COMP%]{background-color:var(--bf-bg);margin:0;max-height:620px;overflow:auto;padding:0}.bigframes-widget[_ngcontent-%COMP%]   .footer[_ngcontent-%COMP%]{align-items:center;background-color:var(--bf-bg);color:var(--bf-fg);display:flex;font-size:.8rem;justify-content:space-between;padding:8px}.bigframes-widget[_ngcontent-%COMP%]   .footer[_ngcontent-%COMP%] > *[_ngcontent-%COMP%]{flex:1}.bigframes-widget[_ngcontent-%COMP%]   .pagination[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:4px;justify-content:center;padding:4px}.bigframes-widget[_ngcontent-%COMP%]   .page-indicator[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .row-count[_ngcontent-%COMP%]{margin:0 8px}.bigframes-widget[_ngcontent-%COMP%]   .settings[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:16px;justify-content:end}.bigframes-widget[_ngcontent-%COMP%]   .page-size[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .max-columns[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:4px}.bigframes-widget[_ngcontent-%COMP%]   .page-size[_ngcontent-%COMP%]   label[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .max-columns[_ngcontent-%COMP%]   label[_ngcontent-%COMP%]{margin-right:8px}.bigframes-widget[_ngcontent-%COMP%]     table.bigframes-widget-table, .bigframes-widget[_ngcontent-%COMP%]     table.dataframe{background-color:var(--bf-bg);border:1px solid var(--bf-border-color);border-collapse:collapse;border-spacing:0;box-shadow:none;color:var(--bf-fg);margin:0;outline:none;text-align:left;width:auto}.bigframes-widget[_ngcontent-%COMP%]     tr{border:none}.bigframes-widget[_ngcontent-%COMP%]     th{background-color:var(--bf-header-bg);border:1px solid var(--bf-border-color);color:var(--bf-fg);padding:0;position:sticky;text-align:left;top:0;z-index:1}.bigframes-widget[_ngcontent-%COMP%]     td{border:1px solid var(--bf-border-color);color:var(--bf-fg);padding:.5em}.bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(odd), .bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(odd) td{background-color:var(--bf-row-odd-bg)}.bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(2n), .bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(2n) td{background-color:var(--bf-row-even-bg)}.bigframes-widget[_ngcontent-%COMP%]     .bf-header-content{box-sizing:border-box;height:100%;overflow:auto;padding:.5em;resize:horizontal;width:100%}.bigframes-widget[_ngcontent-%COMP%]     th .sort-indicator{padding-left:4px;visibility:hidden}.bigframes-widget[_ngcontent-%COMP%]     th:hover .sort-indicator{visibility:visible}.bigframes-widget[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]{background-color:transparent;border:1px solid currentColor;border-radius:4px;color:inherit;cursor:pointer;display:inline-block;padding:2px 8px;text-align:center;text-decoration:none;-webkit-user-select:none;user-select:none;vertical-align:middle}.bigframes-widget[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]:disabled{opacity:.65;pointer-events:none}.bigframes-widget[_ngcontent-%COMP%]   .bigframes-error-message[_ngcontent-%COMP%]{background-color:var(--bf-error-bg);border:1px solid var(--bf-error-border);border-radius:4px;color:var(--bf-error-fg);font-size:14px;margin-bottom:8px;padding:8px}.bigframes-widget[_ngcontent-%COMP%]     .cell-align-right{text-align:right}.bigframes-widget[_ngcontent-%COMP%]     .cell-align-left{text-align:left}.bigframes-widget[_ngcontent-%COMP%]     .null-value{color:var(--bf-null-fg)}.bigframes-widget[_ngcontent-%COMP%]     .debug-info{border-top:1px solid var(--bf-border-color)}"] });
};
function Vm({ model: e12, el: t }) {
  let n = document.createElement("app-root");
  t.appendChild(n);
  let r = { providers: [Oi(), { provide: "ANYWIDGET_MODEL", useValue: e12 }] };
  ya(fo, r).catch((o) => console.error(o));
}
var tS = { render: Vm };
export {
  tS as default
};
