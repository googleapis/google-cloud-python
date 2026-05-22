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
var ad = Object.defineProperty;
var cd = Object.defineProperties;
var ld = Object.getOwnPropertyDescriptors;
var Ca = Object.getOwnPropertySymbols;
var ud = Object.prototype.hasOwnProperty;
var dd = Object.prototype.propertyIsEnumerable;
var wa = (e12, t, n) => t in e12 ? ad(e12, t, { enumerable: true, configurable: true, writable: true, value: n }) : e12[t] = n;
var N = (e12, t) => {
  for (var n in t ||= {})
    ud.call(t, n) && wa(e12, n, t[n]);
  if (Ca)
    for (var n of Ca(t))
      dd.call(t, n) && wa(e12, n, t[n]);
  return e12;
};
var R = (e12, t) => cd(e12, ld(t));
var V = null;
var On = false;
var wo = 1;
var fd = null;
var Q = Symbol("SIGNAL");
function g(e12) {
  let t = V;
  return V = e12, t;
}
function Pn() {
  return V;
}
var ft = { version: 0, lastCleanEpoch: 0, dirty: false, producers: void 0, producersTail: void 0, consumers: void 0, consumersTail: void 0, recomputing: false, consumerAllowSignalWrites: false, consumerIsAlwaysLive: false, kind: "unknown", producerMustRecompute: () => false, producerRecomputeValue: () => {
}, consumerMarkedDirty: () => {
}, consumerOnSignalRead: () => {
} };
function To(e12) {
  if (On)
    throw new Error("");
  if (V === null)
    return;
  V.consumerOnSignalRead(e12);
  let t = V.producersTail;
  if (t !== void 0 && t.producer === e12)
    return;
  let n, r = V.recomputing;
  if (r && (n = t !== void 0 ? t.nextProducer : V.producers, n !== void 0 && n.producer === e12)) {
    V.producersTail = n, n.lastReadVersion = e12.version;
    return;
  }
  let o = e12.consumersTail;
  if (o !== void 0 && o.consumer === V && (!r || hd(o, V)))
    return;
  let i = ht(V), s = { producer: e12, consumer: V, nextProducer: n, prevConsumer: o, lastReadVersion: e12.version, nextConsumer: void 0 };
  V.producersTail = s, t !== void 0 ? t.nextProducer = s : V.producers = s, i && Sa(e12, s);
}
function Ta() {
  wo++;
}
function Mo(e12) {
  if (!(ht(e12) && !e12.dirty) && !(!e12.dirty && e12.lastCleanEpoch === wo)) {
    if (!e12.producerMustRecompute(e12) && !Fn(e12)) {
      Co(e12);
      return;
    }
    e12.producerRecomputeValue(e12), Co(e12);
  }
}
function _o(e12) {
  if (e12.consumers === void 0)
    return;
  let t = On;
  On = true;
  try {
    for (let n = e12.consumers; n !== void 0; n = n.nextConsumer) {
      let r = n.consumer;
      r.dirty || pd(r);
    }
  } finally {
    On = t;
  }
}
function So() {
  return V?.consumerAllowSignalWrites !== false;
}
function pd(e12) {
  e12.dirty = true, _o(e12), e12.consumerMarkedDirty?.(e12);
}
function Co(e12) {
  e12.dirty = false, e12.lastCleanEpoch = wo;
}
function Ut(e12) {
  return e12 && Ma(e12), g(e12);
}
function Ma(e12) {
  e12.producersTail = void 0, e12.recomputing = true;
}
function Ln(e12, t) {
  g(t), e12 && _a(e12);
}
function _a(e12) {
  e12.recomputing = false;
  let t = e12.producersTail, n = t !== void 0 ? t.nextProducer : e12.producers;
  if (n !== void 0) {
    if (ht(e12))
      do
        n = No(n);
      while (n !== void 0);
    t !== void 0 ? t.nextProducer = void 0 : e12.producers = void 0;
  }
}
function Fn(e12) {
  for (let t = e12.producers; t !== void 0; t = t.nextProducer) {
    let n = t.producer, r = t.lastReadVersion;
    if (r !== n.version || (Mo(n), r !== n.version))
      return true;
  }
  return false;
}
function pt(e12) {
  if (ht(e12)) {
    let t = e12.producers;
    for (; t !== void 0; )
      t = No(t);
  }
  e12.producers = void 0, e12.producersTail = void 0, e12.consumers = void 0, e12.consumersTail = void 0;
}
function Sa(e12, t) {
  let n = e12.consumersTail, r = ht(e12);
  if (n !== void 0 ? (t.nextConsumer = n.nextConsumer, n.nextConsumer = t) : (t.nextConsumer = void 0, e12.consumers = t), t.prevConsumer = n, e12.consumersTail = t, !r)
    for (let o = e12.producers; o !== void 0; o = o.nextProducer)
      Sa(o.producer, o);
}
function No(e12) {
  let t = e12.producer, n = e12.nextProducer, r = e12.nextConsumer, o = e12.prevConsumer;
  if (e12.nextConsumer = void 0, e12.prevConsumer = void 0, r !== void 0 ? r.prevConsumer = o : t.consumersTail = o, o !== void 0)
    o.nextConsumer = r;
  else if (t.consumers = r, !ht(t)) {
    let i = t.producers;
    for (; i !== void 0; )
      i = No(i);
  }
  return n;
}
function ht(e12) {
  return e12.consumerIsAlwaysLive || e12.consumers !== void 0;
}
function xo(e12) {
  fd?.(e12);
}
function hd(e12, t) {
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
function Ro(e12, t) {
  return Object.is(e12, t);
}
function jn(e12, t) {
  let n = Object.create(gd);
  n.computation = e12, t !== void 0 && (n.equal = t);
  let r = () => {
    if (Mo(n), To(n), n.value === kn)
      throw n.error;
    return n.value;
  };
  return r[Q] = n, xo(n), r;
}
var Do = Symbol("UNSET");
var bo = Symbol("COMPUTING");
var kn = Symbol("ERRORED");
var gd = R(N({}, ft), { value: Do, dirty: true, error: null, equal: Ro, kind: "computed", producerMustRecompute(e12) {
  return e12.value === Do || e12.value === bo;
}, producerRecomputeValue(e12) {
  if (e12.value === bo)
    throw new Error("");
  let t = e12.value;
  e12.value = bo;
  let n = Ut(e12), r, o = false;
  try {
    r = e12.computation(), g(null), o = t !== Do && t !== kn && r !== kn && e12.equal(t, r);
  } catch (i) {
    r = kn, e12.error = i;
  } finally {
    Ln(e12, n);
  }
  if (o) {
    e12.value = t;
    return;
  }
  e12.value = r, e12.version++;
} });
function md() {
  throw new Error();
}
var Na = md;
function xa(e12) {
  Na(e12);
}
function Ao(e12) {
  Na = e12;
}
var yd = null;
function Oo(e12, t) {
  let n = Object.create(Oa);
  n.value = e12, t !== void 0 && (n.equal = t);
  let r = () => Ra(n);
  return r[Q] = n, xo(n), [r, (s) => ko(n, s), (s) => Aa(n, s)];
}
function Ra(e12) {
  return To(e12), e12.value;
}
function ko(e12, t) {
  So() || xa(e12), e12.equal(e12.value, t) || (e12.value = t, vd(e12));
}
function Aa(e12, t) {
  So() || xa(e12), ko(e12, t(e12.value));
}
var Oa = R(N({}, ft), { equal: Ro, value: void 0, kind: "signal" });
function vd(e12) {
  e12.version++, Ta(), _o(e12), yd?.(e12);
}
var Po = R(N({}, ft), { consumerIsAlwaysLive: true, consumerAllowSignalWrites: true, dirty: true, kind: "effect" });
function Lo(e12) {
  if (e12.dirty = false, e12.version > 0 && !Fn(e12))
    return;
  e12.version++;
  let t = Ut(e12);
  try {
    e12.cleanup(), e12.fn();
  } finally {
    Ln(e12, t);
  }
}
function U(e12) {
  return typeof e12 == "function";
}
function Hn(e12) {
  let n = e12((r) => {
    Error.call(r), r.stack = new Error().stack;
  });
  return n.prototype = Object.create(Error.prototype), n.prototype.constructor = n, n;
}
var Vn = Hn((e12) => function(n) {
  e12(this), this.message = n ? `${n.length} errors occurred during unsubscription:
${n.map((r, o) => `${o + 1}) ${r.toString()}`).join(`
  `)}` : "", this.name = "UnsubscriptionError", this.errors = n;
});
function zt(e12, t) {
  if (e12) {
    let n = e12.indexOf(t);
    0 <= n && e12.splice(n, 1);
  }
}
var $ = class e {
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
      if (U(r))
        try {
          r();
        } catch (i) {
          t = i instanceof Vn ? i.errors : [i];
        }
      let { _finalizers: o } = this;
      if (o) {
        this._finalizers = null;
        for (let i of o)
          try {
            ka(i);
          } catch (s) {
            t = t ?? [], s instanceof Vn ? t = [...t, ...s.errors] : t.push(s);
          }
      }
      if (t)
        throw new Vn(t);
    }
  }
  add(t) {
    var n;
    if (t && t !== this)
      if (this.closed)
        ka(t);
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
    n === t ? this._parentage = null : Array.isArray(n) && zt(n, t);
  }
  remove(t) {
    let { _finalizers: n } = this;
    n && zt(n, t), t instanceof e && t._removeParent(this);
  }
};
$.EMPTY = (() => {
  let e12 = new $();
  return e12.closed = true, e12;
})();
var Fo = $.EMPTY;
function Bn(e12) {
  return e12 instanceof $ || e12 && "closed" in e12 && U(e12.remove) && U(e12.add) && U(e12.unsubscribe);
}
function ka(e12) {
  U(e12) ? e12() : e12.unsubscribe();
}
var ne = { onUnhandledError: null, onStoppedNotification: null, Promise: void 0, useDeprecatedSynchronousErrorHandling: false, useDeprecatedNextContext: false };
var gt = { setTimeout(e12, t, ...n) {
  let { delegate: r } = gt;
  return r?.setTimeout ? r.setTimeout(e12, t, ...n) : setTimeout(e12, t, ...n);
}, clearTimeout(e12) {
  let { delegate: t } = gt;
  return (t?.clearTimeout || clearTimeout)(e12);
}, delegate: void 0 };
function Pa(e12) {
  gt.setTimeout(() => {
    let { onUnhandledError: t } = ne;
    if (t)
      t(e12);
    else
      throw e12;
  });
}
function jo() {
}
var La = Ho("C", void 0, void 0);
function Fa(e12) {
  return Ho("E", void 0, e12);
}
function ja(e12) {
  return Ho("N", e12, void 0);
}
function Ho(e12, t, n) {
  return { kind: e12, value: t, error: n };
}
var Ge = null;
function mt(e12) {
  if (ne.useDeprecatedSynchronousErrorHandling) {
    let t = !Ge;
    if (t && (Ge = { errorThrown: false, error: null }), e12(), t) {
      let { errorThrown: n, error: r } = Ge;
      if (Ge = null, n)
        throw r;
    }
  } else
    e12();
}
function Ha(e12) {
  ne.useDeprecatedSynchronousErrorHandling && Ge && (Ge.errorThrown = true, Ge.error = e12);
}
var qe = class extends $ {
  constructor(t) {
    super(), this.isStopped = false, t ? (this.destination = t, Bn(t) && t.add(this)) : this.destination = Dd;
  }
  static create(t, n, r) {
    return new yt(t, n, r);
  }
  next(t) {
    this.isStopped ? Bo(ja(t), this) : this._next(t);
  }
  error(t) {
    this.isStopped ? Bo(Fa(t), this) : (this.isStopped = true, this._error(t));
  }
  complete() {
    this.isStopped ? Bo(La, this) : (this.isStopped = true, this._complete());
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
var Ed = Function.prototype.bind;
function Vo(e12, t) {
  return Ed.call(e12, t);
}
var $o = class {
  constructor(t) {
    this.partialObserver = t;
  }
  next(t) {
    let { partialObserver: n } = this;
    if (n.next)
      try {
        n.next(t);
      } catch (r) {
        $n(r);
      }
  }
  error(t) {
    let { partialObserver: n } = this;
    if (n.error)
      try {
        n.error(t);
      } catch (r) {
        $n(r);
      }
    else
      $n(t);
  }
  complete() {
    let { partialObserver: t } = this;
    if (t.complete)
      try {
        t.complete();
      } catch (n) {
        $n(n);
      }
  }
};
var yt = class extends qe {
  constructor(t, n, r) {
    super();
    let o;
    if (U(t) || !t)
      o = { next: t ?? void 0, error: n ?? void 0, complete: r ?? void 0 };
    else {
      let i;
      this && ne.useDeprecatedNextContext ? (i = Object.create(t), i.unsubscribe = () => this.unsubscribe(), o = { next: t.next && Vo(t.next, i), error: t.error && Vo(t.error, i), complete: t.complete && Vo(t.complete, i) }) : o = t;
    }
    this.destination = new $o(o);
  }
};
function $n(e12) {
  ne.useDeprecatedSynchronousErrorHandling ? Ha(e12) : Pa(e12);
}
function Id(e12) {
  throw e12;
}
function Bo(e12, t) {
  let { onStoppedNotification: n } = ne;
  n && gt.setTimeout(() => n(e12, t));
}
var Dd = { closed: true, next: jo, error: Id, complete: jo };
var Va = typeof Symbol == "function" && Symbol.observable || "@@observable";
function Ba(e12) {
  return e12;
}
function $a(e12) {
  return e12.length === 0 ? Ba : e12.length === 1 ? e12[0] : function(n) {
    return e12.reduce((r, o) => o(r), n);
  };
}
var vt = (() => {
  class e12 {
    constructor(n) {
      n && (this._subscribe = n);
    }
    lift(n) {
      let r = new e12();
      return r.source = this, r.operator = n, r;
    }
    subscribe(n, r, o) {
      let i = Cd(n) ? n : new yt(n, r, o);
      return mt(() => {
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
      return r = Ua(r), new r((o, i) => {
        let s = new yt({ next: (a) => {
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
    [Va]() {
      return this;
    }
    pipe(...n) {
      return $a(n)(this);
    }
    toPromise(n) {
      return n = Ua(n), new n((r, o) => {
        let i;
        this.subscribe((s) => i = s, (s) => o(s), () => r(i));
      });
    }
  }
  return e12.create = (t) => new e12(t), e12;
})();
function Ua(e12) {
  var t;
  return (t = e12 ?? ne.Promise) !== null && t !== void 0 ? t : Promise;
}
function bd(e12) {
  return e12 && U(e12.next) && U(e12.error) && U(e12.complete);
}
function Cd(e12) {
  return e12 && e12 instanceof qe || bd(e12) && Bn(e12);
}
function wd(e12) {
  return U(e12?.lift);
}
function za(e12) {
  return (t) => {
    if (wd(t))
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
function Wa(e12, t, n, r, o) {
  return new Uo(e12, t, n, r, o);
}
var Uo = class extends qe {
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
var Ga = Hn((e12) => function() {
  e12(this), this.name = "ObjectUnsubscribedError", this.message = "object unsubscribed";
});
var ve = (() => {
  class e12 extends vt {
    constructor() {
      super(), this.closed = false, this.currentObservers = null, this.observers = [], this.isStopped = false, this.hasError = false, this.thrownError = null;
    }
    lift(n) {
      let r = new Un(this, this);
      return r.operator = n, r;
    }
    _throwIfClosed() {
      if (this.closed)
        throw new Ga();
    }
    next(n) {
      mt(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.currentObservers || (this.currentObservers = Array.from(this.observers));
          for (let r of this.currentObservers)
            r.next(n);
        }
      });
    }
    error(n) {
      mt(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.hasError = this.isStopped = true, this.thrownError = n;
          let { observers: r } = this;
          for (; r.length; )
            r.shift().error(n);
        }
      });
    }
    complete() {
      mt(() => {
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
      return r || o ? Fo : (this.currentObservers = null, i.push(n), new $(() => {
        this.currentObservers = null, zt(i, n);
      }));
    }
    _checkFinalizedStatuses(n) {
      let { hasError: r, thrownError: o, isStopped: i } = this;
      r ? n.error(o) : i && n.complete();
    }
    asObservable() {
      let n = new vt();
      return n.source = this, n;
    }
  }
  return e12.create = (t, n) => new Un(t, n), e12;
})();
var Un = class extends ve {
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
    return (r = (n = this.source) === null || n === void 0 ? void 0 : n.subscribe(t)) !== null && r !== void 0 ? r : Fo;
  }
};
var Wt = class extends ve {
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
function zo(e12, t) {
  return za((n, r) => {
    let o = 0;
    n.subscribe(Wa(r, (i) => {
      r.next(e12.call(t, i, o++));
    }));
  });
}
var Wo;
function zn() {
  return Wo;
}
function le(e12) {
  let t = Wo;
  return Wo = e12, t;
}
var qa = Symbol("NotFound");
function Et(e12) {
  return e12 === qa || e12?.name === "\u0275NotFound";
}
var Jn = "https://angular.dev/best-practices/security#preventing-cross-site-scripting-xss";
var v = class extends Error {
  code;
  constructor(t, n) {
    super(Xn(t, n)), this.code = t;
  }
};
function Td(e12) {
  return `NG0${Math.abs(e12)}`;
}
function Xn(e12, t) {
  return `${Td(e12)}${t ? ": " + t : ""}`;
}
var Fe = globalThis;
function w(e12) {
  for (let t in e12)
    if (e12[t] === w)
      return t;
  throw Error("");
}
function er(e12) {
  if (typeof e12 == "string")
    return e12;
  if (Array.isArray(e12))
    return `[${e12.map(er).join(", ")}]`;
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
function ii(e12, t) {
  return e12 ? t ? `${e12} ${t}` : e12 : t || "";
}
var Md = w({ __forward_ref__: w });
function tr(e12) {
  return e12.__forward_ref__ = tr, e12;
}
function q(e12) {
  return Ja(e12) ? e12() : e12;
}
function Ja(e12) {
  return typeof e12 == "function" && e12.hasOwnProperty(Md) && e12.__forward_ref__ === tr;
}
function _(e12) {
  return { token: e12.token, providedIn: e12.providedIn || null, factory: e12.factory, value: void 0 };
}
function nr(e12) {
  return _d(e12, rr);
}
function _d(e12, t) {
  return e12.hasOwnProperty(t) && e12[t] || null;
}
function Sd(e12) {
  let t = e12?.[rr] ?? null;
  return t || null;
}
function qo(e12) {
  return e12 && e12.hasOwnProperty(Gn) ? e12[Gn] : null;
}
var rr = w({ \u0275prov: w });
var Gn = w({ \u0275inj: w });
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
function si(e12) {
  return e12 && !!e12.\u0275providers;
}
var ai = w({ \u0275cmp: w });
var ci = w({ \u0275dir: w });
var li = w({ \u0275pipe: w });
var Zo = w({ \u0275fac: w });
var Je = w({ __NG_ELEMENT_ID__: w });
var Za = w({ __NG_ENV_ID__: w });
function Xe(e12) {
  return di(e12, "@Component"), e12[ai] || null;
}
function ui(e12) {
  return di(e12, "@Directive"), e12[ci] || null;
}
function Xa(e12) {
  return di(e12, "@Pipe"), e12[li] || null;
}
function di(e12, t) {
  if (e12 == null)
    throw new v(-919, false);
}
function fi(e12) {
  return typeof e12 == "string" ? e12 : e12 == null ? "" : String(e12);
}
var ec = w({ ngErrorCode: w });
var Nd = w({ ngErrorMessage: w });
var xd = w({ ngTokenPath: w });
function pi(e12, t) {
  return tc("", -200, t);
}
function or(e12, t) {
  throw new v(-201, false);
}
function tc(e12, t, n) {
  let r = new v(t, e12);
  return r[ec] = t, r[Nd] = e12, n && (r[xd] = n), r;
}
function Rd(e12) {
  return e12[ec];
}
var Qo;
function nc() {
  return Qo;
}
function G(e12) {
  let t = Qo;
  return Qo = e12, t;
}
function hi(e12, t, n) {
  let r = nr(e12);
  if (r && r.providedIn == "root")
    return r.value === void 0 ? r.value = r.factory() : r.value;
  if (n & 8)
    return null;
  if (t !== void 0)
    return t;
  or(e12, "");
}
var Ad = {};
var Ze = Ad;
var Od = "__NG_DI_FLAG__";
var Yo = class {
  injector;
  constructor(t) {
    this.injector = t;
  }
  retrieve(t, n) {
    let r = Qe(n) || 0;
    try {
      return this.injector.get(t, r & 8 ? null : Ze, r);
    } catch (o) {
      if (Et(o))
        return o;
      throw o;
    }
  }
};
function kd(e12, t = 0) {
  let n = zn();
  if (n === void 0)
    throw new v(-203, false);
  if (n === null)
    return hi(e12, void 0, t);
  {
    let r = Pd(t), o = n.retrieve(e12, r);
    if (Et(o)) {
      if (r.optional)
        return null;
      throw o;
    }
    return o;
  }
}
function b(e12, t = 0) {
  return (nc() || kd)(q(e12), t);
}
function E(e12, t) {
  return b(e12, Qe(t));
}
function Qe(e12) {
  return typeof e12 > "u" || typeof e12 == "number" ? e12 : 0 | (e12.optional && 8) | (e12.host && 1) | (e12.self && 2) | (e12.skipSelf && 4);
}
function Pd(e12) {
  return { optional: !!(e12 & 8), host: !!(e12 & 1), self: !!(e12 & 2), skipSelf: !!(e12 & 4) };
}
function Ko(e12) {
  let t = [];
  for (let n = 0; n < e12.length; n++) {
    let r = q(e12[n]);
    if (Array.isArray(r)) {
      if (r.length === 0)
        throw new v(900, false);
      let o, i = 0;
      for (let s = 0; s < r.length; s++) {
        let a = r[s], c = Ld(a);
        typeof c == "number" ? c === -1 ? o = a.token : i |= c : o = a;
      }
      t.push(b(o, i));
    } else
      t.push(b(r));
  }
  return t;
}
function Ld(e12) {
  return e12[Od];
}
function Dt(e12, t) {
  let n = e12.hasOwnProperty(Zo);
  return n ? e12[Zo] : null;
}
function rc(e12, t, n) {
  if (e12.length !== t.length)
    return false;
  for (let r = 0; r < e12.length; r++) {
    let o = e12[r], i = t[r];
    if (n && (o = n(o), i = n(i)), i !== o)
      return false;
  }
  return true;
}
function oc(e12) {
  return e12.flat(Number.POSITIVE_INFINITY);
}
function ir(e12, t) {
  e12.forEach((n) => Array.isArray(n) ? ir(n, t) : t(n));
}
function gi(e12, t, n) {
  t >= e12.length ? e12.push(n) : e12.splice(t, 0, n);
}
function Kt(e12, t) {
  return t >= e12.length - 1 ? e12.pop() : e12.splice(t, 1)[0];
}
function ic(e12, t, n, r) {
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
function sc(e12, t, n) {
  let r = bt(e12, t);
  return r >= 0 ? e12[r | 1] = n : (r = ~r, ic(e12, r, t, n)), r;
}
function sr(e12, t) {
  let n = bt(e12, t);
  if (n >= 0)
    return e12[n | 1];
}
function bt(e12, t) {
  return Fd(e12, t, 1);
}
function Fd(e12, t, n) {
  let r = 0, o = e12.length >> n;
  for (; o !== r; ) {
    let i = r + (o - r >> 1), s = e12[i << n];
    if (t === s)
      return i << n;
    s > t ? o = i : r = i + 1;
  }
  return ~(o << n);
}
var et = {};
var ke = [];
var tt = new D("");
var mi = new D("", -1);
var yi = new D("");
var qt = class {
  get(t, n = Ze) {
    if (n === Ze) {
      let o = tc("", -201);
      throw o.name = "\u0275NotFound", o;
    }
    return n;
  }
};
function Jt(e12) {
  return { \u0275providers: e12 };
}
function ac(e12) {
  return Jt([{ provide: tt, multi: true, useValue: e12 }]);
}
function cc(...e12) {
  return { \u0275providers: vi(true, e12), \u0275fromNgModule: true };
}
function vi(e12, ...t) {
  let n = [], r = /* @__PURE__ */ new Set(), o, i = (s) => {
    n.push(s);
  };
  return ir(t, (s) => {
    let a = s;
    qn(a, i, [], r) && (o ||= [], o.push(a));
  }), o !== void 0 && lc(o, i), n;
}
function lc(e12, t) {
  for (let n = 0; n < e12.length; n++) {
    let { ngModule: r, providers: o } = e12[n];
    Ei(o, (i) => {
      t(i, r);
    });
  }
}
function qn(e12, t, n, r) {
  if (e12 = q(e12), !e12)
    return false;
  let o = null, i = qo(e12), s = !i && Xe(e12);
  if (!i && !s) {
    let c = e12.ngModule;
    if (i = qo(c), i)
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
        qn(l, t, n, r);
    }
  } else if (i) {
    if (i.imports != null && !a) {
      r.add(o);
      let l;
      ir(i.imports, (u) => {
        qn(u, t, n, r) && (l ||= [], l.push(u));
      }), l !== void 0 && lc(l, t);
    }
    if (!a) {
      let l = Dt(o) || (() => new o());
      t({ provide: o, useFactory: l, deps: ke }, o), t({ provide: yi, useValue: o, multi: true }, o), t({ provide: tt, useValue: () => b(o), multi: true }, o);
    }
    let c = i.providers;
    if (c != null && !a) {
      let l = e12;
      Ei(c, (u) => {
        t(u, l);
      });
    }
  } else
    return false;
  return o !== e12 && e12.providers !== void 0;
}
function Ei(e12, t) {
  for (let n of e12)
    si(n) && (n = n.\u0275providers), Array.isArray(n) ? Ei(n, t) : t(n);
}
var jd = w({ provide: String, useValue: w });
function uc(e12) {
  return e12 !== null && typeof e12 == "object" && jd in e12;
}
function Hd(e12) {
  return !!(e12 && e12.useExisting);
}
function Vd(e12) {
  return !!(e12 && e12.useFactory);
}
function Zn(e12) {
  return typeof e12 == "function";
}
var Xt = new D("");
var Wn = {};
var Qa = {};
var Go;
function en() {
  return Go === void 0 && (Go = new qt()), Go;
}
var Y = class {
};
var Ye = class extends Y {
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
    super(), this.parent = n, this.source = r, this.scopes = o, Xo(t, (s) => this.processProvider(s)), this.records.set(mi, It(void 0, this)), o.has("environment") && this.records.set(Y, It(void 0, this));
    let i = this.records.get(Xt);
    i != null && typeof i.value == "string" && this.scopes.add(i.value), this.injectorDefTypes = new Set(this.get(yi, ke, { self: true }));
  }
  retrieve(t, n) {
    let r = Qe(n) || 0;
    try {
      return this.get(t, Ze, r);
    } catch (o) {
      if (Et(o))
        return o;
      throw o;
    }
  }
  destroy() {
    Gt(this), this._destroyed = true;
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
    return Gt(this), this._onDestroyHooks.push(t), () => this.removeOnDestroy(t);
  }
  runInContext(t) {
    Gt(this);
    let n = le(this), r = G(void 0), o;
    try {
      return t();
    } finally {
      le(n), G(r);
    }
  }
  get(t, n = Ze, r) {
    if (Gt(this), t.hasOwnProperty(Za))
      return t[Za](this);
    let o = Qe(r), i, s = le(this), a = G(void 0);
    try {
      if (!(o & 4)) {
        let l = this.records.get(t);
        if (l === void 0) {
          let u = Wd(t) && nr(t);
          u && this.injectableDefInScope(u) ? l = It(Jo(t), Wn) : l = null, this.records.set(t, l);
        }
        if (l != null)
          return this.hydrate(t, l, o);
      }
      let c = o & 2 ? en() : this.parent;
      return n = o & 8 && n === Ze ? null : n, c.get(t, n);
    } catch (c) {
      let l = Rd(c);
      throw l === -200 || l === -201 ? new v(l, null) : c;
    } finally {
      G(a), le(s);
    }
  }
  resolveInjectorInitializers() {
    let t = g(null), n = le(this), r = G(void 0), o;
    try {
      let i = this.get(tt, ke, { self: true });
      for (let s of i)
        s();
    } finally {
      le(n), G(r), g(t);
    }
  }
  toString() {
    return "R3Injector[...]";
  }
  processProvider(t) {
    t = q(t);
    let n = Zn(t) ? t : q(t && t.provide), r = $d(t);
    if (!Zn(t) && t.multi === true) {
      let o = this.records.get(n);
      o || (o = It(void 0, Wn, true), o.factory = () => Ko(o.multi), this.records.set(n, o)), n = t, o.multi.push(t);
    }
    this.records.set(n, r);
  }
  hydrate(t, n, r) {
    let o = g(null);
    try {
      if (n.value === Qa)
        throw pi("");
      return n.value === Wn && (n.value = Qa, n.value = n.factory(void 0, r)), typeof n.value == "object" && n.value && zd(n.value) && this._ngOnDestroyHooks.add(n.value), n.value;
    } finally {
      g(o);
    }
  }
  injectableDefInScope(t) {
    if (!t.providedIn)
      return false;
    let n = q(t.providedIn);
    return typeof n == "string" ? n === "any" || this.scopes.has(n) : this.injectorDefTypes.has(n);
  }
  removeOnDestroy(t) {
    let n = this._onDestroyHooks.indexOf(t);
    n !== -1 && this._onDestroyHooks.splice(n, 1);
  }
};
function Jo(e12) {
  let t = nr(e12), n = t !== null ? t.factory : Dt(e12);
  if (n !== null)
    return n;
  if (e12 instanceof D)
    throw new v(-204, false);
  if (e12 instanceof Function)
    return Bd(e12);
  throw new v(-204, false);
}
function Bd(e12) {
  if (e12.length > 0)
    throw new v(-204, false);
  let n = Sd(e12);
  return n !== null ? () => n.factory(e12) : () => new e12();
}
function $d(e12) {
  if (uc(e12))
    return It(void 0, e12.useValue);
  {
    let t = dc(e12);
    return It(t, Wn);
  }
}
function dc(e12, t, n) {
  let r;
  if (Zn(e12)) {
    let o = q(e12);
    return Dt(o) || Jo(o);
  } else if (uc(e12))
    r = () => q(e12.useValue);
  else if (Vd(e12))
    r = () => e12.useFactory(...Ko(e12.deps || []));
  else if (Hd(e12))
    r = (o, i) => b(q(e12.useExisting), i !== void 0 && i & 8 ? 8 : void 0);
  else {
    let o = q(e12 && (e12.useClass || e12.provide));
    if (Ud(e12))
      r = () => new o(...Ko(e12.deps));
    else
      return Dt(o) || Jo(o);
  }
  return r;
}
function Gt(e12) {
  if (e12.destroyed)
    throw new v(-205, false);
}
function It(e12, t, n = false) {
  return { factory: e12, value: t, multi: n ? [] : void 0 };
}
function Ud(e12) {
  return !!e12.deps;
}
function zd(e12) {
  return e12 !== null && typeof e12 == "object" && typeof e12.ngOnDestroy == "function";
}
function Wd(e12) {
  return typeof e12 == "function" || typeof e12 == "object" && e12.ngMetadataName === "InjectionToken";
}
function Xo(e12, t) {
  for (let n of e12)
    Array.isArray(n) ? Xo(n, t) : n && si(n) ? Xo(n.\u0275providers, t) : t(n);
}
function ar(e12, t) {
  let n;
  e12 instanceof Ye ? (Gt(e12), n = e12) : n = new Yo(e12);
  let r, o = le(n), i = G(void 0);
  try {
    return t();
  } finally {
    le(o), G(i);
  }
}
function fc() {
  return nc() !== void 0 || zn() != null;
}
var re = 0;
var m = 1;
var y = 2;
var A = 3;
var J = 4;
var X = 5;
var Ct = 6;
var wt = 7;
var x = 8;
var be = 9;
var de = 10;
var O = 11;
var Tt = 12;
var Ii = 13;
var nt = 14;
var ee = 15;
var je = 16;
var rt = 17;
var fe = 18;
var Ce = 19;
var Di = 20;
var Ie = 21;
var cr = 22;
var Pe = 23;
var Z = 24;
var lr = 25;
var He = 26;
var B = 27;
var pc = 1;
var bi = 6;
var Ve = 7;
var tn = 8;
var ot = 9;
var S = 10;
function Be(e12) {
  return Array.isArray(e12) && typeof e12[pc] == "object";
}
function oe(e12) {
  return Array.isArray(e12) && e12[pc] === true;
}
function Ci(e12) {
  return (e12.flags & 4) !== 0;
}
function Mt(e12) {
  return e12.componentOffset > -1;
}
function wi(e12) {
  return (e12.flags & 1) === 1;
}
function _t(e12) {
  return !!e12.template;
}
function St(e12) {
  return (e12[y] & 512) !== 0;
}
function it(e12) {
  return (e12[y] & 256) === 256;
}
var hc = "svg";
var gc = "math";
function te(e12) {
  for (; Array.isArray(e12); )
    e12 = e12[re];
  return e12;
}
function Ti(e12, t) {
  return te(t[e12]);
}
function pe(e12, t) {
  return te(t[e12.index]);
}
function ur(e12, t) {
  return e12.data[t];
}
function we(e12, t) {
  let n = t[e12];
  return Be(n) ? n : n[re];
}
function mc(e12) {
  return (e12[y] & 4) === 4;
}
function dr(e12) {
  return (e12[y] & 128) === 128;
}
function yc(e12) {
  return oe(e12[A]);
}
function he(e12, t) {
  return t == null ? null : e12[t];
}
function Mi(e12) {
  e12[rt] = 0;
}
function _i(e12) {
  e12[y] & 1024 || (e12[y] |= 1024, dr(e12) && Nt(e12));
}
function vc(e12, t) {
  for (; e12 > 0; )
    t = t[nt], e12--;
  return t;
}
function nn(e12) {
  return !!(e12[y] & 9216 || e12[Z]?.dirty);
}
function fr(e12) {
  e12[de].changeDetectionScheduler?.notify(8), e12[y] & 64 && (e12[y] |= 1024), nn(e12) && Nt(e12);
}
function Nt(e12) {
  e12[de].changeDetectionScheduler?.notify(0);
  let t = Le(e12);
  for (; t !== null && !(t[y] & 8192 || (t[y] |= 8192, !dr(t))); )
    t = Le(t);
}
function Si(e12, t) {
  if (it(e12))
    throw new v(911, false);
  e12[Ie] === null && (e12[Ie] = []), e12[Ie].push(t);
}
function Ec(e12, t) {
  if (e12[Ie] === null)
    return;
  let n = e12[Ie].indexOf(t);
  n !== -1 && e12[Ie].splice(n, 1);
}
function Le(e12) {
  let t = e12[A];
  return oe(t) ? t[A] : t;
}
function Ni(e12) {
  return e12[wt] ??= [];
}
function xi(e12) {
  return e12.cleanup ??= [];
}
function Ic(e12, t, n, r) {
  let o = Ni(t);
  o.push(n), e12.firstCreatePass && xi(e12).push(r, o.length - 1);
}
var I = { lFrame: Lc(null), bindingsEnabled: true, skipHydrationRootTNode: null };
var ei = false;
function Dc() {
  return I.lFrame.elementDepthCount;
}
function bc() {
  I.lFrame.elementDepthCount++;
}
function Cc() {
  I.lFrame.elementDepthCount--;
}
function wc() {
  return I.skipHydrationRootTNode !== null;
}
function Tc(e12) {
  return I.skipHydrationRootTNode === e12;
}
function Mc() {
  I.skipHydrationRootTNode = null;
}
function M() {
  return I.lFrame.lView;
}
function ie() {
  return I.lFrame.tView;
}
function Te(e12) {
  return I.lFrame.contextLView = e12, e12[x];
}
function Me(e12) {
  return I.lFrame.contextLView = null, e12;
}
function ge() {
  let e12 = Ri();
  for (; e12 !== null && e12.type === 64; )
    e12 = e12.parent;
  return e12;
}
function Ri() {
  return I.lFrame.currentTNode;
}
function _c() {
  let e12 = I.lFrame, t = e12.currentTNode;
  return e12.isParent ? t : t.parent;
}
function xt(e12, t) {
  let n = I.lFrame;
  n.currentTNode = e12, n.isParent = t;
}
function Ai() {
  return I.lFrame.isParent;
}
function Sc() {
  I.lFrame.isParent = false;
}
function Oi() {
  return ei;
}
function Zt(e12) {
  let t = ei;
  return ei = e12, t;
}
function Nc(e12) {
  return I.lFrame.bindingIndex = e12;
}
function rn() {
  return I.lFrame.bindingIndex++;
}
function xc(e12) {
  let t = I.lFrame, n = t.bindingIndex;
  return t.bindingIndex = t.bindingIndex + e12, n;
}
function Rc() {
  return I.lFrame.inI18n;
}
function Ac(e12, t) {
  let n = I.lFrame;
  n.bindingIndex = n.bindingRootIndex = e12, pr(t);
}
function Oc() {
  return I.lFrame.currentDirectiveIndex;
}
function pr(e12) {
  I.lFrame.currentDirectiveIndex = e12;
}
function kc(e12) {
  let t = I.lFrame.currentDirectiveIndex;
  return t === -1 ? null : e12[t];
}
function ki() {
  return I.lFrame.currentQueryIndex;
}
function hr(e12) {
  I.lFrame.currentQueryIndex = e12;
}
function Gd(e12) {
  let t = e12[m];
  return t.type === 2 ? t.declTNode : t.type === 1 ? e12[X] : null;
}
function Pi(e12, t, n) {
  if (n & 4) {
    let o = t, i = e12;
    for (; o = o.parent, o === null && !(n & 1); )
      if (o = Gd(i), o === null || (i = i[nt], o.type & 10))
        break;
    if (o === null)
      return false;
    t = o, e12 = i;
  }
  let r = I.lFrame = Pc();
  return r.currentTNode = t, r.lView = e12, true;
}
function gr(e12) {
  let t = Pc(), n = e12[m];
  I.lFrame = t, t.currentTNode = n.firstChild, t.lView = e12, t.tView = n, t.contextLView = e12, t.bindingIndex = n.bindingStartIndex, t.inI18n = false;
}
function Pc() {
  let e12 = I.lFrame, t = e12 === null ? null : e12.child;
  return t === null ? Lc(e12) : t;
}
function Lc(e12) {
  let t = { currentTNode: null, isParent: true, lView: null, tView: null, selectedIndex: -1, contextLView: null, elementDepthCount: 0, currentNamespace: null, currentDirectiveIndex: -1, bindingRootIndex: -1, bindingIndex: -1, currentQueryIndex: 0, parent: e12, child: null, inI18n: false };
  return e12 !== null && (e12.child = t), t;
}
function Fc() {
  let e12 = I.lFrame;
  return I.lFrame = e12.parent, e12.currentTNode = null, e12.lView = null, e12;
}
var Li = Fc;
function mr() {
  let e12 = Fc();
  e12.isParent = true, e12.tView = null, e12.selectedIndex = -1, e12.contextLView = null, e12.elementDepthCount = 0, e12.currentDirectiveIndex = -1, e12.currentNamespace = null, e12.bindingRootIndex = -1, e12.bindingIndex = -1, e12.currentQueryIndex = 0;
}
function jc(e12) {
  return (I.lFrame.contextLView = vc(e12, I.lFrame.contextLView))[x];
}
function $e() {
  return I.lFrame.selectedIndex;
}
function Ue(e12) {
  I.lFrame.selectedIndex = e12;
}
function Hc() {
  let e12 = I.lFrame;
  return ur(e12.tView, e12.selectedIndex);
}
function Vc() {
  return I.lFrame.currentNamespace;
}
var Bc = true;
function yr() {
  return Bc;
}
function vr(e12) {
  Bc = e12;
}
function ti(e12, t = null, n = null, r) {
  let o = $c(e12, t, n, r);
  return o.resolveInjectorInitializers(), o;
}
function $c(e12, t = null, n = null, r, o = /* @__PURE__ */ new Set()) {
  let i = [n || ke, cc(e12)], s;
  return new Ye(i, t || en(), s || null, o);
}
var ue = class e2 {
  static THROW_IF_NOT_FOUND = Ze;
  static NULL = new qt();
  static create(t, n) {
    if (Array.isArray(t))
      return ti({ name: "" }, n, t, "");
    {
      let r = t.name ?? "";
      return ti({ name: r }, t.parent, t.providers, r);
    }
  }
  static \u0275prov = _({ token: e2, providedIn: "any", factory: () => b(mi) });
  static __NG_ELEMENT_ID__ = -1;
};
var z = new D("");
var Rt = /* @__PURE__ */ (() => {
  class e12 {
    static __NG_ELEMENT_ID__ = qd;
    static __NG_ENV_ID__ = (n) => n;
  }
  return e12;
})();
var Qn = class extends Rt {
  _lView;
  constructor(t) {
    super(), this._lView = t;
  }
  get destroyed() {
    return it(this._lView);
  }
  onDestroy(t) {
    let n = this._lView;
    return Si(n, t), () => Ec(n, t);
  }
};
function qd() {
  return new Qn(M());
}
var Uc = false;
var zc = new D("");
var At = (() => {
  class e12 {
    taskId = 0;
    pendingTasks = /* @__PURE__ */ new Set();
    destroyed = false;
    pendingTask = new Wt(false);
    debugTaskTracker = E(zc, { optional: true });
    get hasPendingTasks() {
      return this.destroyed ? false : this.pendingTask.value;
    }
    get hasPendingTasksObservable() {
      return this.destroyed ? new vt((n) => {
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
var ni = class extends ve {
  __isAsync;
  destroyRef = void 0;
  pendingTasks = void 0;
  constructor(t = false) {
    super(), this.__isAsync = t, fc() && (this.destroyRef = E(Rt, { optional: true }) ?? void 0, this.pendingTasks = E(At, { optional: true }) ?? void 0);
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
    return t instanceof $ && t.add(a), a;
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
var Ee = ni;
function Yn(...e12) {
}
function Fi(e12) {
  let t, n;
  function r() {
    e12 = Yn;
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
function Wc(e12) {
  return queueMicrotask(() => e12()), () => {
    e12 = Yn;
  };
}
var ji = "isAngularZone";
var Qt = ji + "_ID";
var Zd = 0;
var K = class e3 {
  hasPendingMacrotasks = false;
  hasPendingMicrotasks = false;
  isStable = true;
  onUnstable = new Ee(false);
  onMicrotaskEmpty = new Ee(false);
  onStable = new Ee(false);
  onError = new Ee(false);
  constructor(t) {
    let { enableLongStackTrace: n = false, shouldCoalesceEventChangeDetection: r = false, shouldCoalesceRunChangeDetection: o = false, scheduleInRootZone: i = Uc } = t;
    if (typeof Zone > "u")
      throw new v(908, false);
    Zone.assertZonePatched();
    let s = this;
    s._nesting = 0, s._outer = s._inner = Zone.current, Zone.TaskTrackingZoneSpec && (s._inner = s._inner.fork(new Zone.TaskTrackingZoneSpec())), n && Zone.longStackTraceZoneSpec && (s._inner = s._inner.fork(Zone.longStackTraceZoneSpec)), s.shouldCoalesceEventChangeDetection = !o && r, s.shouldCoalesceRunChangeDetection = o, s.callbackScheduled = false, s.scheduleInRootZone = i, Kd(s);
  }
  static isInAngularZone() {
    return typeof Zone < "u" && Zone.current.get(ji) === true;
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
    let i = this._inner, s = i.scheduleEventTask("NgZoneEvent: " + o, t, Qd, Yn, Yn);
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
var Qd = {};
function Hi(e12) {
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
function Yd(e12) {
  if (e12.isCheckStableRunning || e12.callbackScheduled)
    return;
  e12.callbackScheduled = true;
  function t() {
    Fi(() => {
      e12.callbackScheduled = false, ri(e12), e12.isCheckStableRunning = true, Hi(e12), e12.isCheckStableRunning = false;
    });
  }
  e12.scheduleInRootZone ? Zone.root.run(() => {
    t();
  }) : e12._outer.run(() => {
    t();
  }), ri(e12);
}
function Kd(e12) {
  let t = () => {
    Yd(e12);
  }, n = Zd++;
  e12._inner = e12._inner.fork({ name: "angular", properties: { [ji]: true, [Qt]: n, [Qt + n]: true }, onInvokeTask: (r, o, i, s, a, c) => {
    if (Jd(c))
      return r.invokeTask(i, s, a, c);
    try {
      return Ya(e12), r.invokeTask(i, s, a, c);
    } finally {
      (e12.shouldCoalesceEventChangeDetection && s.type === "eventTask" || e12.shouldCoalesceRunChangeDetection) && t(), Ka(e12);
    }
  }, onInvoke: (r, o, i, s, a, c, l) => {
    try {
      return Ya(e12), r.invoke(i, s, a, c, l);
    } finally {
      e12.shouldCoalesceRunChangeDetection && !e12.callbackScheduled && !Xd(c) && t(), Ka(e12);
    }
  }, onHasTask: (r, o, i, s) => {
    r.hasTask(i, s), o === i && (s.change == "microTask" ? (e12._hasPendingMicrotasks = s.microTask, ri(e12), Hi(e12)) : s.change == "macroTask" && (e12.hasPendingMacrotasks = s.macroTask));
  }, onHandleError: (r, o, i, s) => (r.handleError(i, s), e12.runOutsideAngular(() => e12.onError.emit(s)), false) });
}
function ri(e12) {
  e12._hasPendingMicrotasks || (e12.shouldCoalesceEventChangeDetection || e12.shouldCoalesceRunChangeDetection) && e12.callbackScheduled === true ? e12.hasPendingMicrotasks = true : e12.hasPendingMicrotasks = false;
}
function Ya(e12) {
  e12._nesting++, e12.isStable && (e12.isStable = false, e12.onUnstable.emit(null));
}
function Ka(e12) {
  e12._nesting--, Hi(e12);
}
var Yt = class {
  hasPendingMicrotasks = false;
  hasPendingMacrotasks = false;
  isStable = true;
  onUnstable = new Ee();
  onMicrotaskEmpty = new Ee();
  onStable = new Ee();
  onError = new Ee();
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
function Jd(e12) {
  return Gc(e12, "__ignore_ng_zone__");
}
function Xd(e12) {
  return Gc(e12, "__scheduler_tick__");
}
function Gc(e12, t) {
  return !Array.isArray(e12) || e12.length !== 1 ? false : e12[0]?.data?.[t] === true;
}
var De = class {
  _console = console;
  handleError(t) {
    this._console.error("ERROR", t);
  }
};
var st = new D("", { factory: () => {
  let e12 = E(K), t = E(Y), n;
  return (r) => {
    e12.runOutsideAngular(() => {
      t.destroyed && !n ? setTimeout(() => {
        throw r;
      }) : (n ??= t.get(De), n.handleError(r));
    });
  };
} });
var qc = { provide: tt, useValue: () => {
  let e12 = E(De, { optional: true });
}, multi: true };
var ef = new D("", { factory: () => {
  let e12 = E(z).defaultView;
  if (!e12)
    return;
  let t = E(st), n = (i) => {
    t(i.reason), i.preventDefault();
  }, r = (i) => {
    i.error ? t(i.error) : t(new Error(i.message, { cause: i })), i.preventDefault();
  }, o = () => {
    e12.addEventListener("unhandledrejection", n), e12.addEventListener("error", r);
  };
  typeof Zone < "u" ? Zone.root.run(o) : o(), E(Rt).onDestroy(() => {
    e12.removeEventListener("error", r), e12.removeEventListener("unhandledrejection", n);
  });
} });
function Vi() {
  return Jt([ac(() => {
    E(ef);
  })]);
}
function j(e12, t) {
  let [n, r, o] = Oo(e12, t?.equal), i = n, s = i[Q];
  return i.set = r, i.update = o, i.asReadonly = Zc.bind(i), i;
}
function Zc() {
  let e12 = this[Q];
  if (e12.readonlyFn === void 0) {
    let t = () => this();
    t[Q] = e12, e12.readonlyFn = t;
  }
  return e12.readonlyFn;
}
var Er = /* @__PURE__ */ (() => {
  class e12 {
    view;
    node;
    constructor(n, r) {
      this.view = n, this.node = r;
    }
    static __NG_ELEMENT_ID__ = tf;
  }
  return e12;
})();
function tf() {
  return new Er(M(), ge());
}
var Ke = class {
};
var on = new D("", { factory: () => true });
var Bi = new D("");
var Ir = (() => {
  class e12 {
    static \u0275prov = _({ token: e12, providedIn: "root", factory: () => new oi() });
  }
  return e12;
})();
var oi = class {
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
var Kn = class {
  [Q];
  constructor(t) {
    this[Q] = t;
  }
  destroy() {
    this[Q].destroy();
  }
};
function $i(e12, t) {
  let n = t?.injector ?? E(ue), r = t?.manualCleanup !== true ? n.get(Rt) : null, o, i = n.get(Er, null, { optional: true }), s = n.get(Ke);
  return i !== null ? (o = of(i.view, s, e12), r instanceof Qn && r._lView === i.view && (r = null)) : o = sf(e12, n.get(Ir), s), o.injector = n, r !== null && (o.onDestroyFns = [r.onDestroy(() => o.destroy())]), new Kn(o);
}
var Qc = R(N({}, Po), { cleanupFns: void 0, zone: null, onDestroyFns: null, run() {
  let e12 = Zt(false);
  try {
    Lo(this);
  } finally {
    Zt(e12);
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
var nf = R(N({}, Qc), { consumerMarkedDirty() {
  this.scheduler.schedule(this), this.notifier.notify(12);
}, destroy() {
  if (pt(this), this.onDestroyFns !== null)
    for (let e12 of this.onDestroyFns)
      e12();
  this.cleanup(), this.scheduler.remove(this);
} });
var rf = R(N({}, Qc), { consumerMarkedDirty() {
  this.view[y] |= 8192, Nt(this.view), this.notifier.notify(13);
}, destroy() {
  if (pt(this), this.onDestroyFns !== null)
    for (let e12 of this.onDestroyFns)
      e12();
  this.cleanup(), this.view[Pe]?.delete(this);
} });
function of(e12, t, n) {
  let r = Object.create(rf);
  return r.view = e12, r.zone = typeof Zone < "u" ? Zone.current : null, r.notifier = t, r.fn = Yc(r, n), e12[Pe] ??= /* @__PURE__ */ new Set(), e12[Pe].add(r), r.consumerMarkedDirty(r), r;
}
function sf(e12, t, n) {
  let r = Object.create(nf);
  return r.fn = Yc(r, e12), r.scheduler = t, r.notifier = n, r.zone = typeof Zone < "u" ? Zone.current : null, r.scheduler.add(r), r.notifier.notify(12), r;
}
function Yc(e12, t) {
  return () => {
    t((n) => (e12.cleanupFns ??= []).push(n));
  };
}
function _l(e12) {
  return { toString: e12 }.toString();
}
function Ef(e12) {
  return typeof e12 == "function";
}
function Sl(e12, t, n, r) {
  t !== null ? t.applyValueToInputSignal(t, r) : e12[n] = r;
}
var Nr = class {
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
function If(e12) {
  return e12.type.prototype.ngOnChanges && (e12.setInput = bf), Df;
}
function Df() {
  let e12 = xl(this), t = e12?.current;
  if (t) {
    let n = e12.previous;
    if (n === et)
      e12.previous = t;
    else
      for (let r in t)
        n[r] = t[r];
    e12.current = null, this.ngOnChanges(t);
  }
}
function bf(e12, t, n, r, o) {
  let i = this.declaredInputs[r], s = xl(e12) || Cf(e12, { previous: et, current: null }), a = s.current || (s.current = {}), c = s.previous, l = c[i];
  a[i] = new Nr(l && l.currentValue, n, c === et), Sl(e12, t, o, n);
}
var Nl = "__ngSimpleChanges__";
function xl(e12) {
  return e12[Nl] || null;
}
function Cf(e12, t) {
  return e12[Nl] = t;
}
var Kc = [];
var T = function(e12, t = null, n) {
  for (let r = 0; r < Kc.length; r++) {
    let o = Kc[r];
    o(e12, t, n);
  }
};
var C = function(e12) {
  return e12[e12.TemplateCreateStart = 0] = "TemplateCreateStart", e12[e12.TemplateCreateEnd = 1] = "TemplateCreateEnd", e12[e12.TemplateUpdateStart = 2] = "TemplateUpdateStart", e12[e12.TemplateUpdateEnd = 3] = "TemplateUpdateEnd", e12[e12.LifecycleHookStart = 4] = "LifecycleHookStart", e12[e12.LifecycleHookEnd = 5] = "LifecycleHookEnd", e12[e12.OutputStart = 6] = "OutputStart", e12[e12.OutputEnd = 7] = "OutputEnd", e12[e12.BootstrapApplicationStart = 8] = "BootstrapApplicationStart", e12[e12.BootstrapApplicationEnd = 9] = "BootstrapApplicationEnd", e12[e12.BootstrapComponentStart = 10] = "BootstrapComponentStart", e12[e12.BootstrapComponentEnd = 11] = "BootstrapComponentEnd", e12[e12.ChangeDetectionStart = 12] = "ChangeDetectionStart", e12[e12.ChangeDetectionEnd = 13] = "ChangeDetectionEnd", e12[e12.ChangeDetectionSyncStart = 14] = "ChangeDetectionSyncStart", e12[e12.ChangeDetectionSyncEnd = 15] = "ChangeDetectionSyncEnd", e12[e12.AfterRenderHooksStart = 16] = "AfterRenderHooksStart", e12[e12.AfterRenderHooksEnd = 17] = "AfterRenderHooksEnd", e12[e12.ComponentStart = 18] = "ComponentStart", e12[e12.ComponentEnd = 19] = "ComponentEnd", e12[e12.DeferBlockStateStart = 20] = "DeferBlockStateStart", e12[e12.DeferBlockStateEnd = 21] = "DeferBlockStateEnd", e12[e12.DynamicComponentStart = 22] = "DynamicComponentStart", e12[e12.DynamicComponentEnd = 23] = "DynamicComponentEnd", e12[e12.HostBindingsUpdateStart = 24] = "HostBindingsUpdateStart", e12[e12.HostBindingsUpdateEnd = 25] = "HostBindingsUpdateEnd", e12;
}(C || {});
function wf(e12, t, n) {
  let { ngOnChanges: r, ngOnInit: o, ngDoCheck: i } = t.type.prototype;
  if (r) {
    let s = If(t);
    (n.preOrderHooks ??= []).push(e12, s), (n.preOrderCheckHooks ??= []).push(e12, s);
  }
  o && (n.preOrderHooks ??= []).push(0 - e12, o), i && ((n.preOrderHooks ??= []).push(e12, i), (n.preOrderCheckHooks ??= []).push(e12, i));
}
function Tf(e12, t) {
  for (let n = t.directiveStart, r = t.directiveEnd; n < r; n++) {
    let i = e12.data[n].type.prototype, { ngAfterContentInit: s, ngAfterContentChecked: a, ngAfterViewInit: c, ngAfterViewChecked: l, ngOnDestroy: u } = i;
    s && (e12.contentHooks ??= []).push(-n, s), a && ((e12.contentHooks ??= []).push(n, a), (e12.contentCheckHooks ??= []).push(n, a)), c && (e12.viewHooks ??= []).push(-n, c), l && ((e12.viewHooks ??= []).push(n, l), (e12.viewCheckHooks ??= []).push(n, l)), u != null && (e12.destroyHooks ??= []).push(n, u);
  }
}
function Tr(e12, t, n) {
  Rl(e12, t, 3, n);
}
function Mr(e12, t, n, r) {
  (e12[y] & 3) === n && Rl(e12, t, n, r);
}
function Ui(e12, t) {
  let n = e12[y];
  (n & 3) === t && (n &= 16383, n += 1, e12[y] = n);
}
function Rl(e12, t, n, r) {
  let o = r !== void 0 ? e12[rt] & 65535 : 0, i = r ?? -1, s = t.length - 1, a = 0;
  for (let c = o; c < s; c++)
    if (typeof t[c + 1] == "number") {
      if (a = t[c], r != null && a >= r)
        break;
    } else
      t[c] < 0 && (e12[rt] += 65536), (a < i || i == -1) && (Mf(e12, n, t, c), e12[rt] = (e12[rt] & 4294901760) + c + 2), c++;
}
function Jc(e12, t) {
  T(C.LifecycleHookStart, e12, t);
  let n = g(null);
  try {
    t.call(e12);
  } finally {
    g(n), T(C.LifecycleHookEnd, e12, t);
  }
}
function Mf(e12, t, n, r) {
  let o = n[r] < 0, i = n[r + 1], s = o ? -n[r] : n[r], a = e12[s];
  o ? e12[y] >> 14 < e12[rt] >> 16 && (e12[y] & 3) === t && (e12[y] += 16384, Jc(a, i)) : Jc(a, i);
}
var kt = -1;
var ln = class {
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
function _f(e12, t, n) {
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
      Sf(i) ? e12.setProperty(t, i, s) : e12.setAttribute(t, i, s), r++;
    }
  }
  return r;
}
function Sf(e12) {
  return e12.charCodeAt(0) === 64;
}
function $r(e12, t) {
  if (!(t === null || t.length === 0))
    if (e12 === null || e12.length === 0)
      e12 = t.slice();
    else {
      let n = -1;
      for (let r = 0; r < t.length; r++) {
        let o = t[r];
        typeof o == "number" ? n = o : n === 0 || (n === -1 || n === 2 ? Xc(e12, n, o, null, t[++r]) : Xc(e12, n, o, null, null));
      }
    }
  return e12;
}
function Xc(e12, t, n, r, o) {
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
function Al(e12) {
  return e12 !== kt;
}
function xr(e12) {
  return e12 & 32767;
}
function Nf(e12) {
  return e12 >> 16;
}
function Rr(e12, t) {
  let n = Nf(e12), r = t;
  for (; n > 0; )
    r = r[nt], n--;
  return r;
}
var Yi = true;
function el(e12) {
  let t = Yi;
  return Yi = e12, t;
}
var xf = 256;
var Ol = xf - 1;
var kl = 5;
var Rf = 0;
var me = {};
function Af(e12, t, n) {
  let r;
  typeof n == "string" ? r = n.charCodeAt(0) || 0 : n.hasOwnProperty(Je) && (r = n[Je]), r == null && (r = n[Je] = Rf++);
  let o = r & Ol, i = 1 << o;
  t.data[e12 + (o >> kl)] |= i;
}
function Pl(e12, t) {
  let n = Ll(e12, t);
  if (n !== -1)
    return n;
  let r = t[m];
  r.firstCreatePass && (e12.injectorIndex = t.length, zi(r.data, e12), zi(t, null), zi(r.blueprint, null));
  let o = ks(e12, t), i = e12.injectorIndex;
  if (Al(o)) {
    let s = xr(o), a = Rr(o, t), c = a[m].data;
    for (let l = 0; l < 8; l++)
      t[i + l] = a[s + l] | c[s + l];
  }
  return t[i + 8] = o, i;
}
function zi(e12, t) {
  e12.push(0, 0, 0, 0, 0, 0, 0, 0, t);
}
function Ll(e12, t) {
  return e12.injectorIndex === -1 || e12.parent && e12.parent.injectorIndex === e12.injectorIndex || t[e12.injectorIndex + 8] === null ? -1 : e12.injectorIndex;
}
function ks(e12, t) {
  if (e12.parent && e12.parent.injectorIndex !== -1)
    return e12.parent.injectorIndex;
  let n = 0, r = null, o = t;
  for (; o !== null; ) {
    if (r = Bl(o), r === null)
      return kt;
    if (n++, o = o[nt], r.injectorIndex !== -1)
      return r.injectorIndex | n << 16;
  }
  return kt;
}
function Of(e12, t, n) {
  Af(e12, t, n);
}
function Fl(e12, t, n) {
  if (n & 8 || e12 !== void 0)
    return e12;
  or(t, "NodeInjector");
}
function jl(e12, t, n, r) {
  if (n & 8 && r === void 0 && (r = null), (n & 3) === 0) {
    let o = e12[be], i = G(void 0);
    try {
      return o ? o.get(t, r, n & 8) : hi(t, r, n & 8);
    } finally {
      G(i);
    }
  }
  return Fl(r, t, n);
}
function Hl(e12, t, n, r = 0, o) {
  if (e12 !== null) {
    if (t[y] & 2048 && !(r & 2)) {
      let s = Ff(e12, t, n, r, me);
      if (s !== me)
        return s;
    }
    let i = Vl(e12, t, n, r, me);
    if (i !== me)
      return i;
  }
  return jl(t, n, r, o);
}
function Vl(e12, t, n, r, o) {
  let i = Pf(n);
  if (typeof i == "function") {
    if (!Pi(t, e12, r))
      return r & 1 ? Fl(o, n, r) : jl(t, n, r, o);
    try {
      let s;
      if (s = i(r), s == null && !(r & 8))
        or(n);
      else
        return s;
    } finally {
      Li();
    }
  } else if (typeof i == "number") {
    let s = null, a = Ll(e12, t), c = kt, l = r & 1 ? t[ee][X] : null;
    for ((a === -1 || r & 4) && (c = a === -1 ? ks(e12, t) : t[a + 8], c === kt || !nl(r, false) ? a = -1 : (s = t[m], a = xr(c), t = Rr(c, t))); a !== -1; ) {
      let u = t[m];
      if (tl(i, a, u.data)) {
        let d = kf(a, t, n, s, r, l);
        if (d !== me)
          return d;
      }
      c = t[a + 8], c !== kt && nl(r, t[m].data[a + 8] === l) && tl(i, a, t) ? (s = u, a = xr(c), t = Rr(c, t)) : a = -1;
    }
  }
  return o;
}
function kf(e12, t, n, r, o, i) {
  let s = t[m], a = s.data[e12 + 8], c = r == null ? Mt(a) && Yi : r != s && (a.type & 3) !== 0, l = o & 1 && i === a, u = _r(a, s, n, c, l);
  return u !== null ? Ar(t, s, u, a, o) : me;
}
function _r(e12, t, n, r, o) {
  let i = e12.providerIndexes, s = t.data, a = i & 1048575, c = e12.directiveStart, l = e12.directiveEnd, u = i >> 20, d = r ? a : a + u, f = o ? a + u : l;
  for (let p = d; p < f; p++) {
    let h = s[p];
    if (p < c && n === h || p >= c && h.type === n)
      return p;
  }
  if (o) {
    let p = s[c];
    if (p && _t(p) && p.type === n)
      return c;
  }
  return null;
}
function Ar(e12, t, n, r, o) {
  let i = e12[n], s = t.data;
  if (i instanceof ln) {
    let a = i;
    if (a.resolving)
      throw pi("");
    let c = el(a.canSeeViewProviders);
    a.resolving = true;
    let l = s[n].type || s[n], u, d = a.injectImpl ? G(a.injectImpl) : null, f = Pi(e12, r, 0);
    try {
      i = e12[n] = a.factory(void 0, o, s, e12, r), t.firstCreatePass && n >= r.directiveStart && wf(n, s[n], t);
    } finally {
      d !== null && G(d), el(c), a.resolving = false, Li();
    }
  }
  return i;
}
function Pf(e12) {
  if (typeof e12 == "string")
    return e12.charCodeAt(0) || 0;
  let t = e12.hasOwnProperty(Je) ? e12[Je] : void 0;
  return typeof t == "number" ? t >= 0 ? t & Ol : Lf : t;
}
function tl(e12, t, n) {
  let r = 1 << e12;
  return !!(n[t + (e12 >> kl)] & r);
}
function nl(e12, t) {
  return !(e12 & 2) && !(e12 & 1 && t);
}
var at = class {
  _tNode;
  _lView;
  constructor(t, n) {
    this._tNode = t, this._lView = n;
  }
  get(t, n, r) {
    return Hl(this._tNode, this._lView, t, Qe(r), n);
  }
};
function Lf() {
  return new at(ge(), M());
}
function Ff(e12, t, n, r, o) {
  let i = e12, s = t;
  for (; i !== null && s !== null && s[y] & 2048 && !St(s); ) {
    let a = Vl(i, s, n, r | 2, me);
    if (a !== me)
      return a;
    let c = i.parent;
    if (!c) {
      let l = s[Di];
      if (l) {
        let u = l.get(n, me, r & -5);
        if (u !== me)
          return u;
      }
      c = Bl(s), s = s[nt];
    }
    i = c;
  }
  return o;
}
function Bl(e12) {
  let t = e12[m], n = t.type;
  return n === 2 ? t.declTNode : n === 1 ? e12[X] : null;
}
function jf() {
  return jt(ge(), M());
}
function jt(e12, t) {
  return new yn(pe(e12, t));
}
var yn = /* @__PURE__ */ (() => {
  class e12 {
    nativeElement;
    constructor(n) {
      this.nativeElement = n;
    }
    static __NG_ELEMENT_ID__ = jf;
  }
  return e12;
})();
function Hf(e12) {
  return e12 instanceof yn ? e12.nativeElement : e12;
}
function Vf() {
  return this._results[Symbol.iterator]();
}
var Or = class {
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
    return this._changes ??= new ve();
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
    let r = oc(t);
    (this._changesDetected = !rc(this._results, r, n)) && (this._results = r, this.length = r.length, this.last = r[this.length - 1], this.first = r[0]);
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
  [Symbol.iterator] = Vf;
};
function $l(e12) {
  return (e12.flags & 128) === 128;
}
var Ps = function(e12) {
  return e12[e12.OnPush = 0] = "OnPush", e12[e12.Eager = 1] = "Eager", e12[e12.Default = 1] = "Default", e12;
}(Ps || {});
var Ul = /* @__PURE__ */ new Map();
var Bf = 0;
function $f() {
  return Bf++;
}
function Uf(e12) {
  Ul.set(e12[Ce], e12);
}
function Ki(e12) {
  Ul.delete(e12[Ce]);
}
var rl = "__ngContext__";
function Pt(e12, t) {
  Be(t) ? (e12[rl] = t[Ce], Uf(t)) : e12[rl] = t;
}
function zl(e12) {
  return Gl(e12[Tt]);
}
function Wl(e12) {
  return Gl(e12[J]);
}
function Gl(e12) {
  for (; e12 !== null && !oe(e12); )
    e12 = e12[J];
  return e12;
}
var Ji;
function Ls(e12) {
  Ji = e12;
}
function ql() {
  if (Ji !== void 0)
    return Ji;
  if (typeof document < "u")
    return document;
  throw new v(210, false);
}
var Ur = new D("", { factory: () => zf });
var zf = "ng";
var zr = new D("");
var vn = new D("", { providedIn: "platform", factory: () => "unknown" });
var Wr = new D("", { factory: () => E(z).body?.querySelector("[ngCspNonce]")?.getAttribute("ngCspNonce") || null });
var Zl = "r";
var Ql = "di";
var Yl = false;
var Kl = new D("", { factory: () => Yl });
var ol = /* @__PURE__ */ new WeakMap();
function Wf(e12, t) {
  if (e12 == null || typeof e12 != "object")
    return;
  let n = ol.get(e12);
  n || (n = /* @__PURE__ */ new WeakSet(), ol.set(e12, n)), n.add(t);
}
var Gf = (e12, t, n, r) => {
};
function qf(e12, t, n, r) {
  Gf(e12, t, n, r);
}
function Fs(e12) {
  return (e12.flags & 32) === 32;
}
var Zf = () => null;
function Jl(e12, t, n = false) {
  return Zf(e12, t, n);
}
function Xl(e12, t) {
  let n = e12.contentQueries;
  if (n !== null) {
    let r = g(null);
    try {
      for (let o = 0; o < n.length; o += 2) {
        let i = n[o], s = n[o + 1];
        if (s !== -1) {
          let a = e12.data[s];
          hr(i), a.contentQueries(2, t[s], s);
        }
      }
    } finally {
      g(r);
    }
  }
}
function Xi(e12, t, n) {
  hr(0);
  let r = g(null);
  try {
    t(e12, n);
  } finally {
    g(r);
  }
}
function Qf(e12, t, n) {
  if (Ci(t)) {
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
var se = function(e12) {
  return e12[e12.Emulated = 0] = "Emulated", e12[e12.None = 2] = "None", e12[e12.ShadowDom = 3] = "ShadowDom", e12[e12.ExperimentalIsolatedShadowDom = 4] = "ExperimentalIsolatedShadowDom", e12;
}(se || {});
var Dr;
function Yf() {
  if (Dr === void 0 && (Dr = null, Fe.trustedTypes))
    try {
      Dr = Fe.trustedTypes.createPolicy("angular", { createHTML: (e12) => e12, createScript: (e12) => e12, createScriptURL: (e12) => e12 });
    } catch {
    }
  return Dr;
}
function Gr(e12) {
  return Yf()?.createHTML(e12) || e12;
}
var br;
function Kf() {
  if (br === void 0 && (br = null, Fe.trustedTypes))
    try {
      br = Fe.trustedTypes.createPolicy("angular#unsafe-bypass", { createHTML: (e12) => e12, createScript: (e12) => e12, createScriptURL: (e12) => e12 });
    } catch {
    }
  return br;
}
function il(e12) {
  return Kf()?.createHTML(e12) || e12;
}
var _e = class {
  changingThisBreaksApplicationSecurity;
  constructor(t) {
    this.changingThisBreaksApplicationSecurity = t;
  }
  toString() {
    return `SafeValue must use [property]=binding: ${this.changingThisBreaksApplicationSecurity} (see ${Jn})`;
  }
};
var es = class extends _e {
  getTypeName() {
    return "HTML";
  }
};
var ts = class extends _e {
  getTypeName() {
    return "Style";
  }
};
var ns = class extends _e {
  getTypeName() {
    return "Script";
  }
};
var rs = class extends _e {
  getTypeName() {
    return "URL";
  }
};
var os = class extends _e {
  getTypeName() {
    return "ResourceURL";
  }
};
function Ne(e12) {
  return e12 instanceof _e ? e12.changingThisBreaksApplicationSecurity : e12;
}
function ze(e12, t) {
  let n = eu(e12);
  if (n != null && n !== t) {
    if (n === "ResourceURL" && t === "URL")
      return true;
    throw new Error(`Required a safe ${t}, got a ${n} (see ${Jn})`);
  }
  return n === t;
}
function eu(e12) {
  return e12 instanceof _e && e12.getTypeName() || null;
}
function js(e12) {
  return new es(e12);
}
function Hs(e12) {
  return new ts(e12);
}
function Vs(e12) {
  return new ns(e12);
}
function Bs(e12) {
  return new rs(e12);
}
function $s(e12) {
  return new os(e12);
}
function Jf(e12) {
  let t = new ss(e12);
  return Xf() ? new is(t) : t;
}
var is = class {
  inertDocumentHelper;
  constructor(t) {
    this.inertDocumentHelper = t;
  }
  getInertBodyElement(t) {
    t = "<body><remove></remove>" + t;
    try {
      let n = new window.DOMParser().parseFromString(Gr(t), "text/html").body;
      return n === null ? this.inertDocumentHelper.getInertBodyElement(t) : (n.firstChild?.remove(), n);
    } catch {
      return null;
    }
  }
};
var ss = class {
  defaultDoc;
  inertDocument;
  constructor(t) {
    this.defaultDoc = t, this.inertDocument = this.defaultDoc.implementation.createHTMLDocument("sanitization-inert");
  }
  getInertBodyElement(t) {
    let n = this.inertDocument.createElement("template");
    return n.innerHTML = Gr(t), n;
  }
};
function Xf() {
  try {
    return !!new window.DOMParser().parseFromString(Gr(""), "text/html");
  } catch {
    return false;
  }
}
var ep = /^(?!javascript:)(?:[a-z0-9+.-]+:|[^&:\/?#]*(?:[\/?#]|$))/i;
function qr(e12) {
  return e12 = String(e12), e12.match(ep) ? e12 : "unsafe:" + e12;
}
function xe(e12) {
  let t = {};
  for (let n of e12.split(","))
    t[n] = true;
  return t;
}
function En(...e12) {
  let t = {};
  for (let n of e12)
    for (let r in n)
      n.hasOwnProperty(r) && (t[r] = true);
  return t;
}
var tu = xe("area,br,col,hr,img,wbr");
var nu = xe("colgroup,dd,dt,li,p,tbody,td,tfoot,th,thead,tr");
var ru = xe("rp,rt");
var tp = En(ru, nu);
var np = En(nu, xe("address,article,aside,blockquote,caption,center,del,details,dialog,dir,div,dl,figure,figcaption,footer,h1,h2,h3,h4,h5,h6,header,hgroup,hr,ins,main,map,menu,nav,ol,pre,section,summary,table,ul"));
var rp = En(ru, xe("a,abbr,acronym,audio,b,bdi,bdo,big,br,cite,code,del,dfn,em,font,i,img,ins,kbd,label,map,mark,picture,q,ruby,rp,rt,s,samp,small,source,span,strike,strong,sub,sup,time,track,tt,u,var,video"));
var sl = En(tu, np, rp, tp);
var ou = xe("background,cite,href,itemtype,longdesc,poster,src,xlink:href");
var op = xe("abbr,accesskey,align,alt,autoplay,axis,bgcolor,border,cellpadding,cellspacing,class,clear,color,cols,colspan,compact,controls,coords,datetime,default,dir,download,face,headers,height,hidden,hreflang,hspace,ismap,itemscope,itemprop,kind,label,lang,language,loop,media,muted,nohref,nowrap,open,preload,rel,rev,role,rows,rowspan,rules,scope,scrolling,shape,size,sizes,span,srclang,srcset,start,summary,tabindex,target,title,translate,type,usemap,valign,value,vspace,width");
var ip = xe("aria-activedescendant,aria-atomic,aria-autocomplete,aria-busy,aria-checked,aria-colcount,aria-colindex,aria-colspan,aria-controls,aria-current,aria-describedby,aria-details,aria-disabled,aria-dropeffect,aria-errormessage,aria-expanded,aria-flowto,aria-grabbed,aria-haspopup,aria-hidden,aria-invalid,aria-keyshortcuts,aria-label,aria-labelledby,aria-level,aria-live,aria-modal,aria-multiline,aria-multiselectable,aria-orientation,aria-owns,aria-placeholder,aria-posinset,aria-pressed,aria-readonly,aria-relevant,aria-required,aria-roledescription,aria-rowcount,aria-rowindex,aria-rowspan,aria-selected,aria-setsize,aria-sort,aria-valuemax,aria-valuemin,aria-valuenow,aria-valuetext");
var sp = En(ou, op, ip);
var ap = xe("script,style,template");
var as = class {
  sanitizedSomething = false;
  buf = [];
  sanitizeChildren(t) {
    let n = t.firstChild, r = true, o = [];
    for (; n; ) {
      if (n.nodeType === Node.ELEMENT_NODE ? r = this.startElement(n) : n.nodeType === Node.TEXT_NODE ? this.chars(n.nodeValue) : this.sanitizedSomething = true, r && n.firstChild) {
        o.push(n), n = up(n);
        continue;
      }
      for (; n; ) {
        n.nodeType === Node.ELEMENT_NODE && this.endElement(n);
        let i = lp(n);
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
    let n = al(t).toLowerCase();
    if (!sl.hasOwnProperty(n))
      return this.sanitizedSomething = true, !ap.hasOwnProperty(n);
    this.buf.push("<"), this.buf.push(n);
    let r = t.attributes;
    for (let o = 0; o < r.length; o++) {
      let i = r.item(o), s = i.name, a = s.toLowerCase();
      if (!sp.hasOwnProperty(a)) {
        this.sanitizedSomething = true;
        continue;
      }
      let c = i.value;
      ou[a] && (c = qr(c)), this.buf.push(" ", s, '="', cl(c), '"');
    }
    return this.buf.push(">"), true;
  }
  endElement(t) {
    let n = al(t).toLowerCase();
    sl.hasOwnProperty(n) && !tu.hasOwnProperty(n) && (this.buf.push("</"), this.buf.push(n), this.buf.push(">"));
  }
  chars(t) {
    this.buf.push(cl(t));
  }
};
function cp(e12, t) {
  return (e12.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_CONTAINED_BY) !== Node.DOCUMENT_POSITION_CONTAINED_BY;
}
function lp(e12) {
  let t = e12.nextSibling;
  if (t && e12 !== t.previousSibling)
    throw iu(t);
  return t;
}
function up(e12) {
  let t = e12.firstChild;
  if (t && cp(e12, t))
    throw iu(t);
  return t;
}
function al(e12) {
  let t = e12.nodeName;
  return typeof t == "string" ? t : "FORM";
}
function iu(e12) {
  return new Error(`Failed to sanitize html because the element is clobbered: ${e12.outerHTML}`);
}
var dp = /[\uD800-\uDBFF][\uDC00-\uDFFF]/g;
var fp = /([^\#-~ |!])/g;
function cl(e12) {
  return e12.replace(/&/g, "&amp;").replace(dp, function(t) {
    let n = t.charCodeAt(0), r = t.charCodeAt(1);
    return "&#" + ((n - 55296) * 1024 + (r - 56320) + 65536) + ";";
  }).replace(fp, function(t) {
    return "&#" + t.charCodeAt(0) + ";";
  }).replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
var Cr;
function Zr(e12, t) {
  let n = null;
  try {
    Cr = Cr || Jf(e12);
    let r = t ? String(t) : "";
    n = Cr.getInertBodyElement(r);
    let o = 5, i = r;
    do {
      if (o === 0)
        throw new Error("Failed to sanitize html because the input is unstable");
      o--, r = i, i = n.innerHTML, n = Cr.getInertBodyElement(r);
    } while (r !== i);
    let a = new as().sanitizeChildren(ll(n) || n);
    return Gr(a);
  } finally {
    if (n) {
      let r = ll(n) || n;
      for (; r.firstChild; )
        r.firstChild.remove();
    }
  }
}
function ll(e12) {
  return "content" in e12 && pp(e12) ? e12.content : null;
}
function pp(e12) {
  return e12.nodeType === Node.ELEMENT_NODE && e12.nodeName === "TEMPLATE";
}
function hp(e12, t) {
  return e12.createText(t);
}
function gp(e12, t, n) {
  e12.setValue(t, n);
}
function su(e12, t, n) {
  return e12.createElement(t, n);
}
function kr(e12, t, n, r, o) {
  e12.insertBefore(t, n, r, o);
}
function au(e12, t, n) {
  e12.appendChild(t, n);
}
function ul(e12, t, n, r, o) {
  r !== null ? kr(e12, t, n, r, o) : au(e12, t, n);
}
function cu(e12, t, n, r) {
  e12.removeChild(null, t, n, r);
}
function mp(e12, t, n) {
  e12.setAttribute(t, "style", n);
}
function yp(e12, t, n) {
  n === "" ? e12.removeAttribute(t, "class") : e12.setAttribute(t, "class", n);
}
function lu(e12, t, n) {
  let { mergedAttrs: r, classes: o, styles: i } = n;
  r !== null && _f(e12, t, r), o !== null && yp(e12, t, o), i !== null && mp(e12, t, i);
}
var ye = function(e12) {
  return e12[e12.NONE = 0] = "NONE", e12[e12.HTML = 1] = "HTML", e12[e12.STYLE = 2] = "STYLE", e12[e12.SCRIPT = 3] = "SCRIPT", e12[e12.URL = 4] = "URL", e12[e12.RESOURCE_URL = 5] = "RESOURCE_URL", e12;
}(ye || {});
function Us(e12) {
  let t = vp();
  return t ? il(t.sanitize(ye.HTML, e12) || "") : ze(e12, "HTML") ? il(Ne(e12)) : Zr(ql(), fi(e12));
}
function vp() {
  let e12 = M();
  return e12 && e12[de].sanitizer;
}
var Ep = "ng-template";
function Ip(e12) {
  return e12.type === 4 && e12.value !== Ep;
}
function cs(e12) {
  return (e12 & 1) === 0;
}
function dl(e12, t) {
  return e12 ? ":not(" + t.trim() + ")" : t;
}
function Dp(e12) {
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
      o !== "" && !cs(s) && (t += dl(i, o), o = ""), r = s, i = i || !cs(r);
    n++;
  }
  return o !== "" && (t += dl(i, o)), t;
}
function bp(e12) {
  return e12.map(Dp).join(",");
}
function Cp(e12) {
  let t = [], n = [], r = 1, o = 2;
  for (; r < e12.length; ) {
    let i = e12[r];
    if (typeof i == "string")
      o === 2 ? i !== "" && t.push(i, e12[++r]) : o === 8 && n.push(i);
    else {
      if (!cs(o))
        break;
      o = i;
    }
    r++;
  }
  return n.length && t.push(1, ...n), t;
}
var Re = {};
function zs(e12, t, n, r, o, i, s, a, c, l, u) {
  let d = B + r, f = d + o, p = wp(d, f), h = typeof l == "function" ? l() : l;
  return p[m] = { type: e12, blueprint: p, template: n, queries: null, viewQuery: a, declTNode: t, data: p.slice().fill(null, d), bindingStartIndex: d, expandoStartIndex: f, hostBindingOpCodes: null, firstCreatePass: true, firstUpdatePass: true, staticViewQueries: false, staticContentQueries: false, preOrderHooks: null, preOrderCheckHooks: null, contentHooks: null, contentCheckHooks: null, viewHooks: null, viewCheckHooks: null, destroyHooks: null, cleanup: null, contentQueries: null, components: null, directiveRegistry: typeof i == "function" ? i() : i, pipeRegistry: typeof s == "function" ? s() : s, firstChild: null, schemas: c, consts: h, incompleteFirstPass: false, ssrId: u };
}
function wp(e12, t) {
  let n = [];
  for (let r = 0; r < t; r++)
    n.push(r < e12 ? null : Re);
  return n;
}
function Tp(e12) {
  let t = e12.tView;
  return t === null || t.incompleteFirstPass ? e12.tView = zs(1, null, e12.template, e12.decls, e12.vars, e12.directiveDefs, e12.pipeDefs, e12.viewQuery, e12.schemas, e12.consts, e12.id) : t;
}
function Ws(e12, t, n, r, o, i, s, a, c, l, u) {
  let d = t.blueprint.slice();
  return d[re] = o, d[y] = r | 4 | 128 | 8 | 64 | 1024, (l !== null || e12 && e12[y] & 2048) && (d[y] |= 2048), Mi(d), d[A] = d[nt] = e12, d[x] = n, d[de] = s || e12 && e12[de], d[O] = a || e12 && e12[O], d[be] = c || e12 && e12[be] || null, d[X] = i, d[Ce] = $f(), d[Ct] = u, d[Di] = l, d[ee] = t.type == 2 ? e12[ee] : d, d;
}
function Mp(e12, t, n) {
  let r = pe(t, e12), o = Tp(n), i = e12[de].rendererFactory, s = Gs(e12, Ws(e12, o, null, uu(n), r, t, null, i.createRenderer(r, n), null, null, null));
  return e12[t.index] = s;
}
function uu(e12) {
  let t = 16;
  return e12.signals ? t = 4096 : e12.onPush && (t = 64), t;
}
function du(e12, t, n, r) {
  if (n === 0)
    return -1;
  let o = t.length;
  for (let i = 0; i < n; i++)
    t.push(r), e12.blueprint.push(r), e12.data.push(null);
  return o;
}
function Gs(e12, t) {
  return e12[Tt] ? e12[Ii][J] = t : e12[Tt] = t, e12[Ii] = t, t;
}
function F(e12 = 1) {
  fu(ie(), M(), $e() + e12, false);
}
function fu(e12, t, n, r) {
  if (!r)
    if ((t[y] & 3) === 3) {
      let i = e12.preOrderCheckHooks;
      i !== null && Tr(t, i, n);
    } else {
      let i = e12.preOrderHooks;
      i !== null && Mr(t, i, 0, n);
    }
  Ue(n);
}
var Qr = function(e12) {
  return e12[e12.None = 0] = "None", e12[e12.SignalBased = 1] = "SignalBased", e12[e12.HasDecoratorInputTransform = 2] = "HasDecoratorInputTransform", e12;
}(Qr || {});
function ls(e12, t, n, r) {
  let o = g(null);
  try {
    let [i, s, a] = e12.inputs[n], c = null;
    (s & Qr.SignalBased) !== 0 && (c = t[i][Q]), c !== null && c.transformFn !== void 0 ? r = c.transformFn(r) : a !== null && (r = a.call(t, r)), e12.setInput !== null ? e12.setInput(t, c, r, n, i) : Sl(t, c, i, r);
  } finally {
    g(o);
  }
}
var Se = function(e12) {
  return e12[e12.Important = 1] = "Important", e12[e12.DashCase = 2] = "DashCase", e12;
}(Se || {});
var _p;
function qs(e12, t) {
  return _p(e12, t);
}
var ZE = typeof document < "u" && typeof document?.documentElement?.getAnimations == "function";
var us = /* @__PURE__ */ new WeakMap();
var sn = /* @__PURE__ */ new WeakSet();
function Sp(e12, t) {
  let n = us.get(e12);
  if (!n || n.length === 0)
    return;
  let r = t.parentNode, o = t.previousSibling;
  for (let i = n.length - 1; i >= 0; i--) {
    let s = n[i], a = s.parentNode;
    s === t ? (n.splice(i, 1), sn.add(s), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } }))) : (o && s === o || a && r && a !== r) && (n.splice(i, 1), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } })), s.parentNode?.removeChild(s));
  }
}
function Np(e12, t) {
  let n = us.get(e12);
  n ? n.includes(t) || n.push(t) : us.set(e12, [t]);
}
var ct = /* @__PURE__ */ new Set();
var Zs = function(e12) {
  return e12[e12.CHANGE_DETECTION = 0] = "CHANGE_DETECTION", e12[e12.AFTER_NEXT_RENDER = 1] = "AFTER_NEXT_RENDER", e12;
}(Zs || {});
var Ht = new D("");
var fl = /* @__PURE__ */ new Set();
function Vt(e12) {
  fl.has(e12) || (fl.add(e12), performance?.mark?.("mark_feature_usage", { detail: { feature: e12 } }));
}
var pu = (() => {
  class e12 {
    impl = null;
    execute() {
      this.impl?.execute();
    }
    static \u0275prov = _({ token: e12, providedIn: "root", factory: () => new e12() });
  }
  return e12;
})();
var hu = new D("", { factory: () => ({ queue: /* @__PURE__ */ new Set(), isScheduled: false, scheduler: null, injector: E(Y) }) });
function gu(e12, t, n) {
  let r = e12.get(hu);
  if (Array.isArray(t))
    for (let o of t)
      r.queue.add(o), n?.detachedLeaveAnimationFns?.push(o);
  else
    r.queue.add(t), n?.detachedLeaveAnimationFns?.push(t);
  r.scheduler && r.scheduler(e12);
}
function xp(e12, t) {
  let n = e12.get(hu);
  if (t.detachedLeaveAnimationFns) {
    for (let r of t.detachedLeaveAnimationFns)
      n.queue.delete(r);
    t.detachedLeaveAnimationFns = void 0;
  }
}
function Rp(e12, t) {
  for (let [n, r] of t)
    gu(e12, r.animateFns);
}
function pl(e12, t, n, r) {
  let o = e12?.[He]?.enter;
  t !== null && o && o.has(n.index) && Rp(r, o);
}
function Ot(e12, t, n, r, o, i, s, a) {
  if (o != null) {
    let c, l = false;
    oe(o) ? c = o : Be(o) && (l = true, o = o[re]);
    let u = te(o);
    e12 === 0 && r !== null ? (pl(a, r, i, n), s == null ? au(t, r, u) : kr(t, r, u, s || null, true)) : e12 === 1 && r !== null ? (pl(a, r, i, n), kr(t, r, u, s || null, true), Sp(i, u)) : e12 === 2 ? (a?.[He]?.leave?.has(i.index) && Np(i, u), sn.delete(u), hl(a, i, n, (d) => {
      if (sn.has(u)) {
        sn.delete(u);
        return;
      }
      cu(t, u, l, d);
    })) : e12 === 3 && (sn.delete(u), hl(a, i, n, () => {
      t.destroyNode(u);
    })), c != null && zp(t, e12, n, c, i, r, s);
  }
}
function Ap(e12, t) {
  mu(e12, t), t[re] = null, t[X] = null;
}
function Op(e12, t, n, r, o, i) {
  r[re] = o, r[X] = t, Kr(e12, r, n, 1, o, i);
}
function mu(e12, t) {
  t[de].changeDetectionScheduler?.notify(9), Kr(e12, t, t[O], 2, null, null);
}
function kp(e12) {
  let t = e12[Tt];
  if (!t)
    return Wi(e12[m], e12);
  for (; t; ) {
    let n = null;
    if (Be(t))
      n = t[Tt];
    else {
      let r = t[S];
      r && (n = r);
    }
    if (!n) {
      for (; t && !t[J] && t !== e12; )
        Be(t) && Wi(t[m], t), t = t[A];
      t === null && (t = e12), Be(t) && Wi(t[m], t), n = t && t[J];
    }
    t = n;
  }
}
function Qs(e12, t) {
  let n = e12[ot], r = n.indexOf(t);
  n.splice(r, 1);
}
function Yr(e12, t) {
  if (it(t))
    return;
  let n = t[O];
  n.destroyNode && Kr(e12, t, n, 3, null, null), kp(t);
}
function Wi(e12, t) {
  if (it(t))
    return;
  let n = g(null);
  try {
    t[y] &= -129, t[y] |= 256, t[Z] && pt(t[Z]), Fp(e12, t), Lp(e12, t), t[m].type === 1 && t[O].destroy();
    let r = t[je];
    if (r !== null && oe(t[A])) {
      r !== t[A] && Qs(r, t);
      let o = t[fe];
      o !== null && o.detachView(e12);
    }
    Ki(t);
  } finally {
    g(n);
  }
}
function hl(e12, t, n, r) {
  let o = e12?.[He];
  if (o == null || o.leave == null || !o.leave.has(t.index))
    return r(false);
  e12 && ct.add(e12[Ce]), gu(n, () => {
    if (o.leave && o.leave.has(t.index)) {
      let s = o.leave.get(t.index), a = [];
      if (s) {
        for (let c = 0; c < s.animateFns.length; c++) {
          let l = s.animateFns[c], { promise: u } = l();
          a.push(u);
        }
        o.detachedLeaveAnimationFns = void 0;
      }
      o.running = Promise.allSettled(a), Pp(e12, r);
    } else
      e12 && ct.delete(e12[Ce]), r(false);
  }, o);
}
function Pp(e12, t) {
  let n = e12[He]?.running;
  if (n) {
    n.then(() => {
      e12[He].running = void 0, ct.delete(e12[Ce]), t(true);
    });
    return;
  }
  t(false);
}
function Lp(e12, t) {
  let n = e12.cleanup, r = t[wt];
  if (n !== null)
    for (let s = 0; s < n.length - 1; s += 2)
      if (typeof n[s] == "string") {
        let a = n[s + 3];
        a >= 0 ? r[a]() : r[-a].unsubscribe(), s += 2;
      } else {
        let a = r[n[s + 1]];
        n[s].call(a);
      }
  r !== null && (t[wt] = null);
  let o = t[Ie];
  if (o !== null) {
    t[Ie] = null;
    for (let s = 0; s < o.length; s++) {
      let a = o[s];
      a();
    }
  }
  let i = t[Pe];
  if (i !== null) {
    t[Pe] = null;
    for (let s of i)
      s.destroy();
  }
}
function Fp(e12, t) {
  let n;
  if (e12 != null && (n = e12.destroyHooks) != null)
    for (let r = 0; r < n.length; r += 2) {
      let o = t[n[r]];
      if (!(o instanceof ln)) {
        let i = n[r + 1];
        if (Array.isArray(i))
          for (let s = 0; s < i.length; s += 2) {
            let a = o[i[s]], c = i[s + 1];
            T(C.LifecycleHookStart, a, c);
            try {
              c.call(a);
            } finally {
              T(C.LifecycleHookEnd, a, c);
            }
          }
        else {
          T(C.LifecycleHookStart, o, i);
          try {
            i.call(o);
          } finally {
            T(C.LifecycleHookEnd, o, i);
          }
        }
      }
    }
}
function jp(e12, t, n) {
  return Hp(e12, t.parent, n);
}
function Hp(e12, t, n) {
  let r = t;
  for (; r !== null && r.type & 168; )
    t = r, r = t.parent;
  if (r === null)
    return n[re];
  if (Mt(r)) {
    let { encapsulation: o } = e12.data[r.directiveStart + r.componentOffset];
    if (o === se.None || o === se.Emulated)
      return null;
  }
  return pe(r, n);
}
function Vp(e12, t, n) {
  return $p(e12, t, n);
}
function Bp(e12, t, n) {
  return e12.type & 40 ? pe(e12, n) : null;
}
var $p = Bp;
var gl;
function Ys(e12, t, n, r) {
  let o = jp(e12, r, t), i = t[O], s = r.parent || t[X], a = Vp(s, r, t);
  if (o != null)
    if (Array.isArray(n))
      for (let c = 0; c < n.length; c++)
        ul(i, o, n[c], a, false);
    else
      ul(i, o, n, a, false);
  gl !== void 0 && gl(i, r, t, n, o);
}
function an(e12, t) {
  if (t !== null) {
    let n = t.type;
    if (n & 3)
      return pe(t, e12);
    if (n & 4)
      return ds(-1, e12[t.index]);
    if (n & 8) {
      let r = t.child;
      if (r !== null)
        return an(e12, r);
      {
        let o = e12[t.index];
        return oe(o) ? ds(-1, o) : te(o);
      }
    } else {
      if (n & 128)
        return an(e12, t.next);
      if (n & 32)
        return qs(t, e12)() || te(e12[t.index]);
      {
        let r = yu(e12, t);
        if (r !== null) {
          if (Array.isArray(r))
            return r[0];
          let o = Le(e12[ee]);
          return an(o, r);
        } else
          return an(e12, t.next);
      }
    }
  }
  return null;
}
function yu(e12, t) {
  if (t !== null) {
    let r = e12[ee][X], o = t.projection;
    return r.projection[o];
  }
  return null;
}
function ds(e12, t) {
  let n = S + e12 + 1;
  if (n < t.length) {
    let r = t[n], o = r[m].firstChild;
    if (o !== null)
      return an(r, o);
  }
  return t[Ve];
}
function Ks(e12, t, n, r, o, i, s) {
  for (; n != null; ) {
    let a = r[be];
    if (n.type === 128) {
      n = n.next;
      continue;
    }
    let c = r[n.index], l = n.type;
    if (s && t === 0 && (c && Pt(te(c), r), n.flags |= 2), !Fs(n))
      if (l & 8)
        Ks(e12, t, n.child, r, o, i, false), Ot(t, e12, a, o, c, n, i, r);
      else if (l & 32) {
        let u = qs(n, r), d;
        for (; d = u(); )
          Ot(t, e12, a, o, d, n, i, r);
        Ot(t, e12, a, o, c, n, i, r);
      } else
        l & 16 ? Up(e12, t, r, n, o, i) : Ot(t, e12, a, o, c, n, i, r);
    n = s ? n.projectionNext : n.next;
  }
}
function Kr(e12, t, n, r, o, i) {
  Ks(n, r, e12.firstChild, t, o, i, false);
}
function Up(e12, t, n, r, o, i) {
  let s = n[ee], c = s[X].projection[r.projection];
  if (Array.isArray(c))
    for (let l = 0; l < c.length; l++) {
      let u = c[l];
      Ot(t, e12, n[be], o, u, r, i, n);
    }
  else {
    let l = c, u = s[A];
    $l(r) && (l.flags |= 128), Ks(e12, t, l, u, o, i, true);
  }
}
function zp(e12, t, n, r, o, i, s) {
  let a = r[Ve], c = te(r);
  a !== c && Ot(t, e12, n, i, a, o, s);
  for (let l = S; l < r.length; l++) {
    let u = r[l];
    Kr(u[m], u, e12, t, i, a);
  }
}
function Wp(e12, t, n, r, o) {
  if (t)
    o ? e12.addClass(n, r) : e12.removeClass(n, r);
  else {
    let i = r.indexOf("-") === -1 ? void 0 : Se.DashCase;
    o == null ? e12.removeStyle(n, r, i) : (typeof o == "string" && o.endsWith("!important") && (o = o.slice(0, -10), i |= Se.Important), e12.setStyle(n, r, o, i));
  }
}
function vu(e12, t, n, r, o) {
  let i = $e(), s = r & 2;
  try {
    Ue(-1), s && t.length > B && fu(e12, t, B, false);
    let a = s ? C.TemplateUpdateStart : C.TemplateCreateStart;
    T(a, o, n), n(r, o);
  } finally {
    Ue(i);
    let a = s ? C.TemplateUpdateEnd : C.TemplateCreateEnd;
    T(a, o, n);
  }
}
function Gp(e12, t, n) {
  Kp(e12, t, n), (n.flags & 64) === 64 && Jp(e12, t, n);
}
function Eu(e12, t, n = pe) {
  let r = t.localNames;
  if (r !== null) {
    let o = t.index + 1;
    for (let i = 0; i < r.length; i += 2) {
      let s = r[i + 1], a = s === -1 ? n(t, e12) : e12[s];
      e12[o++] = a;
    }
  }
}
function qp(e12, t, n, r) {
  let i = r.get(Kl, Yl) || n === se.ShadowDom || n === se.ExperimentalIsolatedShadowDom, s = e12.selectRootElement(t, i);
  return Zp(s), s;
}
function Zp(e12) {
  Qp(e12);
}
var Qp = () => null;
function Yp(e12, t, n, r, o, i) {
  if (e12.type & 3) {
    let s = pe(e12, t);
    r = i != null ? i(r, e12.value || "", n) : r, o.setProperty(s, n, r);
  } else
    e12.type & 12;
}
function Kp(e12, t, n) {
  let r = n.directiveStart, o = n.directiveEnd;
  Mt(n) && Mp(t, n, e12.data[r + n.componentOffset]), e12.firstCreatePass || Pl(n, t);
  let i = n.initialInputs;
  for (let s = r; s < o; s++) {
    let a = e12.data[s], c = Ar(t, e12, s, n);
    if (Pt(c, t), i !== null && eh(t, s - r, c, a, n, i), _t(a)) {
      let l = we(n.index, t);
      l[x] = Ar(t, e12, s, n);
    }
  }
}
function Jp(e12, t, n) {
  let r = n.directiveStart, o = n.directiveEnd, i = n.index, s = Oc();
  try {
    Ue(i);
    for (let a = r; a < o; a++) {
      let c = e12.data[a], l = t[a];
      pr(a), (c.hostBindings !== null || c.hostVars !== 0 || c.hostAttrs !== null) && Xp(c, l);
    }
  } finally {
    Ue(-1), pr(s);
  }
}
function Xp(e12, t) {
  e12.hostBindings !== null && e12.hostBindings(1, t);
}
function eh(e12, t, n, r, o, i) {
  let s = i[t];
  if (s !== null)
    for (let a = 0; a < s.length; a += 2) {
      let c = s[a], l = s[a + 1];
      ls(r, n, c, l);
    }
}
function th(e12, t, n, r, o) {
  let i = B + n, s = t[m], a = o(s, t, e12, r, n);
  t[i] = a, xt(e12, true);
  let c = e12.type === 2;
  return c ? (lu(t[O], a, e12), (Dc() === 0 || wi(e12)) && Pt(a, t), bc()) : Pt(a, t), yr() && (!c || !Fs(e12)) && Ys(s, t, a, e12), e12;
}
function nh(e12) {
  let t = e12;
  return Ai() ? Sc() : (t = t.parent, xt(t, false)), t;
}
function rh(e12, t) {
  let n = e12[be];
  if (!n)
    return;
  let r;
  try {
    r = n.get(st, null);
  } catch {
    r = null;
  }
  r?.(t);
}
function oh(e12, t, n, r, o) {
  let i = e12.inputs?.[r], s = e12.hostDirectiveInputs?.[r], a = false;
  if (s)
    for (let c = 0; c < s.length; c += 2) {
      let l = s[c], u = s[c + 1], d = t.data[l];
      ls(d, n[l], u, o), a = true;
    }
  if (i)
    for (let c of i) {
      let l = n[c], u = t.data[c];
      ls(u, l, r, o), a = true;
    }
  return a;
}
function ih(e12, t) {
  let n = we(t, e12), r = n[m];
  sh(r, n);
  let o = n[re];
  o !== null && n[Ct] === null && (n[Ct] = Jl(o, n[be])), T(C.ComponentStart);
  try {
    Js(r, n, n[x]);
  } finally {
    T(C.ComponentEnd, n[x]);
  }
}
function sh(e12, t) {
  for (let n = t.length; n < e12.blueprint.length; n++)
    t.push(e12.blueprint[n]);
}
function Js(e12, t, n) {
  gr(t);
  try {
    let r = e12.viewQuery;
    r !== null && Xi(1, r, n);
    let o = e12.template;
    o !== null && vu(e12, t, o, 1, n), e12.firstCreatePass && (e12.firstCreatePass = false), t[fe]?.finishViewCreation(e12), e12.staticContentQueries && Xl(e12, t), e12.staticViewQueries && Xi(2, e12.viewQuery, n);
    let i = e12.components;
    i !== null && ah(t, i);
  } catch (r) {
    throw e12.firstCreatePass && (e12.incompleteFirstPass = true, e12.firstCreatePass = false), r;
  } finally {
    t[y] &= -5, mr();
  }
}
function ah(e12, t) {
  for (let n = 0; n < t.length; n++)
    ih(e12, t[n]);
}
function Jr(e12, t, n, r) {
  let o = g(null);
  try {
    let i = t.tView, a = e12[y] & 4096 ? 4096 : 16, c = Ws(e12, i, n, a, null, t, null, null, r?.injector ?? null, r?.embeddedViewInjector ?? null, r?.dehydratedView ?? null), l = e12[t.index];
    c[je] = l;
    let u = e12[fe];
    return u !== null && (c[fe] = u.createEmbeddedView(i)), Js(i, c, n), c;
  } finally {
    g(o);
  }
}
function un(e12, t) {
  return !t || t.firstChild === null || $l(e12);
}
function dn(e12, t, n, r, o = false) {
  for (; n !== null; ) {
    if (n.type === 128) {
      n = o ? n.projectionNext : n.next;
      continue;
    }
    let i = t[n.index];
    i !== null && r.push(te(i)), oe(i) && Iu(i, r);
    let s = n.type;
    if (s & 8)
      dn(e12, t, n.child, r);
    else if (s & 32) {
      let a = qs(n, t), c;
      for (; c = a(); )
        r.push(c);
    } else if (s & 16) {
      let a = yu(t, n);
      if (Array.isArray(a))
        r.push(...a);
      else {
        let c = Le(t[ee]);
        dn(c[m], c, a, r, true);
      }
    }
    n = o ? n.projectionNext : n.next;
  }
  return r;
}
function Iu(e12, t) {
  for (let n = S; n < e12.length; n++) {
    let r = e12[n], o = r[m].firstChild;
    o !== null && dn(r[m], r, o, t);
  }
  e12[Ve] !== e12[re] && t.push(e12[Ve]);
}
function Du(e12) {
  if (e12[lr] !== null) {
    for (let t of e12[lr])
      t.impl.addSequence(t);
    e12[lr].length = 0;
  }
}
var bu = [];
function ch(e12) {
  return e12[Z] ?? lh(e12);
}
function lh(e12) {
  let t = bu.pop() ?? Object.create(dh);
  return t.lView = e12, t;
}
function uh(e12) {
  e12.lView[Z] !== e12 && (e12.lView = null, bu.push(e12));
}
var dh = R(N({}, ft), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e12) => {
  Nt(e12.lView);
}, consumerOnSignalRead() {
  this.lView[Z] = this;
} });
function fh(e12) {
  let t = e12[Z] ?? Object.create(ph);
  return t.lView = e12, t;
}
var ph = R(N({}, ft), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e12) => {
  let t = Le(e12.lView);
  for (; t && !Cu(t[m]); )
    t = Le(t);
  t && _i(t);
}, consumerOnSignalRead() {
  this.lView[Z] = this;
} });
function Cu(e12) {
  return e12.type !== 2;
}
function wu(e12) {
  if (e12[Pe] === null)
    return;
  let t = true;
  for (; t; ) {
    let n = false;
    for (let r of e12[Pe])
      r.dirty && (n = true, r.zone === null || Zone.current === r.zone ? r.run() : r.zone.run(() => r.run()));
    t = n && !!(e12[y] & 8192);
  }
}
var hh = 100;
function Tu(e12, t = 0) {
  let r = e12[de].rendererFactory, o = false;
  o || r.begin?.();
  try {
    gh(e12, t);
  } finally {
    o || r.end?.();
  }
}
function gh(e12, t) {
  let n = Oi();
  try {
    Zt(true), fs(e12, t);
    let r = 0;
    for (; nn(e12); ) {
      if (r === hh)
        throw new v(103, false);
      r++, fs(e12, 1);
    }
  } finally {
    Zt(n);
  }
}
function mh(e12, t, n, r) {
  if (it(t))
    return;
  let o = t[y], i = false, s = false;
  gr(t);
  let a = true, c = null, l = null;
  i || (Cu(e12) ? (l = ch(t), c = Ut(l)) : Pn() === null ? (a = false, l = fh(t), c = Ut(l)) : t[Z] && (pt(t[Z]), t[Z] = null));
  try {
    Mi(t), Nc(e12.bindingStartIndex), n !== null && vu(e12, t, n, 2, r);
    let u = (o & 3) === 3;
    if (!i)
      if (u) {
        let p = e12.preOrderCheckHooks;
        p !== null && Tr(t, p, null);
      } else {
        let p = e12.preOrderHooks;
        p !== null && Mr(t, p, 0, null), Ui(t, 0);
      }
    if (s || yh(t), wu(t), Mu(t, 0), e12.contentQueries !== null && Xl(e12, t), !i)
      if (u) {
        let p = e12.contentCheckHooks;
        p !== null && Tr(t, p);
      } else {
        let p = e12.contentHooks;
        p !== null && Mr(t, p, 1), Ui(t, 1);
      }
    Eh(e12, t);
    let d = e12.components;
    d !== null && Su(t, d, 0);
    let f = e12.viewQuery;
    if (f !== null && Xi(2, f, r), !i)
      if (u) {
        let p = e12.viewCheckHooks;
        p !== null && Tr(t, p);
      } else {
        let p = e12.viewHooks;
        p !== null && Mr(t, p, 2), Ui(t, 2);
      }
    if (e12.firstUpdatePass === true && (e12.firstUpdatePass = false), t[cr]) {
      for (let p of t[cr])
        p();
      t[cr] = null;
    }
    i || (Du(t), t[y] &= -73);
  } catch (u) {
    throw i || Nt(t), u;
  } finally {
    l !== null && (Ln(l, c), a && uh(l)), mr();
  }
}
function Mu(e12, t) {
  for (let n = zl(e12); n !== null; n = Wl(n))
    for (let r = S; r < n.length; r++) {
      let o = n[r];
      _u(o, t);
    }
}
function yh(e12) {
  for (let t = zl(e12); t !== null; t = Wl(t)) {
    if (!(t[y] & 2))
      continue;
    let n = t[ot];
    for (let r = 0; r < n.length; r++) {
      let o = n[r];
      _i(o);
    }
  }
}
function vh(e12, t, n) {
  T(C.ComponentStart);
  let r = we(t, e12);
  try {
    _u(r, n);
  } finally {
    T(C.ComponentEnd, r[x]);
  }
}
function _u(e12, t) {
  dr(e12) && fs(e12, t);
}
function fs(e12, t) {
  let r = e12[m], o = e12[y], i = e12[Z], s = !!(t === 0 && o & 16);
  if (s ||= !!(o & 64 && t === 0), s ||= !!(o & 1024), s ||= !!(i?.dirty && Fn(i)), s ||= false, i && (i.dirty = false), e12[y] &= -9217, s)
    mh(r, e12, r.template, e12[x]);
  else if (o & 8192) {
    let a = g(null);
    try {
      wu(e12), Mu(e12, 1);
      let c = r.components;
      c !== null && Su(e12, c, 1), Du(e12);
    } finally {
      g(a);
    }
  }
}
function Su(e12, t, n) {
  for (let r = 0; r < t.length; r++)
    vh(e12, t[r], n);
}
function Eh(e12, t) {
  let n = e12.hostBindingOpCodes;
  if (n !== null)
    try {
      for (let r = 0; r < n.length; r++) {
        let o = n[r];
        if (o < 0)
          Ue(~o);
        else {
          let i = o, s = n[++r], a = n[++r];
          Ac(s, i);
          let c = t[i];
          T(C.HostBindingsUpdateStart, c);
          try {
            a(2, c);
          } finally {
            T(C.HostBindingsUpdateEnd, c);
          }
        }
      }
    } finally {
      Ue(-1);
    }
}
function Xs(e12, t) {
  let n = Oi() ? 64 : 1088;
  for (e12[de].changeDetectionScheduler?.notify(t); e12; ) {
    e12[y] |= n;
    let r = Le(e12);
    if (St(e12) && !r)
      return e12;
    e12 = r;
  }
  return null;
}
function Nu(e12, t, n, r) {
  return [e12, true, 0, t, null, r, null, n, null, null];
}
function xu(e12, t) {
  let n = S + t;
  if (n < e12.length)
    return e12[n];
}
function Xr(e12, t, n, r = true) {
  let o = t[m];
  if (Ih(o, t, e12, n), r) {
    let s = ds(n, e12), a = t[O], c = a.parentNode(e12[Ve]);
    c !== null && Op(o, e12[X], a, t, c, s);
  }
  let i = t[Ct];
  i !== null && i.firstChild !== null && (i.firstChild = null);
}
function Ru(e12, t) {
  let n = fn(e12, t);
  return n !== void 0 && Yr(n[m], n), n;
}
function fn(e12, t) {
  if (e12.length <= S)
    return;
  let n = S + t, r = e12[n];
  if (r) {
    let o = r[je];
    o !== null && o !== e12 && Qs(o, r), t > 0 && (e12[n - 1][J] = r[J]);
    let i = Kt(e12, S + t);
    Ap(r[m], r);
    let s = i[fe];
    s !== null && s.detachView(i[m]), r[A] = null, r[J] = null, r[y] &= -129;
  }
  return r;
}
function Ih(e12, t, n, r) {
  let o = S + r, i = n.length;
  r > 0 && (n[o - 1][J] = t), r < i - S ? (t[J] = n[o], gi(n, S + r, t)) : (n.push(t), t[J] = null), t[A] = n;
  let s = t[je];
  s !== null && n !== s && Au(s, t);
  let a = t[fe];
  a !== null && a.insertView(e12), fr(t), t[y] |= 128;
}
function Au(e12, t) {
  let n = e12[ot], r = t[A];
  if (Be(r))
    e12[y] |= 2;
  else {
    let o = r[A][ee];
    t[ee] !== o && (e12[y] |= 2);
  }
  n === null ? e12[ot] = [t] : n.push(t);
}
var Lt = class {
  _lView;
  _cdRefInjectingView;
  _appRef = null;
  _attachedToViewContainer = false;
  exhaustive;
  get rootNodes() {
    let t = this._lView, n = t[m];
    return dn(n, t, n.firstChild, []);
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
    return it(this._lView);
  }
  destroy() {
    if (this._appRef)
      this._appRef.detachView(this);
    else if (this._attachedToViewContainer) {
      let t = this._lView[A];
      if (oe(t)) {
        let n = t[tn], r = n ? n.indexOf(this) : -1;
        r > -1 && (fn(t, r), Kt(n, r));
      }
      this._attachedToViewContainer = false;
    }
    Yr(this._lView[m], this._lView);
  }
  onDestroy(t) {
    Si(this._lView, t);
  }
  markForCheck() {
    Xs(this._cdRefInjectingView || this._lView, 4);
  }
  detach() {
    this._lView[y] &= -129;
  }
  reattach() {
    fr(this._lView), this._lView[y] |= 128;
  }
  detectChanges() {
    this._lView[y] |= 1024, Tu(this._lView);
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
    let t = St(this._lView), n = this._lView[je];
    n !== null && !t && Qs(n, this._lView), mu(this._lView[m], this._lView);
  }
  attachToAppRef(t) {
    if (this._attachedToViewContainer)
      throw new v(902, false);
    this._appRef = t;
    let n = St(this._lView), r = this._lView[je];
    r !== null && !n && Au(r, this._lView), fr(this._lView);
  }
};
var pn = /* @__PURE__ */ (() => {
  class e12 {
    _declarationLView;
    _declarationTContainer;
    elementRef;
    static __NG_ELEMENT_ID__ = Dh;
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
      let i = Jr(this._declarationLView, this._declarationTContainer, n, { embeddedViewInjector: r, dehydratedView: o });
      return new Lt(i);
    }
  }
  return e12;
})();
function Dh() {
  return ea(ge(), M());
}
function ea(e12, t) {
  return e12.type & 4 ? new pn(t, e12, jt(e12, t)) : null;
}
function eo(e12, t, n, r, o) {
  let i = e12.data[t];
  if (i === null)
    i = bh(e12, t, n, r, o), Rc() && (i.flags |= 32);
  else if (i.type & 64) {
    i.type = n, i.value = r, i.attrs = o;
    let s = _c();
    i.injectorIndex = s === null ? -1 : s.injectorIndex;
  }
  return xt(i, true), i;
}
function bh(e12, t, n, r, o) {
  let i = Ri(), s = Ai(), a = s ? i : i && i.parent, c = e12.data[t] = wh(e12, a, n, t, r, o);
  return Ch(e12, c, i, s), c;
}
function Ch(e12, t, n, r) {
  e12.firstChild === null && (e12.firstChild = t), n !== null && (r ? n.child == null && t.parent !== null && (n.child = t) : n.next === null && (n.next = t, t.prev = n));
}
function wh(e12, t, n, r, o, i) {
  let s = t ? t.injectorIndex : -1, a = 0;
  return wc() && (a |= 128), { type: n, index: r, insertBeforeIndex: null, injectorIndex: s, directiveStart: -1, directiveEnd: -1, directiveStylingLast: -1, componentOffset: -1, controlDirectiveIndex: -1, customControlIndex: -1, propertyBindings: null, flags: a, providerIndexes: 0, value: o, attrs: i, mergedAttrs: null, localNames: null, initialInputs: null, inputs: null, hostDirectiveInputs: null, outputs: null, hostDirectiveOutputs: null, directiveToIndex: null, tView: null, next: null, prev: null, projectionNext: null, child: null, parent: t, projection: null, styles: null, stylesWithoutHost: null, residualStyles: void 0, classes: null, classesWithoutHost: null, residualClasses: void 0, classBindings: 0, styleBindings: 0 };
}
function Th(e12) {
  let t = e12[bi] ?? [], r = e12[A][O], o = [];
  for (let i of t)
    i.data[Ql] !== void 0 ? o.push(i) : Mh(i, r);
  e12[bi] = o;
}
function Mh(e12, t) {
  let n = 0, r = e12.firstChild;
  if (r) {
    let o = e12.data[Zl];
    for (; n < o; ) {
      let i = r.nextSibling;
      cu(t, r, false), r = i, n++;
    }
  }
}
var _h = () => null;
var Sh = () => null;
function ps(e12, t) {
  return _h(e12, t);
}
function Ou(e12, t, n) {
  return Sh(e12, t, n);
}
var ku = class {
};
var to = class {
};
var hs = class {
  resolveComponentFactory(t) {
    throw new v(917, false);
  }
};
var no = class {
  static NULL = new hs();
};
var lt = class {
};
var Pu = (() => {
  class e12 {
    static \u0275prov = _({ token: e12, providedIn: "root", factory: () => null });
  }
  return e12;
})();
var Sr = {};
var gs = class {
  injector;
  parentInjector;
  constructor(t, n) {
    this.injector = t, this.parentInjector = n;
  }
  get(t, n, r) {
    let o = this.injector.get(t, Sr, r);
    return o !== Sr || n === Sr ? o : this.parentInjector.get(t, n, r);
  }
};
function Pr(e12, t, n) {
  let r = n ? e12.styles : null, o = n ? e12.classes : null, i = 0;
  if (t !== null)
    for (let s = 0; s < t.length; s++) {
      let a = t[s];
      if (typeof a == "number")
        i = a;
      else if (i == 1)
        o = ii(o, a);
      else if (i == 2) {
        let c = a, l = t[++s];
        r = ii(r, c + ": " + l + ";");
      }
    }
  n ? e12.styles = r : e12.stylesWithoutHost = r, n ? e12.classes = o : e12.classesWithoutHost = o;
}
function Lu(e12, t = 0) {
  let n = M();
  if (n === null)
    return b(e12, t);
  let r = ge();
  return Hl(r, n, q(e12), t);
}
function Nh(e12, t, n, r, o) {
  let i = r === null ? null : { "": -1 }, s = o(e12, n);
  if (s !== null) {
    let a = s, c = null, l = null;
    for (let u of s)
      if (u.resolveHostDirectives !== null) {
        [a, c, l] = u.resolveHostDirectives(s);
        break;
      }
    Ah(e12, t, n, a, i, c, l);
  }
  i !== null && r !== null && xh(n, r, i);
}
function xh(e12, t, n) {
  let r = e12.localNames = [];
  for (let o = 0; o < t.length; o += 2) {
    let i = n[t[o + 1]];
    if (i == null)
      throw new v(-301, false);
    r.push(t[o], i);
  }
}
function Rh(e12, t, n) {
  t.componentOffset = n, (e12.components ??= []).push(t.index);
}
function Ah(e12, t, n, r, o, i, s) {
  let a = r.length, c = null;
  for (let f = 0; f < a; f++) {
    let p = r[f];
    c === null && _t(p) && (c = p, Rh(e12, n, f)), Of(Pl(n, t), e12, p.type);
  }
  jh(n, e12.data.length, a), c?.viewProvidersResolver && c.viewProvidersResolver(c);
  for (let f = 0; f < a; f++) {
    let p = r[f];
    p.providersResolver && p.providersResolver(p);
  }
  let l = false, u = false, d = du(e12, t, a, null);
  a > 0 && (n.directiveToIndex = /* @__PURE__ */ new Map());
  for (let f = 0; f < a; f++) {
    let p = r[f];
    if (n.mergedAttrs = $r(n.mergedAttrs, p.hostAttrs), kh(e12, n, t, d, p), Fh(d, p, o), s !== null && s.has(p)) {
      let [L, H] = s.get(p);
      n.directiveToIndex.set(p.type, [d, L + n.directiveStart, H + n.directiveStart]);
    } else
      (i === null || !i.has(p)) && n.directiveToIndex.set(p.type, d);
    p.contentQueries !== null && (n.flags |= 4), (p.hostBindings !== null || p.hostAttrs !== null || p.hostVars !== 0) && (n.flags |= 64);
    let h = p.type.prototype;
    !l && (h.ngOnChanges || h.ngOnInit || h.ngDoCheck) && ((e12.preOrderHooks ??= []).push(n.index), l = true), !u && (h.ngOnChanges || h.ngDoCheck) && ((e12.preOrderCheckHooks ??= []).push(n.index), u = true), d++;
  }
  Oh(e12, n, i);
}
function Oh(e12, t, n) {
  for (let r = t.directiveStart; r < t.directiveEnd; r++) {
    let o = e12.data[r];
    if (n === null || !n.has(o))
      ml(0, t, o, r), ml(1, t, o, r), vl(t, r, false);
    else {
      let i = n.get(o);
      yl(0, t, i, r), yl(1, t, i, r), vl(t, r, true);
    }
  }
}
function ml(e12, t, n, r) {
  let o = e12 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s;
      e12 === 0 ? s = t.inputs ??= {} : s = t.outputs ??= {}, s[i] ??= [], s[i].push(r), Fu(t, i);
    }
}
function yl(e12, t, n, r) {
  let o = e12 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s = o[i], a;
      e12 === 0 ? a = t.hostDirectiveInputs ??= {} : a = t.hostDirectiveOutputs ??= {}, a[s] ??= [], a[s].push(r, i), Fu(t, s);
    }
}
function Fu(e12, t) {
  t === "class" ? e12.flags |= 8 : t === "style" && (e12.flags |= 16);
}
function vl(e12, t, n) {
  let { attrs: r, inputs: o, hostDirectiveInputs: i } = e12;
  if (r === null || !n && o === null || n && i === null || Ip(e12)) {
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
function kh(e12, t, n, r, o) {
  e12.data[r] = o;
  let i = o.factory || (o.factory = Dt(o.type, true)), s = new ln(i, _t(o), Lu, null);
  e12.blueprint[r] = s, n[r] = s, Ph(e12, t, r, du(e12, n, o.hostVars, Re), o);
}
function Ph(e12, t, n, r, o) {
  let i = o.hostBindings;
  if (i) {
    let s = e12.hostBindingOpCodes;
    s === null && (s = e12.hostBindingOpCodes = []);
    let a = ~t.index;
    Lh(s) != a && s.push(a), s.push(n, r, i);
  }
}
function Lh(e12) {
  let t = e12.length;
  for (; t > 0; ) {
    let n = e12[--t];
    if (typeof n == "number" && n < 0)
      return n;
  }
  return 0;
}
function Fh(e12, t, n) {
  if (n) {
    if (t.exportAs)
      for (let r = 0; r < t.exportAs.length; r++)
        n[t.exportAs[r]] = e12;
    _t(t) && (n[""] = e12);
  }
}
function jh(e12, t, n) {
  e12.flags |= 1, e12.directiveStart = t, e12.directiveEnd = t + n, e12.providerIndexes = t;
}
function Hh(e12, t, n, r, o, i, s, a) {
  let c = t[m], l = c.consts, u = he(l, s), d = eo(c, e12, n, r, u);
  return i && Nh(c, t, d, he(l, a), o), d.mergedAttrs = $r(d.mergedAttrs, d.attrs), d.attrs !== null && Pr(d, d.attrs, false), d.mergedAttrs !== null && Pr(d, d.mergedAttrs, true), c.queries !== null && c.queries.elementStart(c, d), d;
}
function Vh(e12, t) {
  Tf(e12, t), Ci(t) && e12.queries.elementEnd(t);
}
function Bh(e12, t, n, r, o, i) {
  let s = t.consts, a = he(s, o), c = eo(t, e12, n, r, a);
  if (c.mergedAttrs = $r(c.mergedAttrs, c.attrs), i != null) {
    let l = he(s, i);
    c.localNames = [];
    for (let u = 0; u < l.length; u += 2)
      c.localNames.push(l[u], -1);
  }
  return c.attrs !== null && Pr(c, c.attrs, false), c.mergedAttrs !== null && Pr(c, c.mergedAttrs, true), t.queries !== null && t.queries.elementStart(t, c), c;
}
function In(e12, t, n) {
  if (n === Re)
    return false;
  let r = e12[t];
  return Object.is(r, n) ? false : (e12[t] = n, true);
}
function $h(e12, t, n) {
  return function r(o) {
    let i = r.__ngNativeEl__;
    i !== void 0 && Wf(o, i);
    let s = Mt(e12) ? we(e12.index, t) : t;
    Xs(s, 5);
    let a = t[x], c = El(t, a, n, o), l = r.__ngNextListenerFn__;
    for (; l; )
      c = El(t, a, l, o) && c, l = l.__ngNextListenerFn__;
    return c;
  };
}
function El(e12, t, n, r) {
  let o = g(null);
  try {
    return T(C.OutputStart, t, n), n(r) !== false;
  } catch (i) {
    return rh(e12, i), false;
  } finally {
    T(C.OutputEnd, t, n), g(o);
  }
}
function Uh(e12, t, n, r, o, i, s, a) {
  let c = wi(e12), l = false, u = null;
  if (!r && c && (u = Wh(t, n, i, e12.index)), u !== null) {
    let d = u.__ngLastListenerFn__ || u;
    d.__ngNextListenerFn__ = s, u.__ngLastListenerFn__ = s, l = true;
  } else {
    let d = pe(e12, n), f = r ? r(d) : d;
    qf(n, f, i, a), r || (a.__ngNativeEl__ = d);
    let p = o.listen(f, i, a);
    if (!zh(i)) {
      let h = r ? (L) => r(te(L[e12.index])) : e12.index;
      Gh(h, t, n, i, a, p, false);
    }
  }
  return l;
}
function zh(e12) {
  return e12.startsWith("animation") || e12.startsWith("transition");
}
function Wh(e12, t, n, r) {
  let o = e12.cleanup;
  if (o != null)
    for (let i = 0; i < o.length - 1; i += 2) {
      let s = o[i];
      if (s === n && o[i + 1] === r) {
        let a = t[wt], c = o[i + 2];
        return a && a.length > c ? a[c] : null;
      }
      typeof s == "string" && (i += 2);
    }
  return null;
}
function Gh(e12, t, n, r, o, i, s) {
  let a = t.firstCreatePass ? xi(t) : null, c = Ni(n), l = c.length;
  c.push(o, i), a && a.push(r, e12, l, (l + 1) * (s ? -1 : 1));
}
var ms = Symbol("BINDING");
function qh(e12) {
  return e12.debugInfo?.className || e12.type.name || null;
}
var ys = class extends no {
  ngModule;
  constructor(t) {
    super(), this.ngModule = t;
  }
  resolveComponentFactory(t) {
    let n = Xe(t);
    return new hn(n, this.ngModule);
  }
};
function Zh(e12) {
  return Object.keys(e12).map((t) => {
    let [n, r, o] = e12[t], i = { propName: n, templateName: t, isSignal: (r & Qr.SignalBased) !== 0 };
    return o && (i.transform = o), i;
  });
}
function Qh(e12) {
  return Object.keys(e12).map((t) => ({ propName: e12[t], templateName: t }));
}
function Yh(e12, t, n) {
  let r = t instanceof Y ? t : t?.injector;
  return r && e12.getStandaloneInjector !== null && (r = e12.getStandaloneInjector(r) || r), r ? new gs(n, r) : n;
}
function Kh(e12) {
  let t = e12.get(lt, null);
  if (t === null)
    throw new v(407, false);
  let n = e12.get(Pu, null), r = e12.get(Ke, null), o = e12.get(Ht, null, { optional: true });
  return { rendererFactory: t, sanitizer: n, changeDetectionScheduler: r, ngReflect: false, tracingService: o };
}
function Jh(e12, t) {
  let n = ju(e12);
  return su(t, n, n === "svg" ? hc : n === "math" ? gc : null);
}
function ju(e12) {
  return (e12.selectors[0][0] || "div").toLowerCase();
}
var hn = class extends to {
  componentDef;
  ngModule;
  selector;
  componentType;
  ngContentSelectors;
  isBoundToModule;
  cachedInputs = null;
  cachedOutputs = null;
  get inputs() {
    return this.cachedInputs ??= Zh(this.componentDef.inputs), this.cachedInputs;
  }
  get outputs() {
    return this.cachedOutputs ??= Qh(this.componentDef.outputs), this.cachedOutputs;
  }
  constructor(t, n) {
    super(), this.componentDef = t, this.ngModule = n, this.componentType = t.type, this.selector = bp(t.selectors), this.ngContentSelectors = t.ngContentSelectors ?? [], this.isBoundToModule = !!n;
  }
  create(t, n, r, o, i, s) {
    T(C.DynamicComponentStart);
    let a = g(null);
    try {
      let c = this.componentDef, l = Yh(c, o || this.ngModule, t), u = Kh(l), d = u.tracingService;
      return d && d.componentCreate ? d.componentCreate(qh(c), () => this.createComponentRef(u, l, n, r, i, s)) : this.createComponentRef(u, l, n, r, i, s);
    } finally {
      g(a);
    }
  }
  createComponentRef(t, n, r, o, i, s) {
    let a = this.componentDef, c = Xh(o, a, s, i), l = t.rendererFactory.createRenderer(null, a), u = o ? qp(l, o, a.encapsulation, n) : Jh(a, l), d = s?.some(Il) || i?.some((h) => typeof h != "function" && h.bindings.some(Il)), f = Ws(null, c, null, 512 | uu(a), null, null, t, l, n, null, Jl(u, n, true));
    f[B] = u, gr(f);
    let p = null;
    try {
      let h = Hh(B, f, 2, "#host", () => c.directiveRegistry, true, 0);
      lu(l, u, h), Pt(u, f), Gp(c, f, h), Qf(c, h, f), Vh(c, h), r !== void 0 && tg(h, this.ngContentSelectors, r), p = we(h.index, f), f[x] = p[x], Js(c, f, null);
    } catch (h) {
      throw p !== null && Ki(p), Ki(f), h;
    } finally {
      T(C.DynamicComponentEnd), mr();
    }
    return new Lr(this.componentType, f, !!d);
  }
};
function Xh(e12, t, n, r) {
  let o = e12 ? ["ng-version", "21.2.11"] : Cp(t.selectors[0]), i = null, s = null, a = 0;
  if (n)
    for (let u of n)
      a += u[ms].requiredVars, u.create && (u.targetIdx = 0, (i ??= []).push(u)), u.update && (u.targetIdx = 0, (s ??= []).push(u));
  if (r)
    for (let u = 0; u < r.length; u++) {
      let d = r[u];
      if (typeof d != "function")
        for (let f of d.bindings) {
          a += f[ms].requiredVars;
          let p = u + 1;
          f.create && (f.targetIdx = p, (i ??= []).push(f)), f.update && (f.targetIdx = p, (s ??= []).push(f));
        }
    }
  let c = [t];
  if (r)
    for (let u of r) {
      let d = typeof u == "function" ? u : u.type, f = ui(d);
      c.push(f);
    }
  return zs(0, null, eg(i, s), 1, a, c, null, null, null, [o], null);
}
function eg(e12, t) {
  return !e12 && !t ? null : (n) => {
    if (n & 1 && e12)
      for (let r of e12)
        r.create();
    if (n & 2 && t)
      for (let r of t)
        r.update();
  };
}
function Il(e12) {
  let t = e12[ms].kind;
  return t === "input" || t === "twoWay";
}
var Lr = class extends ku {
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
    super(), this._rootLView = n, this._hasInputBindings = r, this._tNode = ur(n[m], B), this.location = jt(this._tNode, n), this.instance = we(this._tNode.index, n)[x], this.hostView = this.changeDetectorRef = new Lt(n, void 0), this.componentType = t;
  }
  setInput(t, n) {
    this._hasInputBindings;
    let r = this._tNode;
    if (this.previousInputValues ??= /* @__PURE__ */ new Map(), this.previousInputValues.has(t) && Object.is(this.previousInputValues.get(t), n))
      return;
    let o = this._rootLView, i = oh(r, o[m], o, t, n);
    this.previousInputValues.set(t, n);
    let s = we(r.index, o);
    Xs(s, 1);
  }
  get injector() {
    return new at(this._tNode, this._rootLView);
  }
  destroy() {
    this.hostView.destroy();
  }
  onDestroy(t) {
    this.hostView.onDestroy(t);
  }
};
function tg(e12, t, n) {
  let r = e12.projection = [];
  for (let o = 0; o < t.length; o++) {
    let i = n[o];
    r.push(i != null && i.length ? Array.from(i) : null);
  }
}
var ro = /* @__PURE__ */ (() => {
  class e12 {
    static __NG_ELEMENT_ID__ = ng;
  }
  return e12;
})();
function ng() {
  let e12 = ge();
  return Hu(e12, M());
}
var vs = class e4 extends ro {
  _lContainer;
  _hostTNode;
  _hostLView;
  constructor(t, n, r) {
    super(), this._lContainer = t, this._hostTNode = n, this._hostLView = r;
  }
  get element() {
    return jt(this._hostTNode, this._hostLView);
  }
  get injector() {
    return new at(this._hostTNode, this._hostLView);
  }
  get parentInjector() {
    let t = ks(this._hostTNode, this._hostLView);
    if (Al(t)) {
      let n = Rr(t, this._hostLView), r = xr(t), o = n[m].data[r + 8];
      return new at(o, n);
    } else
      return new at(null, this._hostLView);
  }
  clear() {
    for (; this.length > 0; )
      this.remove(this.length - 1);
  }
  get(t) {
    let n = Dl(this._lContainer);
    return n !== null && n[t] || null;
  }
  get length() {
    return this._lContainer.length - S;
  }
  createEmbeddedView(t, n, r) {
    let o, i;
    typeof r == "number" ? o = r : r != null && (o = r.index, i = r.injector);
    let s = ps(this._lContainer, t.ssrId), a = t.createEmbeddedViewImpl(n || {}, i, s);
    return this.insertImpl(a, o, un(this._hostTNode, s)), a;
  }
  createComponent(t, n, r, o, i, s, a) {
    let c = t && !Ef(t), l;
    if (c)
      l = n;
    else {
      let H = n || {};
      l = H.index, r = H.injector, o = H.projectableNodes, i = H.environmentInjector || H.ngModuleRef, s = H.directives, a = H.bindings;
    }
    let u = c ? t : new hn(Xe(t)), d = r || this.parentInjector;
    if (!i && u.ngModule == null) {
      let dt = (c ? d : this.parentInjector).get(Y, null);
      dt && (i = dt);
    }
    let f = Xe(u.componentType ?? {}), p = ps(this._lContainer, f?.id ?? null), h = p?.firstChild ?? null, L = u.create(d, o, h, i, s, a);
    return this.insertImpl(L.hostView, l, un(this._hostTNode, p)), L;
  }
  insert(t, n) {
    return this.insertImpl(t, n, true);
  }
  insertImpl(t, n, r) {
    let o = t._lView;
    if (yc(o)) {
      let a = this.indexOf(t);
      if (a !== -1)
        this.detach(a);
      else {
        let c = o[A], l = new e4(c, c[X], c[A]);
        l.detach(l.indexOf(t));
      }
    }
    let i = this._adjustIndex(n), s = this._lContainer;
    return Xr(s, o, i, r), t.attachToViewContainerRef(), gi(Gi(s), i, t), t;
  }
  move(t, n) {
    return this.insert(t, n);
  }
  indexOf(t) {
    let n = Dl(this._lContainer);
    return n !== null ? n.indexOf(t) : -1;
  }
  remove(t) {
    let n = this._adjustIndex(t, -1), r = fn(this._lContainer, n);
    r && (Kt(Gi(this._lContainer), n), Yr(r[m], r));
  }
  detach(t) {
    let n = this._adjustIndex(t, -1), r = fn(this._lContainer, n);
    return r && Kt(Gi(this._lContainer), n) != null ? new Lt(r) : null;
  }
  _adjustIndex(t, n = 0) {
    return t ?? this.length + n;
  }
};
function Dl(e12) {
  return e12[tn];
}
function Gi(e12) {
  return e12[tn] || (e12[tn] = []);
}
function Hu(e12, t) {
  let n, r = t[e12.index];
  return oe(r) ? n = r : (n = Nu(r, t, null, e12), t[e12.index] = n, Gs(t, n)), og(n, t, e12, r), new vs(n, e12, t);
}
function rg(e12, t) {
  let n = e12[O], r = n.createComment(""), o = pe(t, e12), i = n.parentNode(o);
  return kr(n, i, r, n.nextSibling(o), false), r;
}
var og = ag;
var ig = () => false;
function sg(e12, t, n) {
  return ig(e12, t, n);
}
function ag(e12, t, n, r) {
  if (e12[Ve])
    return;
  let o;
  n.type & 8 ? o = te(r) : o = rg(t, n), e12[Ve] = o;
}
var Es = class e5 {
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
var Is = class e6 {
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
      ta(t, n).matches !== null && this.queries[n].setDirty();
  }
};
var Ds = class {
  flags;
  read;
  predicate;
  constructor(t, n, r = null) {
    this.flags = n, this.read = r, typeof t == "string" ? this.predicate = gg(t) : this.predicate = t;
  }
};
var bs = class e7 {
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
var Cs = class e8 {
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
        this.matchTNodeWithReadOption(t, n, cg(n, i)), this.matchTNodeWithReadOption(t, n, _r(n, t, i, false, false));
      }
    else
      r === pn ? n.type & 4 && this.matchTNodeWithReadOption(t, n, -1) : this.matchTNodeWithReadOption(t, n, _r(n, t, r, false, false));
  }
  matchTNodeWithReadOption(t, n, r) {
    if (r !== null) {
      let o = this.metadata.read;
      if (o !== null)
        if (o === yn || o === ro || o === pn && n.type & 4)
          this.addMatch(n.index, -2);
        else {
          let i = _r(n, t, o, false, false);
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
function cg(e12, t) {
  let n = e12.localNames;
  if (n !== null) {
    for (let r = 0; r < n.length; r += 2)
      if (n[r] === t)
        return n[r + 1];
  }
  return null;
}
function lg(e12, t) {
  return e12.type & 11 ? jt(e12, t) : e12.type & 4 ? ea(e12, t) : null;
}
function ug(e12, t, n, r) {
  return n === -1 ? lg(t, e12) : n === -2 ? dg(e12, t, r) : Ar(e12, e12[m], n, t);
}
function dg(e12, t, n) {
  if (n === yn)
    return jt(t, e12);
  if (n === pn)
    return ea(t, e12);
  if (n === ro)
    return Hu(t, e12);
}
function Vu(e12, t, n, r) {
  let o = t[fe].queries[r];
  if (o.matches === null) {
    let i = e12.data, s = n.matches, a = [];
    for (let c = 0; s !== null && c < s.length; c += 2) {
      let l = s[c];
      if (l < 0)
        a.push(null);
      else {
        let u = i[l];
        a.push(ug(t, u, s[c + 1], n.metadata.read));
      }
    }
    o.matches = a;
  }
  return o.matches;
}
function ws(e12, t, n, r) {
  let o = e12.queries.getByIndex(n), i = o.matches;
  if (i !== null) {
    let s = Vu(e12, t, o, n);
    for (let a = 0; a < i.length; a += 2) {
      let c = i[a];
      if (c > 0)
        r.push(s[a / 2]);
      else {
        let l = i[a + 1], u = t[-c];
        for (let d = S; d < u.length; d++) {
          let f = u[d];
          f[je] === f[A] && ws(f[m], f, l, r);
        }
        if (u[ot] !== null) {
          let d = u[ot];
          for (let f = 0; f < d.length; f++) {
            let p = d[f];
            ws(p[m], p, l, r);
          }
        }
      }
    }
  }
  return r;
}
function fg(e12, t) {
  return e12[fe].queries[t].queryList;
}
function pg(e12, t, n) {
  let r = new Or((n & 4) === 4);
  return Ic(e12, t, r, r.destroy), (t[fe] ??= new Is()).queries.push(new Es(r)) - 1;
}
function hg(e12, t, n) {
  let r = ie();
  return r.firstCreatePass && (mg(r, new Ds(e12, t, n), -1), (t & 2) === 2 && (r.staticViewQueries = true)), pg(r, M(), t);
}
function gg(e12) {
  return e12.split(",").map((t) => t.trim());
}
function mg(e12, t, n) {
  e12.queries === null && (e12.queries = new bs()), e12.queries.track(new Cs(t, n));
}
function ta(e12, t) {
  return e12.queries.getByIndex(t);
}
function yg(e12, t) {
  let n = e12[m], r = ta(n, t);
  return r.crossesNgTemplate ? ws(n, e12, t, []) : Vu(n, e12, r, t);
}
var Fr = class {
};
var gn = class extends Fr {
  injector;
  componentFactoryResolver = new ys(this);
  instance = null;
  constructor(t) {
    super();
    let n = new Ye([...t.providers, { provide: Fr, useValue: this }, { provide: no, useValue: this.componentFactoryResolver }], t.parent || en(), t.debugName, /* @__PURE__ */ new Set(["environment"]));
    this.injector = n, t.runEnvironmentInitializers && n.resolveInjectorInitializers();
  }
  destroy() {
    this.injector.destroy();
  }
  onDestroy(t) {
    this.injector.onDestroy(t);
  }
};
function Bu(e12, t, n = null) {
  return new gn({ providers: e12, parent: t, debugName: n, runEnvironmentInitializers: true }).injector;
}
var vg = (() => {
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
        let r = vi(false, n.type), o = r.length > 0 ? Bu([r], this._injector, "") : null;
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
    static \u0275prov = _({ token: e12, providedIn: "environment", factory: () => new e12(b(Y)) });
  }
  return e12;
})();
function na(e12) {
  return _l(() => {
    let t = bg(e12), n = R(N({}, t), { decls: e12.decls, vars: e12.vars, template: e12.template, consts: e12.consts || null, ngContentSelectors: e12.ngContentSelectors, onPush: e12.changeDetection === Ps.OnPush, directiveDefs: null, pipeDefs: null, dependencies: t.standalone && e12.dependencies || null, getStandaloneInjector: t.standalone ? (o) => o.get(vg).getOrCreateStandaloneInjector(n) : null, getExternalStyles: null, signals: e12.signals ?? false, data: e12.data || {}, encapsulation: e12.encapsulation || se.Emulated, styles: e12.styles || ke, _: null, schemas: e12.schemas || null, tView: null, id: "" });
    t.standalone && Vt("NgStandalone"), Cg(n);
    let r = e12.dependencies;
    return n.directiveDefs = bl(r, Eg), n.pipeDefs = bl(r, Xa), n.id = wg(n), n;
  });
}
function Eg(e12) {
  return Xe(e12) || ui(e12);
}
function Ig(e12, t) {
  if (e12 == null)
    return et;
  let n = {};
  for (let r in e12)
    if (e12.hasOwnProperty(r)) {
      let o = e12[r], i, s, a, c;
      Array.isArray(o) ? (a = o[0], i = o[1], s = o[2] ?? i, c = o[3] || null) : (i = o, s = o, a = Qr.None, c = null), n[i] = [r, a, c], t[i] = s;
    }
  return n;
}
function Dg(e12) {
  if (e12 == null)
    return et;
  let t = {};
  for (let n in e12)
    e12.hasOwnProperty(n) && (t[e12[n]] = n);
  return t;
}
function bg(e12) {
  let t = {};
  return { type: e12.type, providersResolver: null, viewProvidersResolver: null, factory: null, hostBindings: e12.hostBindings || null, hostVars: e12.hostVars || 0, hostAttrs: e12.hostAttrs || null, contentQueries: e12.contentQueries || null, declaredInputs: t, inputConfig: e12.inputs || et, exportAs: e12.exportAs || null, standalone: e12.standalone ?? true, signals: e12.signals === true, selectors: e12.selectors || ke, viewQuery: e12.viewQuery || null, features: e12.features || null, setInput: null, resolveHostDirectives: null, hostDirectives: null, controlDef: null, inputs: Ig(e12.inputs, t), outputs: Dg(e12.outputs), debugInfo: null };
}
function Cg(e12) {
  e12.features?.forEach((t) => t(e12));
}
function bl(e12, t) {
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
function Tg(e12, t, n, r, o, i, s, a) {
  if (n.firstCreatePass) {
    e12.mergedAttrs = $r(e12.mergedAttrs, e12.attrs);
    let u = e12.tView = zs(2, e12, o, i, s, n.directiveRegistry, n.pipeRegistry, null, n.schemas, n.consts, null);
    n.queries !== null && (n.queries.template(n, e12), u.queries = n.queries.embeddedTView(e12));
  }
  a && (e12.flags |= a), xt(e12, false);
  let c = Mg(n, t, e12, r);
  yr() && Ys(n, t, c, e12), Pt(c, t);
  let l = Nu(c, t, c, e12);
  t[r + B] = l, Gs(t, l), sg(l, e12, t);
}
function jr(e12, t, n, r, o, i, s, a, c, l, u) {
  let d = n + B, f;
  if (t.firstCreatePass) {
    if (f = eo(t, d, 4, s || null, a || null), l != null) {
      let p = he(t.consts, l);
      f.localNames = [];
      for (let h = 0; h < p.length; h += 2)
        f.localNames.push(p[h], -1);
    }
  } else
    f = t.data[d];
  return Tg(f, e12, t, n, r, o, i, c), l != null && Eu(e12, f, u), f;
}
var Mg = _g;
function _g(e12, t, n, r) {
  return vr(true), t[O].createComment("");
}
var ra = new D("");
function oa(e12) {
  return !!e12 && typeof e12.then == "function";
}
function $u(e12) {
  return !!e12 && typeof e12.subscribe == "function";
}
var Uu = new D("");
var ia = (() => {
  class e12 {
    resolve;
    reject;
    initialized = false;
    done = false;
    donePromise = new Promise((n, r) => {
      this.resolve = n, this.reject = r;
    });
    appInits = E(Uu, { optional: true }) ?? [];
    injector = E(ue);
    constructor() {
    }
    runInitializers() {
      if (this.initialized)
        return;
      let n = [];
      for (let o of this.appInits) {
        let i = ar(this.injector, o);
        if (oa(i))
          n.push(i);
        else if ($u(i)) {
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
var zu = new D("");
function Wu() {
  Ao(() => {
    let e12 = "";
    throw new v(600, e12);
  });
}
function Gu(e12) {
  return e12.isBoundToModule;
}
var Sg = 10;
var Dn = (() => {
  class e12 {
    _runningTick = false;
    _destroyed = false;
    _destroyListeners = [];
    _views = [];
    internalErrorHandler = E(st);
    afterRenderManager = E(pu);
    zonelessEnabled = E(on);
    rootEffectScheduler = E(Ir);
    dirtyFlags = 0;
    tracingSnapshot = null;
    allTestViews = /* @__PURE__ */ new Set();
    autoDetectTestViews = /* @__PURE__ */ new Set();
    includeAllTestViews = false;
    afterTick = new ve();
    get allViews() {
      return [...(this.includeAllTestViews ? this.allTestViews : this.autoDetectTestViews).keys(), ...this._views];
    }
    get destroyed() {
      return this._destroyed;
    }
    componentTypes = [];
    components = [];
    internalPendingTask = E(At);
    get isStable() {
      return this.internalPendingTask.hasPendingTasksObservable.pipe(zo((n) => !n));
    }
    constructor() {
      E(Ht, { optional: true });
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
    _injector = E(Y);
    _rendererFactory = null;
    get injector() {
      return this._injector;
    }
    bootstrap(n, r) {
      return this.bootstrapImpl(n, r);
    }
    bootstrapImpl(n, r, o = ue.NULL) {
      return this._injector.get(K).run(() => {
        T(C.BootstrapComponentStart);
        let s = n instanceof to;
        if (!this._injector.get(ia).done) {
          let h = "";
          throw new v(405, h);
        }
        let c;
        s ? c = n : c = this._injector.get(no).resolveComponentFactory(n), this.componentTypes.push(c.componentType);
        let l = Gu(c) ? void 0 : this._injector.get(Fr), u = r || c.selector, d = c.create(o, [], u, l), f = d.location.nativeElement, p = d.injector.get(ra, null);
        return p?.registerApplication(f), d.onDestroy(() => {
          this.detachView(d.hostView), cn(this.components, d), p?.unregisterApplication(f);
        }), this._loadComponent(d), T(C.BootstrapComponentEnd, d), d;
      });
    }
    tick() {
      this.zonelessEnabled || (this.dirtyFlags |= 1), this._tick();
    }
    _tick() {
      T(C.ChangeDetectionStart), this.tracingSnapshot !== null ? this.tracingSnapshot.run(Zs.CHANGE_DETECTION, this.tickImpl) : this.tickImpl();
    }
    tickImpl = () => {
      if (this._runningTick)
        throw T(C.ChangeDetectionEnd), new v(101, false);
      let n = g(null);
      try {
        this._runningTick = true, this.synchronize();
      } finally {
        this._runningTick = false, this.tracingSnapshot?.dispose(), this.tracingSnapshot = null, g(n), this.afterTick.next(), T(C.ChangeDetectionEnd);
      }
    };
    synchronize() {
      this._rendererFactory === null && !this._injector.destroyed && (this._rendererFactory = this._injector.get(lt, null, { optional: true }));
      let n = 0;
      for (; this.dirtyFlags !== 0 && n++ < Sg; ) {
        T(C.ChangeDetectionSyncStart);
        try {
          this.synchronizeOnce();
        } finally {
          T(C.ChangeDetectionSyncEnd);
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
          if (!r && !nn(o))
            continue;
          let i = r && !this.zonelessEnabled ? 0 : 1;
          Tu(o, i), n = true;
        }
        if (this.dirtyFlags &= -5, this.syncDirtyFlagsWithViews(), this.dirtyFlags & 23)
          return;
      }
      n || (this._rendererFactory?.begin?.(), this._rendererFactory?.end?.()), this.dirtyFlags & 8 && (this.dirtyFlags &= -9, this.afterRenderManager.execute()), this.syncDirtyFlagsWithViews();
    }
    syncDirtyFlagsWithViews() {
      if (this.allViews.some(({ _lView: n }) => nn(n))) {
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
      cn(this._views, r), r.detachFromAppRef();
    }
    _loadComponent(n) {
      this.attachView(n.hostView);
      try {
        this.tick();
      } catch (o) {
        this.internalErrorHandler(o);
      }
      this.components.push(n), this._injector.get(zu, []).forEach((o) => o(n));
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
      return this._destroyListeners.push(n), () => cn(this._destroyListeners, n);
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
function cn(e12, t) {
  let n = e12.indexOf(t);
  n > -1 && e12.splice(n, 1);
}
var Ts = class {
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
function qi(e12, t, n, r, o) {
  return e12 === n && Object.is(t, r) ? 1 : Object.is(o(e12, t), o(n, r)) ? -1 : 0;
}
function Ng(e12, t, n, r) {
  let o, i, s = 0, a = e12.length - 1, c = void 0;
  if (Array.isArray(t)) {
    g(r);
    let l = t.length - 1;
    for (g(null); s <= a && s <= l; ) {
      let u = e12.at(s), d = t[s], f = qi(s, u, s, d, n);
      if (f !== 0) {
        f < 0 && e12.updateValue(s, d), s++;
        continue;
      }
      let p = e12.at(a), h = t[l], L = qi(a, p, l, h, n);
      if (L !== 0) {
        L < 0 && e12.updateValue(a, h), a--, l--;
        continue;
      }
      let H = n(s, u), dt = n(a, p), $t = n(s, d);
      if (Object.is($t, dt)) {
        let Io = n(l, h);
        Object.is(Io, H) ? (e12.swap(s, a), e12.updateValue(a, h), l--, a--) : e12.move(a, s), e12.updateValue(s, d), s++;
        continue;
      }
      if (o ??= new Hr(), i ??= wl(e12, s, a, n), Ms(e12, o, s, $t))
        e12.updateValue(s, d), s++, a++;
      else if (i.has($t))
        o.set(H, e12.detach(s)), a--;
      else {
        let Io = e12.create(s, t[s]);
        e12.attach(s, Io), s++, a++;
      }
    }
    for (; s <= l; )
      Cl(e12, o, n, s, t[s]), s++;
  } else if (t != null) {
    g(r);
    let l = t[Symbol.iterator]();
    g(null);
    let u = l.next();
    for (; !u.done && s <= a; ) {
      let d = e12.at(s), f = u.value, p = qi(s, d, s, f, n);
      if (p !== 0)
        p < 0 && e12.updateValue(s, f), s++, u = l.next();
      else {
        o ??= new Hr(), i ??= wl(e12, s, a, n);
        let h = n(s, f);
        if (Ms(e12, o, s, h))
          e12.updateValue(s, f), s++, a++, u = l.next();
        else if (!i.has(h))
          e12.attach(s, e12.create(s, f)), s++, a++, u = l.next();
        else {
          let L = n(s, d);
          o.set(L, e12.detach(s)), a--;
        }
      }
    }
    for (; !u.done; )
      Cl(e12, o, n, e12.length, u.value), u = l.next();
  }
  for (; s <= a; )
    e12.destroy(e12.detach(a--));
  o?.forEach((l) => {
    e12.destroy(l);
  });
}
function Ms(e12, t, n, r) {
  return t !== void 0 && t.has(r) ? (e12.attach(n, t.get(r)), t.delete(r), true) : false;
}
function Cl(e12, t, n, r, o) {
  if (Ms(e12, t, r, n(r, o)))
    e12.updateValue(r, o);
  else {
    let i = e12.create(r, o);
    e12.attach(r, i);
  }
}
function wl(e12, t, n, r) {
  let o = /* @__PURE__ */ new Set();
  for (let i = t; i <= n; i++)
    o.add(r(i, e12.at(i)));
  return o;
}
var Hr = class {
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
function bn(e12, t, n, r, o, i, s, a) {
  Vt("NgControlFlow");
  let c = M(), l = ie(), u = he(l.consts, i);
  return jr(c, l, e12, t, n, r, o, u, 256, s, a), sa;
}
function sa(e12, t, n, r, o, i, s, a) {
  Vt("NgControlFlow");
  let c = M(), l = ie(), u = he(l.consts, i);
  return jr(c, l, e12, t, n, r, o, u, 512, s, a), sa;
}
function Cn(e12, t) {
  Vt("NgControlFlow");
  let n = M(), r = rn(), o = n[r] !== Re ? n[r] : -1, i = o !== -1 ? Vr(n, B + o) : void 0, s = 0;
  if (In(n, r, e12)) {
    let a = g(null);
    try {
      if (i !== void 0 && Ru(i, s), e12 !== -1) {
        let c = B + e12, l = Vr(n, c), u = xs(n[m], c), d = Ou(l, u, n), f = Jr(n, u, t, { dehydratedView: d });
        Xr(l, f, s, un(u, d));
      }
    } finally {
      g(a);
    }
  } else if (i !== void 0) {
    let a = xu(i, s);
    a !== void 0 && (a[x] = t);
  }
}
var _s = class {
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
function oo(e12, t) {
  return t;
}
var Ss = class {
  hasEmptyBlock;
  trackByFn;
  liveCollection;
  constructor(t, n, r) {
    this.hasEmptyBlock = t, this.trackByFn = n, this.liveCollection = r;
  }
};
function io(e12, t, n, r, o, i, s, a, c, l, u, d, f) {
  Vt("NgControlFlow");
  let p = M(), h = ie(), L = c !== void 0, H = M(), dt = a ? s.bind(H[ee][x]) : s, $t = new Ss(L, dt);
  H[B + e12] = $t, jr(p, h, e12 + 1, t, n, r, o, he(h.consts, i), 256), L && jr(p, h, e12 + 2, c, l, u, d, he(h.consts, f), 512);
}
var Ns = class extends Ts {
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
    let r = n[Ct];
    this.needsIndexUpdate ||= t !== this.length, Xr(this.lContainer, n, t, un(this.templateTNode, r)), xg(this.lContainer, t);
  }
  detach(t) {
    return this.needsIndexUpdate ||= t !== this.length - 1, Rg(this.lContainer, t), Ag(this.lContainer, t);
  }
  create(t, n) {
    let r = ps(this.lContainer, this.templateTNode.tView.ssrId);
    return Jr(this.hostLView, this.templateTNode, new _s(this.lContainer, n, t), { dehydratedView: r });
  }
  destroy(t) {
    Yr(t[m], t);
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
    return Og(this.lContainer, t);
  }
};
function so(e12) {
  let t = g(null), n = $e();
  try {
    let r = M(), o = r[m], i = r[n], s = n + 1, a = Vr(r, s);
    if (i.liveCollection === void 0) {
      let l = xs(o, s);
      i.liveCollection = new Ns(a, r, l);
    } else
      i.liveCollection.reset();
    let c = i.liveCollection;
    if (Ng(c, e12, i.trackByFn, t), c.updateIndexes(), i.hasEmptyBlock) {
      let l = rn(), u = c.length === 0;
      if (In(r, l, u)) {
        let d = n + 2, f = Vr(r, d);
        if (u) {
          let p = xs(o, d), h = Ou(f, p, r), L = Jr(r, p, void 0, { dehydratedView: h });
          Xr(f, L, 0, un(p, h));
        } else
          o.firstUpdatePass && Th(f), Ru(f, 0);
      }
    }
  } finally {
    g(t);
  }
}
function Vr(e12, t) {
  return e12[t];
}
function xg(e12, t) {
  if (e12.length <= S)
    return;
  let n = S + t, r = e12[n], o = r ? r[He] : void 0;
  if (r && o && o.detachedLeaveAnimationFns && o.detachedLeaveAnimationFns.length > 0) {
    let i = r[be];
    xp(i, o), ct.delete(r[Ce]), o.detachedLeaveAnimationFns = void 0;
  }
}
function Rg(e12, t) {
  if (e12.length <= S)
    return;
  let n = S + t, r = e12[n], o = r ? r[He] : void 0;
  o && o.leave && o.leave.size > 0 && (o.detachedLeaveAnimationFns = []);
}
function Ag(e12, t) {
  return fn(e12, t);
}
function Og(e12, t) {
  return xu(e12, t);
}
function xs(e12, t) {
  return ur(e12, t);
}
function k(e12, t, n, r) {
  let o = M(), i = o[m], s = e12 + B, a = i.firstCreatePass ? Bh(s, i, 2, t, n, r) : i.data[s];
  return th(a, o, e12, t, kg), r != null && Eu(o, a), k;
}
function P() {
  let e12 = ge(), t = nh(e12);
  return Tc(t) && Mc(), Cc(), P;
}
function ao(e12, t, n, r) {
  return k(e12, t, n, r), P(), ao;
}
var kg = (e12, t, n, r, o) => (vr(true), su(t[O], r, Vc()));
function co() {
  return M();
}
function ae(e12, t, n) {
  let r = M(), o = rn();
  if (In(r, o, t)) {
    let i = ie(), s = Hc();
    Yp(s, r, e12, t, r[O], n);
  }
  return ae;
}
var wn = "en-US";
var Pg = wn;
function qu(e12) {
  typeof e12 == "string" && (Pg = e12.toLowerCase().replace(/_/g, "-"));
}
function Ae(e12, t, n) {
  let r = M(), o = ie(), i = ge();
  return (i.type & 3 || n) && Uh(i, o, r, n, r[O], e12, t, $h(i, r, t)), Ae;
}
function ce(e12 = 1) {
  return jc(e12);
}
function lo(e12, t, n) {
  return hg(e12, t, n), lo;
}
function aa(e12) {
  let t = M(), n = ie(), r = ki();
  hr(r + 1);
  let o = ta(n, r);
  if (e12.dirty && mc(t) === ((o.metadata.flags & 2) === 2)) {
    if (o.matches === null)
      e12.reset([]);
    else {
      let i = yg(t, r);
      e12.reset(i, Hf), e12.notifyOnChanges();
    }
    return true;
  }
  return false;
}
function ca() {
  return fg(M(), ki());
}
function wr(e12, t) {
  return e12 << 17 | t << 2;
}
function ut(e12) {
  return e12 >> 17 & 32767;
}
function Lg(e12) {
  return (e12 & 2) == 2;
}
function Fg(e12, t) {
  return e12 & 131071 | t << 17;
}
function Rs(e12) {
  return e12 | 2;
}
function Ft(e12) {
  return (e12 & 131068) >> 2;
}
function Zi(e12, t) {
  return e12 & -131069 | t << 2;
}
function jg(e12) {
  return (e12 & 1) === 1;
}
function As(e12) {
  return e12 | 1;
}
function Hg(e12, t, n, r, o, i) {
  let s = i ? t.classBindings : t.styleBindings, a = ut(s), c = Ft(s);
  e12[r] = n;
  let l = false, u;
  if (Array.isArray(n)) {
    let d = n;
    u = d[1], (u === null || bt(d, u) > 0) && (l = true);
  } else
    u = n;
  if (o)
    if (c !== 0) {
      let f = ut(e12[a + 1]);
      e12[r + 1] = wr(f, a), f !== 0 && (e12[f + 1] = Zi(e12[f + 1], r)), e12[a + 1] = Fg(e12[a + 1], r);
    } else
      e12[r + 1] = wr(a, 0), a !== 0 && (e12[a + 1] = Zi(e12[a + 1], r)), a = r;
  else
    e12[r + 1] = wr(c, 0), a === 0 ? a = r : e12[c + 1] = Zi(e12[c + 1], r), c = r;
  l && (e12[r + 1] = Rs(e12[r + 1])), Tl(e12, u, r, true), Tl(e12, u, r, false), Vg(t, u, e12, r, i), s = wr(a, c), i ? t.classBindings = s : t.styleBindings = s;
}
function Vg(e12, t, n, r, o) {
  let i = o ? e12.residualClasses : e12.residualStyles;
  i != null && typeof t == "string" && bt(i, t) >= 0 && (n[r + 1] = As(n[r + 1]));
}
function Tl(e12, t, n, r) {
  let o = e12[n + 1], i = t === null, s = r ? ut(o) : Ft(o), a = false;
  for (; s !== 0 && (a === false || i); ) {
    let c = e12[s], l = e12[s + 1];
    Bg(c, t) && (a = true, e12[s + 1] = r ? As(l) : Rs(l)), s = r ? ut(l) : Ft(l);
  }
  a && (e12[n + 1] = r ? Rs(o) : As(o));
}
function Bg(e12, t) {
  return e12 === null || t == null || (Array.isArray(e12) ? e12[1] : e12) === t ? true : Array.isArray(e12) && typeof t == "string" ? bt(e12, t) >= 0 : false;
}
function uo(e12, t) {
  return $g(e12, t, null, true), uo;
}
function $g(e12, t, n, r) {
  let o = M(), i = ie(), s = xc(2);
  if (i.firstUpdatePass && zg(i, e12, s, r), t !== Re && In(o, s, t)) {
    let a = i.data[$e()];
    Qg(i, a, o, o[O], e12, o[s + 1] = Yg(t, n), r, s);
  }
}
function Ug(e12, t) {
  return t >= e12.expandoStartIndex;
}
function zg(e12, t, n, r) {
  let o = e12.data;
  if (o[n + 1] === null) {
    let i = o[$e()], s = Ug(e12, n);
    Kg(i, r) && t === null && !s && (t = false), t = Wg(o, i, t, r), Hg(o, i, t, n, s, r);
  }
}
function Wg(e12, t, n, r) {
  let o = kc(e12), i = r ? t.residualClasses : t.residualStyles;
  if (o === null)
    (r ? t.classBindings : t.styleBindings) === 0 && (n = Qi(null, e12, t, n, r), n = mn(n, t.attrs, r), i = null);
  else {
    let s = t.directiveStylingLast;
    if (s === -1 || e12[s] !== o)
      if (n = Qi(o, e12, t, n, r), i === null) {
        let c = Gg(e12, t, r);
        c !== void 0 && Array.isArray(c) && (c = Qi(null, e12, t, c[1], r), c = mn(c, t.attrs, r), qg(e12, t, r, c));
      } else
        i = Zg(e12, t, r);
  }
  return i !== void 0 && (r ? t.residualClasses = i : t.residualStyles = i), n;
}
function Gg(e12, t, n) {
  let r = n ? t.classBindings : t.styleBindings;
  if (Ft(r) !== 0)
    return e12[ut(r)];
}
function qg(e12, t, n, r) {
  let o = n ? t.classBindings : t.styleBindings;
  e12[ut(o)] = r;
}
function Zg(e12, t, n) {
  let r, o = t.directiveEnd;
  for (let i = 1 + t.directiveStylingLast; i < o; i++) {
    let s = e12[i].hostAttrs;
    r = mn(r, s, n);
  }
  return mn(r, t.attrs, n);
}
function Qi(e12, t, n, r, o) {
  let i = null, s = n.directiveEnd, a = n.directiveStylingLast;
  for (a === -1 ? a = n.directiveStart : a++; a < s && (i = t[a], r = mn(r, i.hostAttrs, o), i !== e12); )
    a++;
  return e12 !== null && (n.directiveStylingLast = a), r;
}
function mn(e12, t, n) {
  let r = n ? 1 : 2, o = -1;
  if (t !== null)
    for (let i = 0; i < t.length; i++) {
      let s = t[i];
      typeof s == "number" ? o = s : o === r && (Array.isArray(e12) || (e12 = e12 === void 0 ? [] : ["", e12]), sc(e12, s, n ? true : t[++i]));
    }
  return e12 === void 0 ? null : e12;
}
function Qg(e12, t, n, r, o, i, s, a) {
  if (!(t.type & 3))
    return;
  let c = e12.data, l = c[a + 1], u = jg(l) ? Ml(c, t, n, o, Ft(l), s) : void 0;
  if (!Br(u)) {
    Br(i) || Lg(l) && (i = Ml(c, null, n, o, a, s));
    let d = Ti($e(), n);
    Wp(r, s, d, o, i);
  }
}
function Ml(e12, t, n, r, o, i) {
  let s = t === null, a;
  for (; o > 0; ) {
    let c = e12[o], l = Array.isArray(c), u = l ? c[1] : c, d = u === null, f = n[o + 1];
    f === Re && (f = d ? ke : void 0);
    let p = d ? sr(f, r) : u === r ? f : void 0;
    if (l && !Br(p) && (p = sr(c, r)), Br(p) && (a = p, s))
      return a;
    let h = e12[o + 1];
    o = s ? ut(h) : Ft(h);
  }
  if (t !== null) {
    let c = i ? t.residualClasses : t.residualStyles;
    c != null && (a = sr(c, r));
  }
  return a;
}
function Br(e12) {
  return e12 !== void 0;
}
function Yg(e12, t) {
  return e12 == null || e12 === "" || (typeof t == "string" ? e12 = e12 + t : typeof e12 == "object" && (e12 = er(Ne(e12)))), e12;
}
function Kg(e12, t) {
  return (e12.flags & (t ? 8 : 16)) !== 0;
}
function W(e12, t = "") {
  let n = M(), r = ie(), o = e12 + B, i = r.firstCreatePass ? eo(r, o, 1, t, null) : r.data[o], s = Jg(r, n, i, t);
  n[o] = s, yr() && Ys(r, n, s, i), xt(i, false);
}
var Jg = (e12, t, n, r) => (vr(true), hp(t[O], r));
function Xg(e12, t, n, r = "") {
  return In(e12, rn(), n) ? t + fi(n) + r : Re;
}
function Oe(e12) {
  return la("", e12), Oe;
}
function la(e12, t, n) {
  let r = M(), o = Xg(r, e12, t, n);
  return o !== Re && em(r, $e(), o), la;
}
function em(e12, t, n) {
  let r = Ti(t, e12);
  gp(e12[O], r, n);
}
var Zu = (() => {
  class e12 {
    applicationErrorHandler = E(st);
    appRef = E(Dn);
    taskService = E(At);
    ngZone = E(K);
    zonelessEnabled = E(on);
    tracing = E(Ht, { optional: true });
    zoneIsDefined = typeof Zone < "u" && !!Zone.root.run;
    schedulerTickApplyArgs = [{ data: { __scheduler_tick__: true } }];
    subscriptions = new $();
    angularZoneId = this.zoneIsDefined ? this.ngZone._inner?.get(Qt) : null;
    scheduleInRootZone = !this.zonelessEnabled && this.zoneIsDefined && (E(Bi, { optional: true }) ?? false);
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
      let r = this.useMicrotaskScheduler ? Wc : Fi;
      this.pendingRenderTaskId = this.taskService.add(), this.scheduleInRootZone ? this.cancelScheduledCallback = Zone.root.run(() => r(() => this.tick())) : this.cancelScheduledCallback = this.ngZone.runOutsideAngular(() => r(() => this.tick()));
    }
    shouldScheduleTick() {
      return !(this.appRef.destroyed || this.pendingRenderTaskId !== null || this.runningTick || this.appRef._runningTick || !this.zonelessEnabled && this.zoneIsDefined && Zone.current.get(Qt + this.angularZoneId));
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
function Qu() {
  return [{ provide: Ke, useExisting: Zu }, { provide: K, useClass: Yt }, { provide: on, useValue: true }];
}
function tm() {
  return typeof $localize < "u" && $localize.locale || wn;
}
var ua = new D("", { factory: () => E(ua, { optional: true, skipSelf: true }) || tm() });
function We(e12, t) {
  return jn(e12, t?.equal);
}
var da = new D("");
var dm = new D("");
function Tn(e12) {
  return !e12.moduleRef;
}
function fm(e12) {
  let t = Tn(e12) ? e12.r3Injector : e12.moduleRef.injector, n = t.get(K);
  return n.run(() => {
    Tn(e12) ? e12.r3Injector.resolveInjectorInitializers() : e12.moduleRef.resolveInjectorInitializers();
    let r = t.get(st), o;
    if (n.runOutsideAngular(() => {
      o = n.onError.subscribe({ next: r });
    }), Tn(e12)) {
      let i = () => t.destroy(), s = e12.platformInjector.get(da);
      s.add(i), t.onDestroy(() => {
        o.unsubscribe(), s.delete(i);
      });
    } else {
      let i = () => e12.moduleRef.destroy(), s = e12.platformInjector.get(da);
      s.add(i), e12.moduleRef.onDestroy(() => {
        cn(e12.allPlatformModules, e12.moduleRef), o.unsubscribe(), s.delete(i);
      });
    }
    return hm(r, n, () => {
      let i = t.get(At), s = i.add(), a = t.get(ia);
      return a.runInitializers(), a.donePromise.then(() => {
        let c = t.get(ua, wn);
        if (qu(c || wn), !t.get(dm, true))
          return Tn(e12) ? t.get(Dn) : (e12.allPlatformModules.push(e12.moduleRef), e12.moduleRef);
        if (Tn(e12)) {
          let u = t.get(Dn);
          return e12.rootComponent !== void 0 && u.bootstrap(e12.rootComponent), u;
        } else
          return pm?.(e12.moduleRef, e12.allPlatformModules), e12.moduleRef;
      }).finally(() => {
        i.remove(s);
      });
    });
  });
}
var pm;
function hm(e12, t, n) {
  try {
    let r = n();
    return oa(r) ? r.catch((o) => {
      throw t.runOutsideAngular(() => e12(o)), o;
    }) : r;
  } catch (r) {
    throw t.runOutsideAngular(() => e12(r)), r;
  }
}
var fo = null;
function gm(e12 = [], t) {
  return ue.create({ name: t, providers: [{ provide: Xt, useValue: "platform" }, { provide: da, useValue: /* @__PURE__ */ new Set([() => fo = null]) }, ...e12] });
}
function mm(e12 = []) {
  if (fo)
    return fo;
  let t = gm(e12);
  return fo = t, Wu(), ym(t), t;
}
function ym(e12) {
  let t = e12.get(zr, null);
  ar(e12, () => {
    t?.forEach((n) => n());
  });
}
var vm = 1e4;
var zM = vm - 1e3;
function Ku(e12) {
  let { rootComponent: t, appProviders: n, platformProviders: r, platformRef: o } = e12;
  T(C.BootstrapApplicationStart);
  try {
    let i = o?.injector ?? mm(r), s = [Qu(), qc, ...n || []], a = new gn({ providers: s, parent: i, debugName: "", runEnvironmentInitializers: false });
    return fm({ r3Injector: a.injector, platformInjector: i, rootComponent: t });
  } catch (i) {
    return Promise.reject(i);
  } finally {
    T(C.BootstrapApplicationEnd);
  }
}
var Ju = null;
function Bt() {
  return Ju;
}
function fa(e12) {
  Ju ??= e12;
}
var _n = class {
};
function pa(e12, t) {
  t = encodeURIComponent(t);
  for (let n of e12.split(";")) {
    let r = n.indexOf("="), [o, i] = r == -1 ? [n, ""] : [n.slice(0, r), n.slice(r + 1)];
    if (o.trim() === t)
      return decodeURIComponent(i);
  }
  return null;
}
var Sn = class {
};
var Xu = "browser";
var Nn = class {
  _doc;
  constructor(t) {
    this._doc = t;
  }
  manager;
};
var po = (() => {
  class e12 extends Nn {
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
      return new (r || e12)(b(z));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var mo = new D("");
var ya = (() => {
  class e12 {
    _zone;
    _plugins;
    _eventNameToPlugin = /* @__PURE__ */ new Map();
    constructor(n, r) {
      this._zone = r, n.forEach((s) => {
        s.manager = this;
      });
      let o = n.filter((s) => !(s instanceof po));
      this._plugins = o.slice().reverse();
      let i = n.find((s) => s instanceof po);
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
      return new (r || e12)(b(mo), b(K));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var ha = "ng-app-id";
function ed(e12) {
  for (let t of e12)
    t.remove();
}
function td(e12, t) {
  let n = t.createElement("style");
  return n.textContent = e12, n;
}
function Em(e12, t, n, r) {
  let o = e12.head?.querySelectorAll(`style[${ha}="${t}"],link[${ha}="${t}"]`);
  if (o)
    for (let i of o)
      i.removeAttribute(ha), i instanceof HTMLLinkElement ? r.set(i.href.slice(i.href.lastIndexOf("/") + 1), { usage: 0, elements: [i] }) : i.textContent && n.set(i.textContent, { usage: 0, elements: [i] });
}
function ma(e12, t) {
  let n = t.createElement("link");
  return n.setAttribute("rel", "stylesheet"), n.setAttribute("href", e12), n;
}
var va = (() => {
  class e12 {
    doc;
    appId;
    nonce;
    inline = /* @__PURE__ */ new Map();
    external = /* @__PURE__ */ new Map();
    hosts = /* @__PURE__ */ new Set();
    constructor(n, r, o, i = {}) {
      this.doc = n, this.appId = r, this.nonce = o, Em(n, r, this.inline, this.external), this.hosts.add(n.head);
    }
    addStyles(n, r) {
      for (let o of n)
        this.addUsage(o, this.inline, td);
      r?.forEach((o) => this.addUsage(o, this.external, ma));
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
      o && (o.usage--, o.usage <= 0 && (ed(o.elements), r.delete(n)));
    }
    ngOnDestroy() {
      for (let [, { elements: n }] of [...this.inline, ...this.external])
        ed(n);
      this.hosts.clear();
    }
    addHost(n) {
      this.hosts.add(n);
      for (let [r, { elements: o }] of this.inline)
        o.push(this.addElement(n, td(r, this.doc)));
      for (let [r, { elements: o }] of this.external)
        o.push(this.addElement(n, ma(r, this.doc)));
    }
    removeHost(n) {
      this.hosts.delete(n);
    }
    addElement(n, r) {
      return this.nonce && r.setAttribute("nonce", this.nonce), n.appendChild(r);
    }
    static \u0275fac = function(r) {
      return new (r || e12)(b(z), b(Ur), b(Wr, 8), b(vn));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var ga = { svg: "http://www.w3.org/2000/svg", xhtml: "http://www.w3.org/1999/xhtml", xlink: "http://www.w3.org/1999/xlink", xml: "http://www.w3.org/XML/1998/namespace", xmlns: "http://www.w3.org/2000/xmlns/", math: "http://www.w3.org/1998/Math/MathML" };
var Ea = /%COMP%/g;
var rd = "%COMP%";
var Im = `_nghost-${rd}`;
var Dm = `_ngcontent-${rd}`;
var bm = true;
var Cm = new D("", { factory: () => bm });
function wm(e12) {
  return Dm.replace(Ea, e12);
}
function Tm(e12) {
  return Im.replace(Ea, e12);
}
function od(e12, t) {
  return t.map((n) => n.replace(Ea, e12));
}
var Ia = (() => {
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
      this.eventManager = n, this.sharedStylesHost = r, this.appId = o, this.removeStylesOnCompDestroy = i, this.doc = s, this.ngZone = a, this.nonce = c, this.tracingService = l, this.defaultRenderer = new xn(n, s, a, this.tracingService);
    }
    createRenderer(n, r) {
      if (!n || !r)
        return this.defaultRenderer;
      let o = this.getOrCreateRenderer(n, r);
      return o instanceof go ? o.applyToHost(n) : o instanceof Rn && o.applyStyles(), o;
    }
    getOrCreateRenderer(n, r) {
      let o = this.rendererByCompId, i = o.get(r.id);
      if (!i) {
        let s = this.doc, a = this.ngZone, c = this.eventManager, l = this.sharedStylesHost, u = this.removeStylesOnCompDestroy, d = this.tracingService;
        switch (r.encapsulation) {
          case se.Emulated:
            i = new go(c, l, r, this.appId, u, s, a, d);
            break;
          case se.ShadowDom:
            return new ho(c, n, r, s, a, this.nonce, d, l);
          case se.ExperimentalIsolatedShadowDom:
            return new ho(c, n, r, s, a, this.nonce, d);
          default:
            i = new Rn(c, l, r, u, s, a, d);
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
      return new (r || e12)(b(ya), b(va), b(Ur), b(Cm), b(z), b(K), b(Wr), b(Ht, 8));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var xn = class {
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
    return n ? this.doc.createElementNS(ga[n] || n, t) : this.doc.createElement(t);
  }
  createComment(t) {
    return this.doc.createComment(t);
  }
  createText(t) {
    return this.doc.createTextNode(t);
  }
  appendChild(t, n) {
    (nd(t) ? t.content : t).appendChild(n);
  }
  insertBefore(t, n, r) {
    t && (nd(t) ? t.content : t).insertBefore(n, r);
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
      let i = ga[o];
      i ? t.setAttributeNS(i, n, r) : t.setAttribute(n, r);
    } else
      t.setAttribute(n, r);
  }
  removeAttribute(t, n, r) {
    if (r) {
      let o = ga[r];
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
    o & (Se.DashCase | Se.Important) ? t.style.setProperty(n, r, o & Se.Important ? "important" : "") : t.style[n] = r;
  }
  removeStyle(t, n, r) {
    r & Se.DashCase ? t.style.removeProperty(n) : t.style[n] = "";
  }
  setProperty(t, n, r) {
    t != null && (t[n] = r);
  }
  setValue(t, n) {
    t.nodeValue = n;
  }
  listen(t, n, r, o) {
    if (typeof t == "string" && (t = Bt().getGlobalEventTarget(this.doc, t), !t))
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
function nd(e12) {
  return e12.tagName === "TEMPLATE" && e12.content !== void 0;
}
var ho = class extends xn {
  hostEl;
  sharedStylesHost;
  shadowRoot;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, o, i, a), this.hostEl = n, this.sharedStylesHost = c, this.shadowRoot = n.attachShadow({ mode: "open" }), this.sharedStylesHost && this.sharedStylesHost.addHost(this.shadowRoot);
    let l = r.styles;
    l = od(r.id, l);
    for (let d of l) {
      let f = document.createElement("style");
      s && f.setAttribute("nonce", s), f.textContent = d, this.shadowRoot.appendChild(f);
    }
    let u = r.getExternalStyles?.();
    if (u)
      for (let d of u) {
        let f = ma(d, o);
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
var Rn = class extends xn {
  sharedStylesHost;
  removeStylesOnCompDestroy;
  styles;
  styleUrls;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, i, s, a), this.sharedStylesHost = n, this.removeStylesOnCompDestroy = o;
    let l = r.styles;
    this.styles = c ? od(c, l) : l, this.styleUrls = r.getExternalStyles?.(c);
  }
  applyStyles() {
    this.sharedStylesHost.addStyles(this.styles, this.styleUrls);
  }
  destroy() {
    this.removeStylesOnCompDestroy && ct.size === 0 && this.sharedStylesHost.removeStyles(this.styles, this.styleUrls);
  }
};
var go = class extends Rn {
  contentAttr;
  hostAttr;
  constructor(t, n, r, o, i, s, a, c) {
    let l = o + "-" + r.id;
    super(t, n, r, i, s, a, c, l), this.contentAttr = wm(l), this.hostAttr = Tm(l);
  }
  applyToHost(t) {
    this.applyStyles(), this.setAttribute(t, this.hostAttr, "");
  }
  createElement(t, n) {
    let r = super.createElement(t, n);
    return super.setAttribute(r, this.contentAttr, ""), r;
  }
};
var yo = class e9 extends _n {
  supportsDOMEvents = true;
  static makeCurrent() {
    fa(new e9());
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
    let n = Mm();
    return n == null ? null : _m(n);
  }
  resetBaseElement() {
    An = null;
  }
  getUserAgent() {
    return window.navigator.userAgent;
  }
  getCookie(t) {
    return pa(document.cookie, t);
  }
};
var An = null;
function Mm() {
  return An = An || document.head.querySelector("base"), An ? An.getAttribute("href") : null;
}
function _m(e12) {
  return new URL(e12, document.baseURI).pathname;
}
var Sm = (() => {
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
var id = ["alt", "control", "meta", "shift"];
var Nm = { "\b": "Backspace", "	": "Tab", "\x7F": "Delete", "\x1B": "Escape", Del: "Delete", Esc: "Escape", Left: "ArrowLeft", Right: "ArrowRight", Up: "ArrowUp", Down: "ArrowDown", Menu: "ContextMenu", Scroll: "ScrollLock", Win: "OS" };
var xm = { alt: (e12) => e12.altKey, control: (e12) => e12.ctrlKey, meta: (e12) => e12.metaKey, shift: (e12) => e12.shiftKey };
var sd = (() => {
  class e12 extends Nn {
    constructor(n) {
      super(n);
    }
    supports(n) {
      return e12.parseEventName(n) != null;
    }
    addEventListener(n, r, o, i) {
      let s = e12.parseEventName(r), a = e12.eventCallback(s.fullKey, o, this.manager.getZone());
      return this.manager.getZone().runOutsideAngular(() => Bt().onAndCancel(n, s.domEventName, a, i));
    }
    static parseEventName(n) {
      let r = n.toLowerCase().split("."), o = r.shift();
      if (r.length === 0 || !(o === "keydown" || o === "keyup"))
        return null;
      let i = e12._normalizeKey(r.pop()), s = "", a = r.indexOf("code");
      if (a > -1 && (r.splice(a, 1), s = "code."), id.forEach((l) => {
        let u = r.indexOf(l);
        u > -1 && (r.splice(u, 1), s += l + ".");
      }), s += i, r.length != 0 || i.length === 0)
        return null;
      let c = {};
      return c.domEventName = o, c.fullKey = s, c;
    }
    static matchEventFullKeyCode(n, r) {
      let o = Nm[n.key] || n.key, i = "";
      return r.indexOf("code.") > -1 && (o = n.code, i = "code."), o == null || !o ? false : (o = o.toLowerCase(), o === " " ? o = "space" : o === "." && (o = "dot"), id.forEach((s) => {
        if (s !== o) {
          let a = xm[s];
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
      return new (r || e12)(b(z));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
async function Da(e12, t, n) {
  let r = N({ rootComponent: e12 }, Rm(t, n));
  return Ku(r);
}
function Rm(e12, t) {
  return { platformRef: t?.platformRef, appProviders: [...Lm, ...e12?.providers ?? []], platformProviders: Pm };
}
function Am() {
  yo.makeCurrent();
}
function Om() {
  return new De();
}
function km() {
  return Ls(document), document;
}
var Pm = [{ provide: vn, useValue: Xu }, { provide: zr, useValue: Am, multi: true }, { provide: z, useFactory: km }];
var Lm = [{ provide: Xt, useValue: "root" }, { provide: De, useFactory: Om }, { provide: mo, useClass: po, multi: true }, { provide: mo, useClass: sd, multi: true }, Ia, va, ya, { provide: lt, useExisting: Ia }, { provide: Sn, useClass: Sm }, []];
var ba = (() => {
  class e12 {
    static \u0275fac = function(r) {
      return new (r || e12)();
    };
    static \u0275prov = _({ token: e12, factory: function(r) {
      let o = null;
      return r ? o = new (r || e12)() : o = b(Fm), o;
    }, providedIn: "root" });
  }
  return e12;
})();
var Fm = (() => {
  class e12 extends ba {
    _doc;
    constructor(n) {
      super(), this._doc = n;
    }
    sanitize(n, r) {
      if (r == null)
        return null;
      switch (n) {
        case ye.NONE:
          return r;
        case ye.HTML:
          return ze(r, "HTML") ? Ne(r) : Zr(this._doc, String(r)).toString();
        case ye.STYLE:
          return ze(r, "Style") ? Ne(r) : r;
        case ye.SCRIPT:
          if (ze(r, "Script"))
            return Ne(r);
          throw new v(5200, false);
        case ye.URL:
          return ze(r, "URL") ? Ne(r) : qr(String(r));
        case ye.RESOURCE_URL:
          if (ze(r, "ResourceURL"))
            return Ne(r);
          throw new v(5201, false);
        default:
          throw new v(5202, false);
      }
    }
    bypassSecurityTrustHtml(n) {
      return js(n);
    }
    bypassSecurityTrustStyle(n) {
      return Hs(n);
    }
    bypassSecurityTrustScript(n) {
      return Vs(n);
    }
    bypassSecurityTrustUrl(n) {
      return Bs(n);
    }
    bypassSecurityTrustResourceUrl(n) {
      return $s(n);
    }
    static \u0275fac = function(r) {
      return new (r || e12)(b(z));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac, providedIn: "root" });
  }
  return e12;
})();
var vo = class e10 {
  constructor(t) {
    this.model = t;
    if (t) {
      this.page.set(t.get("page") ?? 0), this.pageSize.set(t.get("page_size") ?? 10), this.maxColumns.set(t.get("max_columns") ?? 0), this.rowCount.set(t.get("row_count") ?? null), this.tableHtml.set(t.get("table_html") ?? ""), this.sortContext.set(t.get("sort_context") ?? []), this.orderableColumns.set(t.get("orderable_columns") ?? []);
      let n = t.get("error_message") ?? t.get("_error_message") ?? null;
      this.errorMessage.set(n), this.startExecution.set(t.get("start_execution") ?? false), this.isDeferredMode.set(t.get("is_deferred_mode") ?? false), this.dryRunInfo.set(t.get("dry_run_info") ?? ""), t.on("change:page", () => {
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
      }), t.on("change:start_execution", () => {
        this.startExecution.set(t.get("start_execution") ?? false);
      }), t.on("change:is_deferred_mode", () => {
        this.isDeferredMode.set(t.get("is_deferred_mode") ?? false);
      }), t.on("change:dry_run_info", () => {
        this.dryRunInfo.set(t.get("dry_run_info") ?? "");
      });
      let r = () => {
        let o = t.get("error_message") ?? t.get("_error_message") ?? null;
        this.errorMessage.set(o);
      };
      t.on("change:error_message", r), t.on("change:_error_message", r);
    }
  }
  page = j(0);
  pageSize = j(10);
  maxColumns = j(0);
  rowCount = j(null);
  tableHtml = j("");
  sortContext = j([]);
  orderableColumns = j([]);
  errorMessage = j(null);
  startExecution = j(false);
  isDeferredMode = j(false);
  dryRunInfo = j("");
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
  setStartExecution(t) {
    this.startExecution.set(t), this.model && (this.model.set("start_execution", t), this.model.save_changes());
  }
  static \u0275fac = function(n) {
    return new (n || e10)(b("ANYWIDGET_MODEL"));
  };
  static \u0275prov = _({ token: e10, factory: e10.\u0275fac, providedIn: "root" });
};
var jm = ["tableContainer"];
function Hm(e12, t) {
  if (e12 & 1 && (k(0, "div", 2), W(1), P()), e12 & 2) {
    let n = ce();
    F(), Oe(n.errorMessage());
  }
}
function Vm(e12, t) {
  e12 & 1 && (ao(0, "span", 7), W(1, " Running... "));
}
function Bm(e12, t) {
  e12 & 1 && W(0, " Run Query ");
}
function $m(e12, t) {
  if (e12 & 1) {
    let n = co();
    k(0, "div", 3)(1, "div", 4)(2, "p", 5), W(3), P(), k(4, "button", 6), Ae("click", function() {
      Te(n);
      let o = ce();
      return Me(o.handleRunQuery());
    }), bn(5, Vm, 2, 0)(6, Bm, 1, 0), P()()();
  }
  if (e12 & 2) {
    let n = ce();
    F(3), Oe(n.dryRunInfo()), F(), ae("disabled", n.isLoading()), F(), Cn(n.isLoading() ? 5 : 6);
  }
}
function Um(e12, t) {
  if (e12 & 1 && (k(0, "option", 18), W(1), P()), e12 & 2) {
    let n = t.$implicit;
    ae("value", n), F(), Oe(n === 0 ? "All" : n);
  }
}
function zm(e12, t) {
  if (e12 & 1 && (k(0, "option", 18), W(1), P()), e12 & 2) {
    let n = t.$implicit;
    ae("value", n), F(), Oe(n);
  }
}
function Wm(e12, t) {
  if (e12 & 1) {
    let n = co();
    k(0, "div", 8, 0), Ae("click", function(o) {
      Te(n);
      let i = ce();
      return Me(i.handleTableClick(o));
    }), P(), k(2, "footer", 9)(3, "span", 10), W(4), P(), k(5, "div", 11)(6, "button", 12), Ae("click", function() {
      Te(n);
      let o = ce();
      return Me(o.handlePageChange(-1));
    }), W(7, "<"), P(), k(8, "span", 13), W(9), P(), k(10, "button", 12), Ae("click", function() {
      Te(n);
      let o = ce();
      return Me(o.handlePageChange(1));
    }), W(11, ">"), P()(), k(12, "div", 14)(13, "div", 15)(14, "label", 16), W(15, "Max columns:"), P(), k(16, "select", 17), Ae("change", function(o) {
      Te(n);
      let i = ce();
      return Me(i.handleMaxColumnsChange(o));
    }), io(17, Um, 2, 2, "option", 18, oo), P()(), k(19, "div", 19)(20, "label", 20), W(21, "Page size:"), P(), k(22, "select", 21), Ae("change", function(o) {
      Te(n);
      let i = ce();
      return Me(i.handlePageSizeChange(o));
    }), io(23, zm, 2, 2, "option", 18, oo), P()()()();
  }
  if (e12 & 2) {
    let n = ce();
    ae("innerHTML", n.sanitizedHtml(), Us), F(4), Oe(n.rowCountText()), F(2), ae("disabled", n.prevPageDisabled()), F(3), Oe(n.pageIndicatorText()), F(), ae("disabled", n.nextPageDisabled()), F(6), ae("value", n.maxColumns()), F(), so(n.maxColumnOptions), F(5), ae("value", n.pageSize()), F(), so(n.pageSizeOptions);
  }
}
var Eo = class e11 {
  state = E(vo);
  sanitizer = E(ba);
  maxColumnOptions = [5, 10, 15, 20, 0];
  pageSizeOptions = [10, 25, 50, 100];
  errorMessage = this.state.errorMessage;
  maxColumns = this.state.maxColumns;
  pageSize = this.state.pageSize;
  page = this.state.page;
  rowCount = this.state.rowCount;
  isDeferredMode = this.state.isDeferredMode;
  dryRunInfo = this.state.dryRunInfo;
  isLoading = j(false);
  sanitizedHtml = We(() => this.sanitizer.bypassSecurityTrustHtml(this.state.tableHtml()));
  totalPages = We(() => {
    let t = this.rowCount(), n = this.pageSize();
    return t !== null && n > 0 ? Math.ceil(t / n) : null;
  });
  pageIndicatorText = We(() => {
    let t = this.page(), n = this.rowCount(), r = this.totalPages(), o = (t + 1).toLocaleString(), i = (r ?? 1).toLocaleString();
    return `Page ${o} of ${i}`;
  });
  rowCountText = We(() => {
    let t = this.rowCount();
    return t === null ? "Total rows unknown" : t === 0 ? "0 total rows" : `${t.toLocaleString()} total rows`;
  });
  prevPageDisabled = We(() => this.page() === 0);
  nextPageDisabled = We(() => {
    let t = this.page(), n = this.rowCount(), r = this.totalPages();
    return n === null ? false : n === 0 ? true : r !== null && t >= r - 1;
  });
  isDarkMode = j(false);
  themeObserver = null;
  isHeightInitialized = false;
  tableContainerRef;
  constructor() {
    $i(() => {
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
  handleRunQuery() {
    this.isLoading.set(true), this.state.setStartExecution(true);
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
    t.shiftKey ? c !== -1 ? l[c].ascending ? l[c] = R(N({}, l[c]), { ascending: false }) : l.splice(c, 1) : l.push({ column: i, ascending: true }) : c !== -1 && l.length === 1 ? l[c].ascending ? l[c] = R(N({}, l[c]), { ascending: false }) : l = [] : l = [{ column: i, ascending: true }], this.state.setSortContext(l);
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
  static \u0275cmp = na({ type: e11, selectors: [["app-root"]], viewQuery: function(n, r) {
    if (n & 1 && lo(jm, 7), n & 2) {
      let o;
      aa(o = ca()) && (r.tableContainerRef = o.first);
    }
  }, decls: 4, vars: 4, consts: [["tableContainer", ""], [1, "bigframes-widget"], [1, "bigframes-error-message"], [1, "deferred-container"], [1, "deferred-card"], [1, "deferred-estimate"], [1, "run-query-button", 3, "click", "disabled"], [1, "spinner"], [1, "table-container", 3, "click", "innerHTML"], [1, "footer"], [1, "row-count"], [1, "pagination"], [3, "click", "disabled"], [1, "page-indicator"], [1, "settings"], [1, "max-columns"], ["for", "max-cols-select"], ["id", "max-cols-select", 3, "change", "value"], [3, "value"], [1, "page-size"], ["for", "page-size-select"], ["id", "page-size-select", 3, "change", "value"]], template: function(n, r) {
    n & 1 && (k(0, "div", 1), bn(1, Hm, 2, 1, "div", 2), bn(2, $m, 7, 3, "div", 3)(3, Wm, 25, 7), P()), n & 2 && (uo("bigframes-dark-mode", r.isDarkMode()), F(), Cn(r.errorMessage() ? 1 : -1), F(), Cn(r.isDeferredMode() ? 2 : 3));
  }, styles: [".bigframes-widget.bigframes-widget[_ngcontent-%COMP%]{--bf-bg: white;--bf-border-color: #ccc;--bf-error-bg: #fbe;--bf-error-border: red;--bf-error-fg: black;--bf-fg: black;--bf-header-bg: #f5f5f5;--bf-null-fg: gray;--bf-row-even-bg: #f5f5f5;--bf-row-odd-bg: white;background-color:var(--bf-bg);box-sizing:border-box;color:var(--bf-fg);display:flex;flex-direction:column;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;margin:0;padding:0}.bigframes-widget[_ngcontent-%COMP%]   *[_ngcontent-%COMP%]{box-sizing:border-box}@media(prefers-color-scheme:dark){.bigframes-widget.bigframes-widget[_ngcontent-%COMP%]{--bf-bg: var(--vscode-editor-background, #202124);--bf-border-color: #444;--bf-error-bg: #511;--bf-error-border: #f88;--bf-error-fg: #fcc;--bf-fg: white;--bf-header-bg: var(--vscode-editor-background, black);--bf-null-fg: #aaa;--bf-row-even-bg: #202124;--bf-row-odd-bg: #383838}}.bigframes-widget.bigframes-dark-mode.bigframes-dark-mode[_ngcontent-%COMP%]{--bf-bg: var(--vscode-editor-background, #202124);--bf-border-color: #444;--bf-error-bg: #511;--bf-error-border: #f88;--bf-error-fg: #fcc;--bf-fg: white;--bf-header-bg: var(--vscode-editor-background, black);--bf-null-fg: #aaa;--bf-row-even-bg: #202124;--bf-row-odd-bg: #383838}.bigframes-widget[_ngcontent-%COMP%]   .table-container[_ngcontent-%COMP%]{background-color:var(--bf-bg);margin:0;max-height:620px;overflow:auto;padding:0}.bigframes-widget[_ngcontent-%COMP%]   .footer[_ngcontent-%COMP%]{align-items:center;background-color:var(--bf-bg);color:var(--bf-fg);display:flex;font-size:.8rem;justify-content:space-between;padding:8px}.bigframes-widget[_ngcontent-%COMP%]   .footer[_ngcontent-%COMP%] > *[_ngcontent-%COMP%]{flex:1}.bigframes-widget[_ngcontent-%COMP%]   .pagination[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:4px;justify-content:center;padding:4px}.bigframes-widget[_ngcontent-%COMP%]   .page-indicator[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .row-count[_ngcontent-%COMP%]{margin:0 8px}.bigframes-widget[_ngcontent-%COMP%]   .settings[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:16px;justify-content:end}.bigframes-widget[_ngcontent-%COMP%]   .page-size[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .max-columns[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:4px}.bigframes-widget[_ngcontent-%COMP%]   .page-size[_ngcontent-%COMP%]   label[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .max-columns[_ngcontent-%COMP%]   label[_ngcontent-%COMP%]{margin-right:8px}.bigframes-widget[_ngcontent-%COMP%]     table.bigframes-widget-table, .bigframes-widget[_ngcontent-%COMP%]     table.dataframe{background-color:var(--bf-bg);border:1px solid var(--bf-border-color);border-collapse:collapse;border-spacing:0;box-shadow:none;color:var(--bf-fg);margin:0;outline:none;text-align:left;width:auto}.bigframes-widget[_ngcontent-%COMP%]     tr{border:none}.bigframes-widget[_ngcontent-%COMP%]     th{background-color:var(--bf-header-bg);border:1px solid var(--bf-border-color);color:var(--bf-fg);padding:0;position:sticky;text-align:left;top:0;z-index:1}.bigframes-widget[_ngcontent-%COMP%]     td{border:1px solid var(--bf-border-color);color:var(--bf-fg);padding:.5em}.bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(odd), .bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(odd) td{background-color:var(--bf-row-odd-bg)}.bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(2n), .bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(2n) td{background-color:var(--bf-row-even-bg)}.bigframes-widget[_ngcontent-%COMP%]     .bf-header-content{box-sizing:border-box;height:100%;overflow:auto;padding:.5em;resize:horizontal;width:100%}.bigframes-widget[_ngcontent-%COMP%]     th .sort-indicator{padding-left:4px;visibility:hidden}.bigframes-widget[_ngcontent-%COMP%]     th:hover .sort-indicator{visibility:visible}.bigframes-widget[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]{background-color:transparent;border:1px solid currentColor;border-radius:4px;color:inherit;cursor:pointer;display:inline-block;padding:2px 8px;text-align:center;text-decoration:none;-webkit-user-select:none;user-select:none;vertical-align:middle}.bigframes-widget[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]:disabled{opacity:.65;pointer-events:none}.bigframes-widget[_ngcontent-%COMP%]   .bigframes-error-message[_ngcontent-%COMP%]{background-color:var(--bf-error-bg);border:1px solid var(--bf-error-border);border-radius:4px;color:var(--bf-error-fg);font-size:14px;margin-bottom:8px;padding:8px}.bigframes-widget[_ngcontent-%COMP%]     .cell-align-right{text-align:right}.bigframes-widget[_ngcontent-%COMP%]     .cell-align-left{text-align:left}.bigframes-widget[_ngcontent-%COMP%]     .null-value{color:var(--bf-null-fg)}.bigframes-widget[_ngcontent-%COMP%]     .debug-info{border-top:1px solid var(--bf-border-color)}.bigframes-widget[_ngcontent-%COMP%]   .deferred-container[_ngcontent-%COMP%]{align-items:center;display:flex;justify-content:center;min-height:220px;padding:24px;width:100%}.bigframes-widget[_ngcontent-%COMP%]   .deferred-card[_ngcontent-%COMP%]{background:linear-gradient(135deg,#fff9,#ffffff4d);border:1px solid rgba(255,255,255,.4);border-radius:16px;box-shadow:0 8px 32px #1f268712;display:flex;flex-direction:column;gap:16px;max-width:500px;padding:32px;text-align:center;transition:all .3s ease-in-out}.bigframes-widget.bigframes-dark-mode[_ngcontent-%COMP%]   .deferred-card[_ngcontent-%COMP%]{background:linear-gradient(135deg,#20212499,#2021244d);border:1px solid rgba(255,255,255,.1);box-shadow:0 8px 32px #0000004d}@media(prefers-color-scheme:dark){.bigframes-widget[_ngcontent-%COMP%]   .deferred-card[_ngcontent-%COMP%]{background:linear-gradient(135deg,#20212499,#2021244d);border:1px solid rgba(255,255,255,.1);box-shadow:0 8px 32px #0000004d}}.bigframes-widget[_ngcontent-%COMP%]   .deferred-title[_ngcontent-%COMP%]{font-size:1.1rem;font-weight:600;margin:0}.bigframes-widget[_ngcontent-%COMP%]   .deferred-estimate[_ngcontent-%COMP%]{color:var(--bf-null-fg);font-size:.9rem;margin:0}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]{align-items:center;background-color:var(--bf-fg);border:1px solid var(--bf-fg);border-radius:8px;color:var(--bf-bg);cursor:pointer;display:inline-flex;font-size:14px;font-weight:600;gap:8px;justify-content:center;padding:10px 20px;transition:transform .2s ease,opacity .2s ease}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]:hover{opacity:.9;transform:translateY(-1px)}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]:active{transform:translateY(0)}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]:disabled{cursor:not-allowed;opacity:.6}.bigframes-widget[_ngcontent-%COMP%]   .spinner[_ngcontent-%COMP%]{animation:_ngcontent-%COMP%_spin 1s linear infinite;border:2px solid currentColor;border-radius:50%;border-top-color:transparent;display:inline-block;height:12px;width:12px}@keyframes _ngcontent-%COMP%_spin{to{transform:rotate(360deg)}}"] });
};
function Gm({ model: e12, el: t }) {
  let n = document.createElement("app-root");
  t.appendChild(n);
  let r = { providers: [Vi(), { provide: "ANYWIDGET_MODEL", useValue: e12 }] };
  Da(Eo, r).catch((o) => console.error(o));
}
var iS = { render: Gm };
export {
  iS as default
};
