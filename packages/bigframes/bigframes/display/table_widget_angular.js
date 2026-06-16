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
var cd = Object.defineProperty;
var ld = Object.defineProperties;
var ud = Object.getOwnPropertyDescriptors;
var Ta = Object.getOwnPropertySymbols;
var dd = Object.prototype.hasOwnProperty;
var fd = Object.prototype.propertyIsEnumerable;
var Ma = (e12, t, n) => t in e12 ? cd(e12, t, { enumerable: true, configurable: true, writable: true, value: n }) : e12[t] = n;
var x = (e12, t) => {
  for (var n in t ||= {})
    dd.call(t, n) && Ma(e12, n, t[n]);
  if (Ta)
    for (var n of Ta(t))
      fd.call(t, n) && Ma(e12, n, t[n]);
  return e12;
};
var R = (e12, t) => ld(e12, ud(t));
var V = null;
var On = false;
var wo = 1;
var pd = null;
var Q = Symbol("SIGNAL");
function g(e12) {
  let t = V;
  return V = e12, t;
}
function Pn() {
  return V;
}
var pt = { version: 0, lastCleanEpoch: 0, dirty: false, producers: void 0, producersTail: void 0, consumers: void 0, consumersTail: void 0, recomputing: false, consumerAllowSignalWrites: false, consumerIsAlwaysLive: false, kind: "unknown", producerMustRecompute: () => false, producerRecomputeValue: () => {
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
  if (o !== void 0 && o.consumer === V && (!r || gd(o, V)))
    return;
  let i = gt(V), s = { producer: e12, consumer: V, nextProducer: n, prevConsumer: o, lastReadVersion: e12.version, nextConsumer: void 0 };
  V.producersTail = s, t !== void 0 ? t.nextProducer = s : V.producers = s, i && xa(e12, s);
}
function _a() {
  wo++;
}
function Mo(e12) {
  if (!(gt(e12) && !e12.dirty) && !(!e12.dirty && e12.lastCleanEpoch === wo)) {
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
      r.dirty || hd(r);
    }
  } finally {
    On = t;
  }
}
function So() {
  return V?.consumerAllowSignalWrites !== false;
}
function hd(e12) {
  e12.dirty = true, _o(e12), e12.consumerMarkedDirty?.(e12);
}
function Co(e12) {
  e12.dirty = false, e12.lastCleanEpoch = wo;
}
function zt(e12) {
  return e12 && Sa(e12), g(e12);
}
function Sa(e12) {
  e12.producersTail = void 0, e12.recomputing = true;
}
function Ln(e12, t) {
  g(t), e12 && Na(e12);
}
function Na(e12) {
  e12.recomputing = false;
  let t = e12.producersTail, n = t !== void 0 ? t.nextProducer : e12.producers;
  if (n !== void 0) {
    if (gt(e12))
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
function ht(e12) {
  if (gt(e12)) {
    let t = e12.producers;
    for (; t !== void 0; )
      t = No(t);
  }
  e12.producers = void 0, e12.producersTail = void 0, e12.consumers = void 0, e12.consumersTail = void 0;
}
function xa(e12, t) {
  let n = e12.consumersTail, r = gt(e12);
  if (n !== void 0 ? (t.nextConsumer = n.nextConsumer, n.nextConsumer = t) : (t.nextConsumer = void 0, e12.consumers = t), t.prevConsumer = n, e12.consumersTail = t, !r)
    for (let o = e12.producers; o !== void 0; o = o.nextProducer)
      xa(o.producer, o);
}
function No(e12) {
  let t = e12.producer, n = e12.nextProducer, r = e12.nextConsumer, o = e12.prevConsumer;
  if (e12.nextConsumer = void 0, e12.prevConsumer = void 0, r !== void 0 ? r.prevConsumer = o : t.consumersTail = o, o !== void 0)
    o.nextConsumer = r;
  else if (t.consumers = r, !gt(t)) {
    let i = t.producers;
    for (; i !== void 0; )
      i = No(i);
  }
  return n;
}
function gt(e12) {
  return e12.consumerIsAlwaysLive || e12.consumers !== void 0;
}
function xo(e12) {
  pd?.(e12);
}
function gd(e12, t) {
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
  let n = Object.create(md);
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
var md = R(x({}, pt), { value: Do, dirty: true, error: null, equal: Ro, kind: "computed", producerMustRecompute(e12) {
  return e12.value === Do || e12.value === bo;
}, producerRecomputeValue(e12) {
  if (e12.value === bo)
    throw new Error("");
  let t = e12.value;
  e12.value = bo;
  let n = zt(e12), r, o = false;
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
function yd() {
  throw new Error();
}
var Ra = yd;
function Aa(e12) {
  Ra(e12);
}
function Ao(e12) {
  Ra = e12;
}
var vd = null;
function Oo(e12, t) {
  let n = Object.create(Pa);
  n.value = e12, t !== void 0 && (n.equal = t);
  let r = () => Oa(n);
  return r[Q] = n, xo(n), [r, (s) => ko(n, s), (s) => ka(n, s)];
}
function Oa(e12) {
  return To(e12), e12.value;
}
function ko(e12, t) {
  So() || Aa(e12), e12.equal(e12.value, t) || (e12.value = t, Ed(e12));
}
function ka(e12, t) {
  So() || Aa(e12), ko(e12, t(e12.value));
}
var Pa = R(x({}, pt), { equal: Ro, value: void 0, kind: "signal" });
function Ed(e12) {
  e12.version++, _a(), _o(e12), vd?.(e12);
}
var Po = R(x({}, pt), { consumerIsAlwaysLive: true, consumerAllowSignalWrites: true, dirty: true, kind: "effect" });
function Lo(e12) {
  if (e12.dirty = false, e12.version > 0 && !Fn(e12))
    return;
  e12.version++;
  let t = zt(e12);
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
function Wt(e12, t) {
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
            La(i);
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
        La(t);
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
    n === t ? this._parentage = null : Array.isArray(n) && Wt(n, t);
  }
  remove(t) {
    let { _finalizers: n } = this;
    n && Wt(n, t), t instanceof e && t._removeParent(this);
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
function La(e12) {
  U(e12) ? e12() : e12.unsubscribe();
}
var ne = { onUnhandledError: null, onStoppedNotification: null, Promise: void 0, useDeprecatedSynchronousErrorHandling: false, useDeprecatedNextContext: false };
var mt = { setTimeout(e12, t, ...n) {
  let { delegate: r } = mt;
  return r?.setTimeout ? r.setTimeout(e12, t, ...n) : setTimeout(e12, t, ...n);
}, clearTimeout(e12) {
  let { delegate: t } = mt;
  return (t?.clearTimeout || clearTimeout)(e12);
}, delegate: void 0 };
function Fa(e12) {
  mt.setTimeout(() => {
    let { onUnhandledError: t } = ne;
    if (t)
      t(e12);
    else
      throw e12;
  });
}
function jo() {
}
var ja = Ho("C", void 0, void 0);
function Ha(e12) {
  return Ho("E", void 0, e12);
}
function Va(e12) {
  return Ho("N", e12, void 0);
}
function Ho(e12, t, n) {
  return { kind: e12, value: t, error: n };
}
var Ge = null;
function yt(e12) {
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
function Ba(e12) {
  ne.useDeprecatedSynchronousErrorHandling && Ge && (Ge.errorThrown = true, Ge.error = e12);
}
var qe = class extends $ {
  constructor(t) {
    super(), this.isStopped = false, t ? (this.destination = t, Bn(t) && t.add(this)) : this.destination = bd;
  }
  static create(t, n, r) {
    return new vt(t, n, r);
  }
  next(t) {
    this.isStopped ? Bo(Va(t), this) : this._next(t);
  }
  error(t) {
    this.isStopped ? Bo(Ha(t), this) : (this.isStopped = true, this._error(t));
  }
  complete() {
    this.isStopped ? Bo(ja, this) : (this.isStopped = true, this._complete());
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
var Id = Function.prototype.bind;
function Vo(e12, t) {
  return Id.call(e12, t);
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
var vt = class extends qe {
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
  ne.useDeprecatedSynchronousErrorHandling ? Ba(e12) : Fa(e12);
}
function Dd(e12) {
  throw e12;
}
function Bo(e12, t) {
  let { onStoppedNotification: n } = ne;
  n && mt.setTimeout(() => n(e12, t));
}
var bd = { closed: true, next: jo, error: Dd, complete: jo };
var $a = typeof Symbol == "function" && Symbol.observable || "@@observable";
function Ua(e12) {
  return e12;
}
function za(e12) {
  return e12.length === 0 ? Ua : e12.length === 1 ? e12[0] : function(n) {
    return e12.reduce((r, o) => o(r), n);
  };
}
var Et = (() => {
  class e12 {
    constructor(n) {
      n && (this._subscribe = n);
    }
    lift(n) {
      let r = new e12();
      return r.source = this, r.operator = n, r;
    }
    subscribe(n, r, o) {
      let i = wd(n) ? n : new vt(n, r, o);
      return yt(() => {
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
      return r = Wa(r), new r((o, i) => {
        let s = new vt({ next: (a) => {
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
    [$a]() {
      return this;
    }
    pipe(...n) {
      return za(n)(this);
    }
    toPromise(n) {
      return n = Wa(n), new n((r, o) => {
        let i;
        this.subscribe((s) => i = s, (s) => o(s), () => r(i));
      });
    }
  }
  return e12.create = (t) => new e12(t), e12;
})();
function Wa(e12) {
  var t;
  return (t = e12 ?? ne.Promise) !== null && t !== void 0 ? t : Promise;
}
function Cd(e12) {
  return e12 && U(e12.next) && U(e12.error) && U(e12.complete);
}
function wd(e12) {
  return e12 && e12 instanceof qe || Cd(e12) && Bn(e12);
}
function Td(e12) {
  return U(e12?.lift);
}
function Ga(e12) {
  return (t) => {
    if (Td(t))
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
function qa(e12, t, n, r, o) {
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
var Za = Hn((e12) => function() {
  e12(this), this.name = "ObjectUnsubscribedError", this.message = "object unsubscribed";
});
var ve = (() => {
  class e12 extends Et {
    constructor() {
      super(), this.closed = false, this.currentObservers = null, this.observers = [], this.isStopped = false, this.hasError = false, this.thrownError = null;
    }
    lift(n) {
      let r = new Un(this, this);
      return r.operator = n, r;
    }
    _throwIfClosed() {
      if (this.closed)
        throw new Za();
    }
    next(n) {
      yt(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.currentObservers || (this.currentObservers = Array.from(this.observers));
          for (let r of this.currentObservers)
            r.next(n);
        }
      });
    }
    error(n) {
      yt(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.hasError = this.isStopped = true, this.thrownError = n;
          let { observers: r } = this;
          for (; r.length; )
            r.shift().error(n);
        }
      });
    }
    complete() {
      yt(() => {
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
        this.currentObservers = null, Wt(i, n);
      }));
    }
    _checkFinalizedStatuses(n) {
      let { hasError: r, thrownError: o, isStopped: i } = this;
      r ? n.error(o) : i && n.complete();
    }
    asObservable() {
      let n = new Et();
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
var Gt = class extends ve {
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
  return Ga((n, r) => {
    let o = 0;
    n.subscribe(qa(r, (i) => {
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
var Qa = Symbol("NotFound");
function It(e12) {
  return e12 === Qa || e12?.name === "\u0275NotFound";
}
var Jn = "https://angular.dev/best-practices/security#preventing-cross-site-scripting-xss";
var v = class extends Error {
  code;
  constructor(t, n) {
    super(Xn(t, n)), this.code = t;
  }
};
function Md(e12) {
  return `NG0${Math.abs(e12)}`;
}
function Xn(e12, t) {
  return `${Md(e12)}${t ? ": " + t : ""}`;
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
var _d = w({ __forward_ref__: w });
function tr(e12) {
  return e12.__forward_ref__ = tr, e12;
}
function q(e12) {
  return ec(e12) ? e12() : e12;
}
function ec(e12) {
  return typeof e12 == "function" && e12.hasOwnProperty(_d) && e12.__forward_ref__ === tr;
}
function _(e12) {
  return { token: e12.token, providedIn: e12.providedIn || null, factory: e12.factory, value: void 0 };
}
function nr(e12) {
  return Sd(e12, rr);
}
function Sd(e12, t) {
  return e12.hasOwnProperty(t) && e12[t] || null;
}
function Nd(e12) {
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
var Ya = w({ __NG_ENV_ID__: w });
function Xe(e12) {
  return di(e12, "@Component"), e12[ai] || null;
}
function ui(e12) {
  return di(e12, "@Directive"), e12[ci] || null;
}
function tc(e12) {
  return di(e12, "@Pipe"), e12[li] || null;
}
function di(e12, t) {
  if (e12 == null)
    throw new v(-919, false);
}
function fi(e12) {
  return typeof e12 == "string" ? e12 : e12 == null ? "" : String(e12);
}
var nc = w({ ngErrorCode: w });
var xd = w({ ngErrorMessage: w });
var Rd = w({ ngTokenPath: w });
function pi(e12, t) {
  return rc("", -200, t);
}
function or(e12, t) {
  throw new v(-201, false);
}
function rc(e12, t, n) {
  let r = new v(t, e12);
  return r[nc] = t, r[xd] = e12, n && (r[Rd] = n), r;
}
function Ad(e12) {
  return e12[nc];
}
var Qo;
function oc() {
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
var Od = {};
var Ze = Od;
var kd = "__NG_DI_FLAG__";
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
      if (It(o))
        return o;
      throw o;
    }
  }
};
function Pd(e12, t = 0) {
  let n = zn();
  if (n === void 0)
    throw new v(-203, false);
  if (n === null)
    return hi(e12, void 0, t);
  {
    let r = Ld(t), o = n.retrieve(e12, r);
    if (It(o)) {
      if (r.optional)
        return null;
      throw o;
    }
    return o;
  }
}
function b(e12, t = 0) {
  return (oc() || Pd)(q(e12), t);
}
function E(e12, t) {
  return b(e12, Qe(t));
}
function Qe(e12) {
  return typeof e12 > "u" || typeof e12 == "number" ? e12 : 0 | (e12.optional && 8) | (e12.host && 1) | (e12.self && 2) | (e12.skipSelf && 4);
}
function Ld(e12) {
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
        let a = r[s], c = Fd(a);
        typeof c == "number" ? c === -1 ? o = a.token : i |= c : o = a;
      }
      t.push(b(o, i));
    } else
      t.push(b(r));
  }
  return t;
}
function Fd(e12) {
  return e12[kd];
}
function bt(e12, t) {
  let n = e12.hasOwnProperty(Zo);
  return n ? e12[Zo] : null;
}
function ic(e12, t, n) {
  if (e12.length !== t.length)
    return false;
  for (let r = 0; r < e12.length; r++) {
    let o = e12[r], i = t[r];
    if (n && (o = n(o), i = n(i)), i !== o)
      return false;
  }
  return true;
}
function sc(e12) {
  return e12.flat(Number.POSITIVE_INFINITY);
}
function ir(e12, t) {
  e12.forEach((n) => Array.isArray(n) ? ir(n, t) : t(n));
}
function gi(e12, t, n) {
  t >= e12.length ? e12.push(n) : e12.splice(t, 0, n);
}
function Jt(e12, t) {
  return t >= e12.length - 1 ? e12.pop() : e12.splice(t, 1)[0];
}
function ac(e12, t, n, r) {
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
function cc(e12, t, n) {
  let r = Ct(e12, t);
  return r >= 0 ? e12[r | 1] = n : (r = ~r, ac(e12, r, t, n)), r;
}
function sr(e12, t) {
  let n = Ct(e12, t);
  if (n >= 0)
    return e12[n | 1];
}
function Ct(e12, t) {
  return jd(e12, t, 1);
}
function jd(e12, t, n) {
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
var Zt = class {
  get(t, n = Ze) {
    if (n === Ze) {
      let o = rc("", -201);
      throw o.name = "\u0275NotFound", o;
    }
    return n;
  }
};
function wt(e12) {
  return { \u0275providers: e12 };
}
function lc(e12) {
  return wt([{ provide: tt, multi: true, useValue: e12 }]);
}
function uc(...e12) {
  return { \u0275providers: vi(true, e12), \u0275fromNgModule: true };
}
function vi(e12, ...t) {
  let n = [], r = /* @__PURE__ */ new Set(), o, i = (s) => {
    n.push(s);
  };
  return ir(t, (s) => {
    let a = s;
    qn(a, i, [], r) && (o ||= [], o.push(a));
  }), o !== void 0 && dc(o, i), n;
}
function dc(e12, t) {
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
      }), l !== void 0 && dc(l, t);
    }
    if (!a) {
      let l = bt(o) || (() => new o());
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
var Hd = w({ provide: String, useValue: w });
function fc(e12) {
  return e12 !== null && typeof e12 == "object" && Hd in e12;
}
function Vd(e12) {
  return !!(e12 && e12.useExisting);
}
function Bd(e12) {
  return !!(e12 && e12.useFactory);
}
function Zn(e12) {
  return typeof e12 == "function";
}
var Xt = new D("");
var Wn = {};
var Ka = {};
var Go;
function en() {
  return Go === void 0 && (Go = new Zt()), Go;
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
    super(), this.parent = n, this.source = r, this.scopes = o, Xo(t, (s) => this.processProvider(s)), this.records.set(mi, Dt(void 0, this)), o.has("environment") && this.records.set(Y, Dt(void 0, this));
    let i = this.records.get(Xt);
    i != null && typeof i.value == "string" && this.scopes.add(i.value), this.injectorDefTypes = new Set(this.get(yi, ke, { self: true }));
  }
  retrieve(t, n) {
    let r = Qe(n) || 0;
    try {
      return this.get(t, Ze, r);
    } catch (o) {
      if (It(o))
        return o;
      throw o;
    }
  }
  destroy() {
    qt(this), this._destroyed = true;
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
    return qt(this), this._onDestroyHooks.push(t), () => this.removeOnDestroy(t);
  }
  runInContext(t) {
    qt(this);
    let n = le(this), r = G(void 0), o;
    try {
      return t();
    } finally {
      le(n), G(r);
    }
  }
  get(t, n = Ze, r) {
    if (qt(this), t.hasOwnProperty(Ya))
      return t[Ya](this);
    let o = Qe(r), i, s = le(this), a = G(void 0);
    try {
      if (!(o & 4)) {
        let l = this.records.get(t);
        if (l === void 0) {
          let u = Gd(t) && nr(t);
          u && this.injectableDefInScope(u) ? l = Dt(Jo(t), Wn) : l = null, this.records.set(t, l);
        }
        if (l != null)
          return this.hydrate(t, l, o);
      }
      let c = o & 2 ? en() : this.parent;
      return n = o & 8 && n === Ze ? null : n, c.get(t, n);
    } catch (c) {
      let l = Ad(c);
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
    let n = Zn(t) ? t : q(t && t.provide), r = Ud(t);
    if (!Zn(t) && t.multi === true) {
      let o = this.records.get(n);
      o || (o = Dt(void 0, Wn, true), o.factory = () => Ko(o.multi), this.records.set(n, o)), n = t, o.multi.push(t);
    }
    this.records.set(n, r);
  }
  hydrate(t, n, r) {
    let o = g(null);
    try {
      if (n.value === Ka)
        throw pi("");
      return n.value === Wn && (n.value = Ka, n.value = n.factory(void 0, r)), typeof n.value == "object" && n.value && Wd(n.value) && this._ngOnDestroyHooks.add(n.value), n.value;
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
  let t = nr(e12), n = t !== null ? t.factory : bt(e12);
  if (n !== null)
    return n;
  if (e12 instanceof D)
    throw new v(-204, false);
  if (e12 instanceof Function)
    return $d(e12);
  throw new v(-204, false);
}
function $d(e12) {
  if (e12.length > 0)
    throw new v(-204, false);
  let n = Nd(e12);
  return n !== null ? () => n.factory(e12) : () => new e12();
}
function Ud(e12) {
  if (fc(e12))
    return Dt(void 0, e12.useValue);
  {
    let t = pc(e12);
    return Dt(t, Wn);
  }
}
function pc(e12, t, n) {
  let r;
  if (Zn(e12)) {
    let o = q(e12);
    return bt(o) || Jo(o);
  } else if (fc(e12))
    r = () => q(e12.useValue);
  else if (Bd(e12))
    r = () => e12.useFactory(...Ko(e12.deps || []));
  else if (Vd(e12))
    r = (o, i) => b(q(e12.useExisting), i !== void 0 && i & 8 ? 8 : void 0);
  else {
    let o = q(e12 && (e12.useClass || e12.provide));
    if (zd(e12))
      r = () => new o(...Ko(e12.deps));
    else
      return bt(o) || Jo(o);
  }
  return r;
}
function qt(e12) {
  if (e12.destroyed)
    throw new v(-205, false);
}
function Dt(e12, t, n = false) {
  return { factory: e12, value: t, multi: n ? [] : void 0 };
}
function zd(e12) {
  return !!e12.deps;
}
function Wd(e12) {
  return e12 !== null && typeof e12 == "object" && typeof e12.ngOnDestroy == "function";
}
function Gd(e12) {
  return typeof e12 == "function" || typeof e12 == "object" && e12.ngMetadataName === "InjectionToken";
}
function Xo(e12, t) {
  for (let n of e12)
    Array.isArray(n) ? Xo(n, t) : n && si(n) ? Xo(n.\u0275providers, t) : t(n);
}
function ar(e12, t) {
  let n;
  e12 instanceof Ye ? (qt(e12), n = e12) : n = new Yo(e12);
  let r, o = le(n), i = G(void 0);
  try {
    return t();
  } finally {
    le(o), G(i);
  }
}
function hc() {
  return oc() !== void 0 || zn() != null;
}
var re = 0;
var m = 1;
var y = 2;
var A = 3;
var J = 4;
var X = 5;
var Tt = 6;
var Mt = 7;
var N = 8;
var be = 9;
var de = 10;
var O = 11;
var _t = 12;
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
var gc = 1;
var bi = 6;
var Ve = 7;
var tn = 8;
var ot = 9;
var S = 10;
function Be(e12) {
  return Array.isArray(e12) && typeof e12[gc] == "object";
}
function oe(e12) {
  return Array.isArray(e12) && e12[gc] === true;
}
function Ci(e12) {
  return (e12.flags & 4) !== 0;
}
function St(e12) {
  return e12.componentOffset > -1;
}
function wi(e12) {
  return (e12.flags & 1) === 1;
}
function Nt(e12) {
  return !!e12.template;
}
function xt(e12) {
  return (e12[y] & 512) !== 0;
}
function it(e12) {
  return (e12[y] & 256) === 256;
}
var mc = "svg";
var yc = "math";
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
function vc(e12) {
  return (e12[y] & 4) === 4;
}
function dr(e12) {
  return (e12[y] & 128) === 128;
}
function Ec(e12) {
  return oe(e12[A]);
}
function he(e12, t) {
  return t == null ? null : e12[t];
}
function Mi(e12) {
  e12[rt] = 0;
}
function _i(e12) {
  e12[y] & 1024 || (e12[y] |= 1024, dr(e12) && Rt(e12));
}
function Ic(e12, t) {
  for (; e12 > 0; )
    t = t[nt], e12--;
  return t;
}
function nn(e12) {
  return !!(e12[y] & 9216 || e12[Z]?.dirty);
}
function fr(e12) {
  e12[de].changeDetectionScheduler?.notify(8), e12[y] & 64 && (e12[y] |= 1024), nn(e12) && Rt(e12);
}
function Rt(e12) {
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
function Dc(e12, t) {
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
  return e12[Mt] ??= [];
}
function xi(e12) {
  return e12.cleanup ??= [];
}
function bc(e12, t, n, r) {
  let o = Ni(t);
  o.push(n), e12.firstCreatePass && xi(e12).push(r, o.length - 1);
}
var I = { lFrame: jc(null), bindingsEnabled: true, skipHydrationRootTNode: null };
var ei = false;
function Cc() {
  return I.lFrame.elementDepthCount;
}
function wc() {
  I.lFrame.elementDepthCount++;
}
function Tc() {
  I.lFrame.elementDepthCount--;
}
function Mc() {
  return I.skipHydrationRootTNode !== null;
}
function _c(e12) {
  return I.skipHydrationRootTNode === e12;
}
function Sc() {
  I.skipHydrationRootTNode = null;
}
function M() {
  return I.lFrame.lView;
}
function ie() {
  return I.lFrame.tView;
}
function Te(e12) {
  return I.lFrame.contextLView = e12, e12[N];
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
function Nc() {
  let e12 = I.lFrame, t = e12.currentTNode;
  return e12.isParent ? t : t.parent;
}
function At(e12, t) {
  let n = I.lFrame;
  n.currentTNode = e12, n.isParent = t;
}
function Ai() {
  return I.lFrame.isParent;
}
function xc() {
  I.lFrame.isParent = false;
}
function Oi() {
  return ei;
}
function Qt(e12) {
  let t = ei;
  return ei = e12, t;
}
function Rc(e12) {
  return I.lFrame.bindingIndex = e12;
}
function rn() {
  return I.lFrame.bindingIndex++;
}
function Ac(e12) {
  let t = I.lFrame, n = t.bindingIndex;
  return t.bindingIndex = t.bindingIndex + e12, n;
}
function Oc() {
  return I.lFrame.inI18n;
}
function kc(e12, t) {
  let n = I.lFrame;
  n.bindingIndex = n.bindingRootIndex = e12, pr(t);
}
function Pc() {
  return I.lFrame.currentDirectiveIndex;
}
function pr(e12) {
  I.lFrame.currentDirectiveIndex = e12;
}
function Lc(e12) {
  let t = I.lFrame.currentDirectiveIndex;
  return t === -1 ? null : e12[t];
}
function ki() {
  return I.lFrame.currentQueryIndex;
}
function hr(e12) {
  I.lFrame.currentQueryIndex = e12;
}
function qd(e12) {
  let t = e12[m];
  return t.type === 2 ? t.declTNode : t.type === 1 ? e12[X] : null;
}
function Pi(e12, t, n) {
  if (n & 4) {
    let o = t, i = e12;
    for (; o = o.parent, o === null && !(n & 1); )
      if (o = qd(i), o === null || (i = i[nt], o.type & 10))
        break;
    if (o === null)
      return false;
    t = o, e12 = i;
  }
  let r = I.lFrame = Fc();
  return r.currentTNode = t, r.lView = e12, true;
}
function gr(e12) {
  let t = Fc(), n = e12[m];
  I.lFrame = t, t.currentTNode = n.firstChild, t.lView = e12, t.tView = n, t.contextLView = e12, t.bindingIndex = n.bindingStartIndex, t.inI18n = false;
}
function Fc() {
  let e12 = I.lFrame, t = e12 === null ? null : e12.child;
  return t === null ? jc(e12) : t;
}
function jc(e12) {
  let t = { currentTNode: null, isParent: true, lView: null, tView: null, selectedIndex: -1, contextLView: null, elementDepthCount: 0, currentNamespace: null, currentDirectiveIndex: -1, bindingRootIndex: -1, bindingIndex: -1, currentQueryIndex: 0, parent: e12, child: null, inI18n: false };
  return e12 !== null && (e12.child = t), t;
}
function Hc() {
  let e12 = I.lFrame;
  return I.lFrame = e12.parent, e12.currentTNode = null, e12.lView = null, e12;
}
var Li = Hc;
function mr() {
  let e12 = Hc();
  e12.isParent = true, e12.tView = null, e12.selectedIndex = -1, e12.contextLView = null, e12.elementDepthCount = 0, e12.currentDirectiveIndex = -1, e12.currentNamespace = null, e12.bindingRootIndex = -1, e12.bindingIndex = -1, e12.currentQueryIndex = 0;
}
function Vc(e12) {
  return (I.lFrame.contextLView = Ic(e12, I.lFrame.contextLView))[N];
}
function $e() {
  return I.lFrame.selectedIndex;
}
function Ue(e12) {
  I.lFrame.selectedIndex = e12;
}
function Bc() {
  let e12 = I.lFrame;
  return ur(e12.tView, e12.selectedIndex);
}
function $c() {
  return I.lFrame.currentNamespace;
}
var Uc = true;
function yr() {
  return Uc;
}
function vr(e12) {
  Uc = e12;
}
function ti(e12, t = null, n = null, r) {
  let o = zc(e12, t, n, r);
  return o.resolveInjectorInitializers(), o;
}
function zc(e12, t = null, n = null, r, o = /* @__PURE__ */ new Set()) {
  let i = [n || ke, uc(e12)], s;
  return new Ye(i, t || en(), s || null, o);
}
var ue = class e2 {
  static THROW_IF_NOT_FOUND = Ze;
  static NULL = new Zt();
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
var Ot = /* @__PURE__ */ (() => {
  class e12 {
    static __NG_ELEMENT_ID__ = Zd;
    static __NG_ENV_ID__ = (n) => n;
  }
  return e12;
})();
var Qn = class extends Ot {
  _lView;
  constructor(t) {
    super(), this._lView = t;
  }
  get destroyed() {
    return it(this._lView);
  }
  onDestroy(t) {
    let n = this._lView;
    return Si(n, t), () => Dc(n, t);
  }
};
function Zd() {
  return new Qn(M());
}
var Wc = false;
var Gc = new D("");
var kt = (() => {
  class e12 {
    taskId = 0;
    pendingTasks = /* @__PURE__ */ new Set();
    destroyed = false;
    pendingTask = new Gt(false);
    debugTaskTracker = E(Gc, { optional: true });
    get hasPendingTasks() {
      return this.destroyed ? false : this.pendingTask.value;
    }
    get hasPendingTasksObservable() {
      return this.destroyed ? new Et((n) => {
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
    super(), this.__isAsync = t, hc() && (this.destroyRef = E(Ot, { optional: true }) ?? void 0, this.pendingTasks = E(kt, { optional: true }) ?? void 0);
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
function qc(e12) {
  return queueMicrotask(() => e12()), () => {
    e12 = Yn;
  };
}
var ji = "isAngularZone";
var Yt = ji + "_ID";
var Qd = 0;
var K = class e3 {
  hasPendingMacrotasks = false;
  hasPendingMicrotasks = false;
  isStable = true;
  onUnstable = new Ee(false);
  onMicrotaskEmpty = new Ee(false);
  onStable = new Ee(false);
  onError = new Ee(false);
  constructor(t) {
    let { enableLongStackTrace: n = false, shouldCoalesceEventChangeDetection: r = false, shouldCoalesceRunChangeDetection: o = false, scheduleInRootZone: i = Wc } = t;
    if (typeof Zone > "u")
      throw new v(908, false);
    Zone.assertZonePatched();
    let s = this;
    s._nesting = 0, s._outer = s._inner = Zone.current, Zone.TaskTrackingZoneSpec && (s._inner = s._inner.fork(new Zone.TaskTrackingZoneSpec())), n && Zone.longStackTraceZoneSpec && (s._inner = s._inner.fork(Zone.longStackTraceZoneSpec)), s.shouldCoalesceEventChangeDetection = !o && r, s.shouldCoalesceRunChangeDetection = o, s.callbackScheduled = false, s.scheduleInRootZone = i, Jd(s);
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
    let i = this._inner, s = i.scheduleEventTask("NgZoneEvent: " + o, t, Yd, Yn, Yn);
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
var Yd = {};
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
function Kd(e12) {
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
function Jd(e12) {
  let t = () => {
    Kd(e12);
  }, n = Qd++;
  e12._inner = e12._inner.fork({ name: "angular", properties: { [ji]: true, [Yt]: n, [Yt + n]: true }, onInvokeTask: (r, o, i, s, a, c) => {
    if (Xd(c))
      return r.invokeTask(i, s, a, c);
    try {
      return Ja(e12), r.invokeTask(i, s, a, c);
    } finally {
      (e12.shouldCoalesceEventChangeDetection && s.type === "eventTask" || e12.shouldCoalesceRunChangeDetection) && t(), Xa(e12);
    }
  }, onInvoke: (r, o, i, s, a, c, l) => {
    try {
      return Ja(e12), r.invoke(i, s, a, c, l);
    } finally {
      e12.shouldCoalesceRunChangeDetection && !e12.callbackScheduled && !ef(c) && t(), Xa(e12);
    }
  }, onHasTask: (r, o, i, s) => {
    r.hasTask(i, s), o === i && (s.change == "microTask" ? (e12._hasPendingMicrotasks = s.microTask, ri(e12), Hi(e12)) : s.change == "macroTask" && (e12.hasPendingMacrotasks = s.macroTask));
  }, onHandleError: (r, o, i, s) => (r.handleError(i, s), e12.runOutsideAngular(() => e12.onError.emit(s)), false) });
}
function ri(e12) {
  e12._hasPendingMicrotasks || (e12.shouldCoalesceEventChangeDetection || e12.shouldCoalesceRunChangeDetection) && e12.callbackScheduled === true ? e12.hasPendingMicrotasks = true : e12.hasPendingMicrotasks = false;
}
function Ja(e12) {
  e12._nesting++, e12.isStable && (e12.isStable = false, e12.onUnstable.emit(null));
}
function Xa(e12) {
  e12._nesting--, Hi(e12);
}
var Kt = class {
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
function Xd(e12) {
  return Zc(e12, "__ignore_ng_zone__");
}
function ef(e12) {
  return Zc(e12, "__scheduler_tick__");
}
function Zc(e12, t) {
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
var Qc = { provide: tt, useValue: () => {
  let e12 = E(De, { optional: true });
}, multi: true };
var tf = new D("", { factory: () => {
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
  typeof Zone < "u" ? Zone.root.run(o) : o(), E(Ot).onDestroy(() => {
    e12.removeEventListener("error", r), e12.removeEventListener("unhandledrejection", n);
  });
} });
function Vi() {
  return wt([lc(() => {
    E(tf);
  })]);
}
function j(e12, t) {
  let [n, r, o] = Oo(e12, t?.equal), i = n, s = i[Q];
  return i.set = r, i.update = o, i.asReadonly = Yc.bind(i), i;
}
function Yc() {
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
    static __NG_ELEMENT_ID__ = nf;
  }
  return e12;
})();
function nf() {
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
  let n = t?.injector ?? E(ue), r = t?.manualCleanup !== true ? n.get(Ot) : null, o, i = n.get(Er, null, { optional: true }), s = n.get(Ke);
  return i !== null ? (o = sf(i.view, s, e12), r instanceof Qn && r._lView === i.view && (r = null)) : o = af(e12, n.get(Ir), s), o.injector = n, r !== null && (o.onDestroyFns = [r.onDestroy(() => o.destroy())]), new Kn(o);
}
var Kc = R(x({}, Po), { cleanupFns: void 0, zone: null, onDestroyFns: null, run() {
  let e12 = Qt(false);
  try {
    Lo(this);
  } finally {
    Qt(e12);
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
var rf = R(x({}, Kc), { consumerMarkedDirty() {
  this.scheduler.schedule(this), this.notifier.notify(12);
}, destroy() {
  if (ht(this), this.onDestroyFns !== null)
    for (let e12 of this.onDestroyFns)
      e12();
  this.cleanup(), this.scheduler.remove(this);
} });
var of = R(x({}, Kc), { consumerMarkedDirty() {
  this.view[y] |= 8192, Rt(this.view), this.notifier.notify(13);
}, destroy() {
  if (ht(this), this.onDestroyFns !== null)
    for (let e12 of this.onDestroyFns)
      e12();
  this.cleanup(), this.view[Pe]?.delete(this);
} });
function sf(e12, t, n) {
  let r = Object.create(of);
  return r.view = e12, r.zone = typeof Zone < "u" ? Zone.current : null, r.notifier = t, r.fn = Jc(r, n), e12[Pe] ??= /* @__PURE__ */ new Set(), e12[Pe].add(r), r.consumerMarkedDirty(r), r;
}
function af(e12, t, n) {
  let r = Object.create(rf);
  return r.fn = Jc(r, e12), r.scheduler = t, r.notifier = n, r.zone = typeof Zone < "u" ? Zone.current : null, r.scheduler.add(r), r.notifier.notify(12), r;
}
function Jc(e12, t) {
  return () => {
    t((n) => (e12.cleanupFns ??= []).push(n));
  };
}
function Nl(e12) {
  return { toString: e12 }.toString();
}
function If(e12) {
  return typeof e12 == "function";
}
function xl(e12, t, n, r) {
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
function Df(e12) {
  return e12.type.prototype.ngOnChanges && (e12.setInput = Cf), bf;
}
function bf() {
  let e12 = Al(this), t = e12?.current;
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
function Cf(e12, t, n, r, o) {
  let i = this.declaredInputs[r], s = Al(e12) || wf(e12, { previous: et, current: null }), a = s.current || (s.current = {}), c = s.previous, l = c[i];
  a[i] = new Nr(l && l.currentValue, n, c === et), xl(e12, t, o, n);
}
var Rl = "__ngSimpleChanges__";
function Al(e12) {
  return e12[Rl] || null;
}
function wf(e12, t) {
  return e12[Rl] = t;
}
var Xc = [];
var T = function(e12, t = null, n) {
  for (let r = 0; r < Xc.length; r++) {
    let o = Xc[r];
    o(e12, t, n);
  }
};
var C = function(e12) {
  return e12[e12.TemplateCreateStart = 0] = "TemplateCreateStart", e12[e12.TemplateCreateEnd = 1] = "TemplateCreateEnd", e12[e12.TemplateUpdateStart = 2] = "TemplateUpdateStart", e12[e12.TemplateUpdateEnd = 3] = "TemplateUpdateEnd", e12[e12.LifecycleHookStart = 4] = "LifecycleHookStart", e12[e12.LifecycleHookEnd = 5] = "LifecycleHookEnd", e12[e12.OutputStart = 6] = "OutputStart", e12[e12.OutputEnd = 7] = "OutputEnd", e12[e12.BootstrapApplicationStart = 8] = "BootstrapApplicationStart", e12[e12.BootstrapApplicationEnd = 9] = "BootstrapApplicationEnd", e12[e12.BootstrapComponentStart = 10] = "BootstrapComponentStart", e12[e12.BootstrapComponentEnd = 11] = "BootstrapComponentEnd", e12[e12.ChangeDetectionStart = 12] = "ChangeDetectionStart", e12[e12.ChangeDetectionEnd = 13] = "ChangeDetectionEnd", e12[e12.ChangeDetectionSyncStart = 14] = "ChangeDetectionSyncStart", e12[e12.ChangeDetectionSyncEnd = 15] = "ChangeDetectionSyncEnd", e12[e12.AfterRenderHooksStart = 16] = "AfterRenderHooksStart", e12[e12.AfterRenderHooksEnd = 17] = "AfterRenderHooksEnd", e12[e12.ComponentStart = 18] = "ComponentStart", e12[e12.ComponentEnd = 19] = "ComponentEnd", e12[e12.DeferBlockStateStart = 20] = "DeferBlockStateStart", e12[e12.DeferBlockStateEnd = 21] = "DeferBlockStateEnd", e12[e12.DynamicComponentStart = 22] = "DynamicComponentStart", e12[e12.DynamicComponentEnd = 23] = "DynamicComponentEnd", e12[e12.HostBindingsUpdateStart = 24] = "HostBindingsUpdateStart", e12[e12.HostBindingsUpdateEnd = 25] = "HostBindingsUpdateEnd", e12;
}(C || {});
function Tf(e12, t, n) {
  let { ngOnChanges: r, ngOnInit: o, ngDoCheck: i } = t.type.prototype;
  if (r) {
    let s = Df(t);
    (n.preOrderHooks ??= []).push(e12, s), (n.preOrderCheckHooks ??= []).push(e12, s);
  }
  o && (n.preOrderHooks ??= []).push(0 - e12, o), i && ((n.preOrderHooks ??= []).push(e12, i), (n.preOrderCheckHooks ??= []).push(e12, i));
}
function Mf(e12, t) {
  for (let n = t.directiveStart, r = t.directiveEnd; n < r; n++) {
    let i = e12.data[n].type.prototype, { ngAfterContentInit: s, ngAfterContentChecked: a, ngAfterViewInit: c, ngAfterViewChecked: l, ngOnDestroy: u } = i;
    s && (e12.contentHooks ??= []).push(-n, s), a && ((e12.contentHooks ??= []).push(n, a), (e12.contentCheckHooks ??= []).push(n, a)), c && (e12.viewHooks ??= []).push(-n, c), l && ((e12.viewHooks ??= []).push(n, l), (e12.viewCheckHooks ??= []).push(n, l)), u != null && (e12.destroyHooks ??= []).push(n, u);
  }
}
function Tr(e12, t, n) {
  Ol(e12, t, 3, n);
}
function Mr(e12, t, n, r) {
  (e12[y] & 3) === n && Ol(e12, t, n, r);
}
function Ui(e12, t) {
  let n = e12[y];
  (n & 3) === t && (n &= 16383, n += 1, e12[y] = n);
}
function Ol(e12, t, n, r) {
  let o = r !== void 0 ? e12[rt] & 65535 : 0, i = r ?? -1, s = t.length - 1, a = 0;
  for (let c = o; c < s; c++)
    if (typeof t[c + 1] == "number") {
      if (a = t[c], r != null && a >= r)
        break;
    } else
      t[c] < 0 && (e12[rt] += 65536), (a < i || i == -1) && (_f(e12, n, t, c), e12[rt] = (e12[rt] & 4294901760) + c + 2), c++;
}
function el(e12, t) {
  T(C.LifecycleHookStart, e12, t);
  let n = g(null);
  try {
    t.call(e12);
  } finally {
    g(n), T(C.LifecycleHookEnd, e12, t);
  }
}
function _f(e12, t, n, r) {
  let o = n[r] < 0, i = n[r + 1], s = o ? -n[r] : n[r], a = e12[s];
  o ? e12[y] >> 14 < e12[rt] >> 16 && (e12[y] & 3) === t && (e12[y] += 16384, el(a, i)) : el(a, i);
}
var Lt = -1;
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
function Sf(e12, t, n) {
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
      Nf(i) ? e12.setProperty(t, i, s) : e12.setAttribute(t, i, s), r++;
    }
  }
  return r;
}
function Nf(e12) {
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
        typeof o == "number" ? n = o : n === 0 || (n === -1 || n === 2 ? tl(e12, n, o, null, t[++r]) : tl(e12, n, o, null, null));
      }
    }
  return e12;
}
function tl(e12, t, n, r, o) {
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
function kl(e12) {
  return e12 !== Lt;
}
function xr(e12) {
  return e12 & 32767;
}
function xf(e12) {
  return e12 >> 16;
}
function Rr(e12, t) {
  let n = xf(e12), r = t;
  for (; n > 0; )
    r = r[nt], n--;
  return r;
}
var Yi = true;
function nl(e12) {
  let t = Yi;
  return Yi = e12, t;
}
var Rf = 256;
var Pl = Rf - 1;
var Ll = 5;
var Af = 0;
var me = {};
function Of(e12, t, n) {
  let r;
  typeof n == "string" ? r = n.charCodeAt(0) || 0 : n.hasOwnProperty(Je) && (r = n[Je]), r == null && (r = n[Je] = Af++);
  let o = r & Pl, i = 1 << o;
  t.data[e12 + (o >> Ll)] |= i;
}
function Fl(e12, t) {
  let n = jl(e12, t);
  if (n !== -1)
    return n;
  let r = t[m];
  r.firstCreatePass && (e12.injectorIndex = t.length, zi(r.data, e12), zi(t, null), zi(r.blueprint, null));
  let o = ks(e12, t), i = e12.injectorIndex;
  if (kl(o)) {
    let s = xr(o), a = Rr(o, t), c = a[m].data;
    for (let l = 0; l < 8; l++)
      t[i + l] = a[s + l] | c[s + l];
  }
  return t[i + 8] = o, i;
}
function zi(e12, t) {
  e12.push(0, 0, 0, 0, 0, 0, 0, 0, t);
}
function jl(e12, t) {
  return e12.injectorIndex === -1 || e12.parent && e12.parent.injectorIndex === e12.injectorIndex || t[e12.injectorIndex + 8] === null ? -1 : e12.injectorIndex;
}
function ks(e12, t) {
  if (e12.parent && e12.parent.injectorIndex !== -1)
    return e12.parent.injectorIndex;
  let n = 0, r = null, o = t;
  for (; o !== null; ) {
    if (r = Ul(o), r === null)
      return Lt;
    if (n++, o = o[nt], r.injectorIndex !== -1)
      return r.injectorIndex | n << 16;
  }
  return Lt;
}
function kf(e12, t, n) {
  Of(e12, t, n);
}
function Hl(e12, t, n) {
  if (n & 8 || e12 !== void 0)
    return e12;
  or(t, "NodeInjector");
}
function Vl(e12, t, n, r) {
  if (n & 8 && r === void 0 && (r = null), (n & 3) === 0) {
    let o = e12[be], i = G(void 0);
    try {
      return o ? o.get(t, r, n & 8) : hi(t, r, n & 8);
    } finally {
      G(i);
    }
  }
  return Hl(r, t, n);
}
function Bl(e12, t, n, r = 0, o) {
  if (e12 !== null) {
    if (t[y] & 2048 && !(r & 2)) {
      let s = jf(e12, t, n, r, me);
      if (s !== me)
        return s;
    }
    let i = $l(e12, t, n, r, me);
    if (i !== me)
      return i;
  }
  return Vl(t, n, r, o);
}
function $l(e12, t, n, r, o) {
  let i = Lf(n);
  if (typeof i == "function") {
    if (!Pi(t, e12, r))
      return r & 1 ? Hl(o, n, r) : Vl(t, n, r, o);
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
    let s = null, a = jl(e12, t), c = Lt, l = r & 1 ? t[ee][X] : null;
    for ((a === -1 || r & 4) && (c = a === -1 ? ks(e12, t) : t[a + 8], c === Lt || !ol(r, false) ? a = -1 : (s = t[m], a = xr(c), t = Rr(c, t))); a !== -1; ) {
      let u = t[m];
      if (rl(i, a, u.data)) {
        let d = Pf(a, t, n, s, r, l);
        if (d !== me)
          return d;
      }
      c = t[a + 8], c !== Lt && ol(r, t[m].data[a + 8] === l) && rl(i, a, t) ? (s = u, a = xr(c), t = Rr(c, t)) : a = -1;
    }
  }
  return o;
}
function Pf(e12, t, n, r, o, i) {
  let s = t[m], a = s.data[e12 + 8], c = r == null ? St(a) && Yi : r != s && (a.type & 3) !== 0, l = o & 1 && i === a, u = _r(a, s, n, c, l);
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
    if (p && Nt(p) && p.type === n)
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
    let c = nl(a.canSeeViewProviders);
    a.resolving = true;
    let l = s[n].type || s[n], u, d = a.injectImpl ? G(a.injectImpl) : null, f = Pi(e12, r, 0);
    try {
      i = e12[n] = a.factory(void 0, o, s, e12, r), t.firstCreatePass && n >= r.directiveStart && Tf(n, s[n], t);
    } finally {
      d !== null && G(d), nl(c), a.resolving = false, Li();
    }
  }
  return i;
}
function Lf(e12) {
  if (typeof e12 == "string")
    return e12.charCodeAt(0) || 0;
  let t = e12.hasOwnProperty(Je) ? e12[Je] : void 0;
  return typeof t == "number" ? t >= 0 ? t & Pl : Ff : t;
}
function rl(e12, t, n) {
  let r = 1 << e12;
  return !!(n[t + (e12 >> Ll)] & r);
}
function ol(e12, t) {
  return !(e12 & 2) && !(e12 & 1 && t);
}
var at = class {
  _tNode;
  _lView;
  constructor(t, n) {
    this._tNode = t, this._lView = n;
  }
  get(t, n, r) {
    return Bl(this._tNode, this._lView, t, Qe(r), n);
  }
};
function Ff() {
  return new at(ge(), M());
}
function jf(e12, t, n, r, o) {
  let i = e12, s = t;
  for (; i !== null && s !== null && s[y] & 2048 && !xt(s); ) {
    let a = $l(i, s, n, r | 2, me);
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
      c = Ul(s), s = s[nt];
    }
    i = c;
  }
  return o;
}
function Ul(e12) {
  let t = e12[m], n = t.type;
  return n === 2 ? t.declTNode : n === 1 ? e12[X] : null;
}
function Hf() {
  return Vt(ge(), M());
}
function Vt(e12, t) {
  return new yn(pe(e12, t));
}
var yn = /* @__PURE__ */ (() => {
  class e12 {
    nativeElement;
    constructor(n) {
      this.nativeElement = n;
    }
    static __NG_ELEMENT_ID__ = Hf;
  }
  return e12;
})();
function Vf(e12) {
  return e12 instanceof yn ? e12.nativeElement : e12;
}
function Bf() {
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
    let r = sc(t);
    (this._changesDetected = !ic(this._results, r, n)) && (this._results = r, this.length = r.length, this.last = r[this.length - 1], this.first = r[0]);
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
  [Symbol.iterator] = Bf;
};
function zl(e12) {
  return (e12.flags & 128) === 128;
}
var Ps = function(e12) {
  return e12[e12.OnPush = 0] = "OnPush", e12[e12.Eager = 1] = "Eager", e12[e12.Default = 1] = "Default", e12;
}(Ps || {});
var Wl = /* @__PURE__ */ new Map();
var $f = 0;
function Uf() {
  return $f++;
}
function zf(e12) {
  Wl.set(e12[Ce], e12);
}
function Ki(e12) {
  Wl.delete(e12[Ce]);
}
var il = "__ngContext__";
function Ft(e12, t) {
  Be(t) ? (e12[il] = t[Ce], zf(t)) : e12[il] = t;
}
function Gl(e12) {
  return Zl(e12[_t]);
}
function ql(e12) {
  return Zl(e12[J]);
}
function Zl(e12) {
  for (; e12 !== null && !oe(e12); )
    e12 = e12[J];
  return e12;
}
var Ji;
function Ls(e12) {
  Ji = e12;
}
function Ql() {
  if (Ji !== void 0)
    return Ji;
  if (typeof document < "u")
    return document;
  throw new v(210, false);
}
var Ur = new D("", { factory: () => Wf });
var Wf = "ng";
var zr = new D("");
var vn = new D("", { providedIn: "platform", factory: () => "unknown" });
var Wr = new D("", { factory: () => E(z).body?.querySelector("[ngCspNonce]")?.getAttribute("ngCspNonce") || null });
var Yl = "r";
var Kl = "di";
var Jl = false;
var Xl = new D("", { factory: () => Jl });
var sl = /* @__PURE__ */ new WeakMap();
function Gf(e12, t) {
  if (e12 == null || typeof e12 != "object")
    return;
  let n = sl.get(e12);
  n || (n = /* @__PURE__ */ new WeakSet(), sl.set(e12, n)), n.add(t);
}
var qf = (e12, t, n, r) => {
};
function Zf(e12, t, n, r) {
  qf(e12, t, n, r);
}
function Fs(e12) {
  return (e12.flags & 32) === 32;
}
var Qf = () => null;
function eu(e12, t, n = false) {
  return Qf(e12, t, n);
}
function tu(e12, t) {
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
function Yf(e12, t, n) {
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
function Kf() {
  if (Dr === void 0 && (Dr = null, Fe.trustedTypes))
    try {
      Dr = Fe.trustedTypes.createPolicy("angular", { createHTML: (e12) => e12, createScript: (e12) => e12, createScriptURL: (e12) => e12 });
    } catch {
    }
  return Dr;
}
function Gr(e12) {
  return Kf()?.createHTML(e12) || e12;
}
var br;
function Jf() {
  if (br === void 0 && (br = null, Fe.trustedTypes))
    try {
      br = Fe.trustedTypes.createPolicy("angular#unsafe-bypass", { createHTML: (e12) => e12, createScript: (e12) => e12, createScriptURL: (e12) => e12 });
    } catch {
    }
  return br;
}
function al(e12) {
  return Jf()?.createHTML(e12) || e12;
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
  let n = nu(e12);
  if (n != null && n !== t) {
    if (n === "ResourceURL" && t === "URL")
      return true;
    throw new Error(`Required a safe ${t}, got a ${n} (see ${Jn})`);
  }
  return n === t;
}
function nu(e12) {
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
function Xf(e12) {
  let t = new ss(e12);
  return ep() ? new is(t) : t;
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
function ep() {
  try {
    return !!new window.DOMParser().parseFromString(Gr(""), "text/html");
  } catch {
    return false;
  }
}
var tp = /^(?!javascript:)(?:[a-z0-9+.-]+:|[^&:\/?#]*(?:[\/?#]|$))/i;
function qr(e12) {
  return e12 = String(e12), e12.match(tp) ? e12 : "unsafe:" + e12;
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
var ru = xe("area,br,col,hr,img,wbr");
var ou = xe("colgroup,dd,dt,li,p,tbody,td,tfoot,th,thead,tr");
var iu = xe("rp,rt");
var np = En(iu, ou);
var rp = En(ou, xe("address,article,aside,blockquote,caption,center,del,details,dialog,dir,div,dl,figure,figcaption,footer,h1,h2,h3,h4,h5,h6,header,hgroup,hr,ins,main,map,menu,nav,ol,pre,section,summary,table,ul"));
var op = En(iu, xe("a,abbr,acronym,audio,b,bdi,bdo,big,br,cite,code,del,dfn,em,font,i,img,ins,kbd,label,map,mark,picture,q,ruby,rp,rt,s,samp,small,source,span,strike,strong,sub,sup,time,track,tt,u,var,video"));
var cl = En(ru, rp, op, np);
var su = xe("background,cite,href,itemtype,longdesc,poster,src,xlink:href");
var ip = xe("abbr,accesskey,align,alt,autoplay,axis,bgcolor,border,cellpadding,cellspacing,class,clear,color,cols,colspan,compact,controls,coords,datetime,default,dir,download,face,headers,height,hidden,hreflang,hspace,ismap,itemscope,itemprop,kind,label,lang,language,loop,media,muted,nohref,nowrap,open,preload,rel,rev,role,rows,rowspan,rules,scope,scrolling,shape,size,sizes,span,srclang,srcset,start,summary,tabindex,target,title,translate,type,usemap,valign,value,vspace,width");
var sp = xe("aria-activedescendant,aria-atomic,aria-autocomplete,aria-busy,aria-checked,aria-colcount,aria-colindex,aria-colspan,aria-controls,aria-current,aria-describedby,aria-details,aria-disabled,aria-dropeffect,aria-errormessage,aria-expanded,aria-flowto,aria-grabbed,aria-haspopup,aria-hidden,aria-invalid,aria-keyshortcuts,aria-label,aria-labelledby,aria-level,aria-live,aria-modal,aria-multiline,aria-multiselectable,aria-orientation,aria-owns,aria-placeholder,aria-posinset,aria-pressed,aria-readonly,aria-relevant,aria-required,aria-roledescription,aria-rowcount,aria-rowindex,aria-rowspan,aria-selected,aria-setsize,aria-sort,aria-valuemax,aria-valuemin,aria-valuenow,aria-valuetext");
var ap = En(su, ip, sp);
var cp = xe("script,style,template");
var as = class {
  sanitizedSomething = false;
  buf = [];
  sanitizeChildren(t) {
    let n = t.firstChild, r = true, o = [];
    for (; n; ) {
      if (n.nodeType === Node.ELEMENT_NODE ? r = this.startElement(n) : n.nodeType === Node.TEXT_NODE ? this.chars(n.nodeValue) : this.sanitizedSomething = true, r && n.firstChild) {
        o.push(n), n = dp(n);
        continue;
      }
      for (; n; ) {
        n.nodeType === Node.ELEMENT_NODE && this.endElement(n);
        let i = up(n);
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
    let n = ll(t).toLowerCase();
    if (!cl.hasOwnProperty(n))
      return this.sanitizedSomething = true, !cp.hasOwnProperty(n);
    this.buf.push("<"), this.buf.push(n);
    let r = t.attributes;
    for (let o = 0; o < r.length; o++) {
      let i = r.item(o), s = i.name, a = s.toLowerCase();
      if (!ap.hasOwnProperty(a)) {
        this.sanitizedSomething = true;
        continue;
      }
      let c = i.value;
      su[a] && (c = qr(c)), this.buf.push(" ", s, '="', ul(c), '"');
    }
    return this.buf.push(">"), true;
  }
  endElement(t) {
    let n = ll(t).toLowerCase();
    cl.hasOwnProperty(n) && !ru.hasOwnProperty(n) && (this.buf.push("</"), this.buf.push(n), this.buf.push(">"));
  }
  chars(t) {
    this.buf.push(ul(t));
  }
};
function lp(e12, t) {
  return (e12.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_CONTAINED_BY) !== Node.DOCUMENT_POSITION_CONTAINED_BY;
}
function up(e12) {
  let t = e12.nextSibling;
  if (t && e12 !== t.previousSibling)
    throw au(t);
  return t;
}
function dp(e12) {
  let t = e12.firstChild;
  if (t && lp(e12, t))
    throw au(t);
  return t;
}
function ll(e12) {
  let t = e12.nodeName;
  return typeof t == "string" ? t : "FORM";
}
function au(e12) {
  return new Error(`Failed to sanitize html because the element is clobbered: ${e12.outerHTML}`);
}
var fp = /[\uD800-\uDBFF][\uDC00-\uDFFF]/g;
var pp = /([^\#-~ |!])/g;
function ul(e12) {
  return e12.replace(/&/g, "&amp;").replace(fp, function(t) {
    let n = t.charCodeAt(0), r = t.charCodeAt(1);
    return "&#" + ((n - 55296) * 1024 + (r - 56320) + 65536) + ";";
  }).replace(pp, function(t) {
    return "&#" + t.charCodeAt(0) + ";";
  }).replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
var Cr;
function Zr(e12, t) {
  let n = null;
  try {
    Cr = Cr || Xf(e12);
    let r = t ? String(t) : "";
    n = Cr.getInertBodyElement(r);
    let o = 5, i = r;
    do {
      if (o === 0)
        throw new Error("Failed to sanitize html because the input is unstable");
      o--, r = i, i = n.innerHTML, n = Cr.getInertBodyElement(r);
    } while (r !== i);
    let a = new as().sanitizeChildren(dl(n) || n);
    return Gr(a);
  } finally {
    if (n) {
      let r = dl(n) || n;
      for (; r.firstChild; )
        r.firstChild.remove();
    }
  }
}
function dl(e12) {
  return "content" in e12 && hp(e12) ? e12.content : null;
}
function hp(e12) {
  return e12.nodeType === Node.ELEMENT_NODE && e12.nodeName === "TEMPLATE";
}
function gp(e12, t) {
  return e12.createText(t);
}
function mp(e12, t, n) {
  e12.setValue(t, n);
}
function cu(e12, t, n) {
  return e12.createElement(t, n);
}
function kr(e12, t, n, r, o) {
  e12.insertBefore(t, n, r, o);
}
function lu(e12, t, n) {
  e12.appendChild(t, n);
}
function fl(e12, t, n, r, o) {
  r !== null ? kr(e12, t, n, r, o) : lu(e12, t, n);
}
function uu(e12, t, n, r) {
  e12.removeChild(null, t, n, r);
}
function yp(e12, t, n) {
  e12.setAttribute(t, "style", n);
}
function vp(e12, t, n) {
  n === "" ? e12.removeAttribute(t, "class") : e12.setAttribute(t, "class", n);
}
function du(e12, t, n) {
  let { mergedAttrs: r, classes: o, styles: i } = n;
  r !== null && Sf(e12, t, r), o !== null && vp(e12, t, o), i !== null && yp(e12, t, i);
}
var ye = function(e12) {
  return e12[e12.NONE = 0] = "NONE", e12[e12.HTML = 1] = "HTML", e12[e12.STYLE = 2] = "STYLE", e12[e12.SCRIPT = 3] = "SCRIPT", e12[e12.URL = 4] = "URL", e12[e12.RESOURCE_URL = 5] = "RESOURCE_URL", e12;
}(ye || {});
function Us(e12) {
  let t = Ep();
  return t ? al(t.sanitize(ye.HTML, e12) || "") : ze(e12, "HTML") ? al(Ne(e12)) : Zr(Ql(), fi(e12));
}
function Ep() {
  let e12 = M();
  return e12 && e12[de].sanitizer;
}
var Ip = "ng-template";
function Dp(e12) {
  return e12.type === 4 && e12.value !== Ip;
}
function cs(e12) {
  return (e12 & 1) === 0;
}
function pl(e12, t) {
  return e12 ? ":not(" + t.trim() + ")" : t;
}
function bp(e12) {
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
      o !== "" && !cs(s) && (t += pl(i, o), o = ""), r = s, i = i || !cs(r);
    n++;
  }
  return o !== "" && (t += pl(i, o)), t;
}
function Cp(e12) {
  return e12.map(bp).join(",");
}
function wp(e12) {
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
  let d = B + r, f = d + o, p = Tp(d, f), h = typeof l == "function" ? l() : l;
  return p[m] = { type: e12, blueprint: p, template: n, queries: null, viewQuery: a, declTNode: t, data: p.slice().fill(null, d), bindingStartIndex: d, expandoStartIndex: f, hostBindingOpCodes: null, firstCreatePass: true, firstUpdatePass: true, staticViewQueries: false, staticContentQueries: false, preOrderHooks: null, preOrderCheckHooks: null, contentHooks: null, contentCheckHooks: null, viewHooks: null, viewCheckHooks: null, destroyHooks: null, cleanup: null, contentQueries: null, components: null, directiveRegistry: typeof i == "function" ? i() : i, pipeRegistry: typeof s == "function" ? s() : s, firstChild: null, schemas: c, consts: h, incompleteFirstPass: false, ssrId: u };
}
function Tp(e12, t) {
  let n = [];
  for (let r = 0; r < t; r++)
    n.push(r < e12 ? null : Re);
  return n;
}
function Mp(e12) {
  let t = e12.tView;
  return t === null || t.incompleteFirstPass ? e12.tView = zs(1, null, e12.template, e12.decls, e12.vars, e12.directiveDefs, e12.pipeDefs, e12.viewQuery, e12.schemas, e12.consts, e12.id) : t;
}
function Ws(e12, t, n, r, o, i, s, a, c, l, u) {
  let d = t.blueprint.slice();
  return d[re] = o, d[y] = r | 4 | 128 | 8 | 64 | 1024, (l !== null || e12 && e12[y] & 2048) && (d[y] |= 2048), Mi(d), d[A] = d[nt] = e12, d[N] = n, d[de] = s || e12 && e12[de], d[O] = a || e12 && e12[O], d[be] = c || e12 && e12[be] || null, d[X] = i, d[Ce] = Uf(), d[Tt] = u, d[Di] = l, d[ee] = t.type == 2 ? e12[ee] : d, d;
}
function _p(e12, t, n) {
  let r = pe(t, e12), o = Mp(n), i = e12[de].rendererFactory, s = Gs(e12, Ws(e12, o, null, fu(n), r, t, null, i.createRenderer(r, n), null, null, null));
  return e12[t.index] = s;
}
function fu(e12) {
  let t = 16;
  return e12.signals ? t = 4096 : e12.onPush && (t = 64), t;
}
function pu(e12, t, n, r) {
  if (n === 0)
    return -1;
  let o = t.length;
  for (let i = 0; i < n; i++)
    t.push(r), e12.blueprint.push(r), e12.data.push(null);
  return o;
}
function Gs(e12, t) {
  return e12[_t] ? e12[Ii][J] = t : e12[_t] = t, e12[Ii] = t, t;
}
function F(e12 = 1) {
  hu(ie(), M(), $e() + e12, false);
}
function hu(e12, t, n, r) {
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
    (s & Qr.SignalBased) !== 0 && (c = t[i][Q]), c !== null && c.transformFn !== void 0 ? r = c.transformFn(r) : a !== null && (r = a.call(t, r)), e12.setInput !== null ? e12.setInput(t, c, r, n, i) : xl(t, c, i, r);
  } finally {
    g(o);
  }
}
var Se = function(e12) {
  return e12[e12.Important = 1] = "Important", e12[e12.DashCase = 2] = "DashCase", e12;
}(Se || {});
var Sp;
function qs(e12, t) {
  return Sp(e12, t);
}
var YE = typeof document < "u" && typeof document?.documentElement?.getAnimations == "function";
var us = /* @__PURE__ */ new WeakMap();
var sn = /* @__PURE__ */ new WeakSet();
function Np(e12, t) {
  let n = us.get(e12);
  if (!n || n.length === 0)
    return;
  let r = t.parentNode, o = t.previousSibling;
  for (let i = n.length - 1; i >= 0; i--) {
    let s = n[i], a = s.parentNode;
    s === t ? (n.splice(i, 1), sn.add(s), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } }))) : (o && s === o || a && r && a !== r) && (n.splice(i, 1), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } })), s.parentNode?.removeChild(s));
  }
}
function xp(e12, t) {
  let n = us.get(e12);
  n ? n.includes(t) || n.push(t) : us.set(e12, [t]);
}
var ct = /* @__PURE__ */ new Set();
var Zs = function(e12) {
  return e12[e12.CHANGE_DETECTION = 0] = "CHANGE_DETECTION", e12[e12.AFTER_NEXT_RENDER = 1] = "AFTER_NEXT_RENDER", e12;
}(Zs || {});
var Bt = new D("");
var hl = /* @__PURE__ */ new Set();
function dt(e12) {
  hl.has(e12) || (hl.add(e12), performance?.mark?.("mark_feature_usage", { detail: { feature: e12 } }));
}
var gu = (() => {
  class e12 {
    impl = null;
    execute() {
      this.impl?.execute();
    }
    static \u0275prov = _({ token: e12, providedIn: "root", factory: () => new e12() });
  }
  return e12;
})();
var mu = new D("", { factory: () => ({ queue: /* @__PURE__ */ new Set(), isScheduled: false, scheduler: null, injector: E(Y) }) });
function yu(e12, t, n) {
  let r = e12.get(mu);
  if (Array.isArray(t))
    for (let o of t)
      r.queue.add(o), n?.detachedLeaveAnimationFns?.push(o);
  else
    r.queue.add(t), n?.detachedLeaveAnimationFns?.push(t);
  r.scheduler && r.scheduler(e12);
}
function Rp(e12, t) {
  let n = e12.get(mu);
  if (t.detachedLeaveAnimationFns) {
    for (let r of t.detachedLeaveAnimationFns)
      n.queue.delete(r);
    t.detachedLeaveAnimationFns = void 0;
  }
}
function Ap(e12, t) {
  for (let [n, r] of t)
    yu(e12, r.animateFns);
}
function gl(e12, t, n, r) {
  let o = e12?.[He]?.enter;
  t !== null && o && o.has(n.index) && Ap(r, o);
}
function Pt(e12, t, n, r, o, i, s, a) {
  if (o != null) {
    let c, l = false;
    oe(o) ? c = o : Be(o) && (l = true, o = o[re]);
    let u = te(o);
    e12 === 0 && r !== null ? (gl(a, r, i, n), s == null ? lu(t, r, u) : kr(t, r, u, s || null, true)) : e12 === 1 && r !== null ? (gl(a, r, i, n), kr(t, r, u, s || null, true), Np(i, u)) : e12 === 2 ? (a?.[He]?.leave?.has(i.index) && xp(i, u), sn.delete(u), ml(a, i, n, (d) => {
      if (sn.has(u)) {
        sn.delete(u);
        return;
      }
      uu(t, u, l, d);
    })) : e12 === 3 && (sn.delete(u), ml(a, i, n, () => {
      t.destroyNode(u);
    })), c != null && Wp(t, e12, n, c, i, r, s);
  }
}
function Op(e12, t) {
  vu(e12, t), t[re] = null, t[X] = null;
}
function kp(e12, t, n, r, o, i) {
  r[re] = o, r[X] = t, Kr(e12, r, n, 1, o, i);
}
function vu(e12, t) {
  t[de].changeDetectionScheduler?.notify(9), Kr(e12, t, t[O], 2, null, null);
}
function Pp(e12) {
  let t = e12[_t];
  if (!t)
    return Wi(e12[m], e12);
  for (; t; ) {
    let n = null;
    if (Be(t))
      n = t[_t];
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
  n.destroyNode && Kr(e12, t, n, 3, null, null), Pp(t);
}
function Wi(e12, t) {
  if (it(t))
    return;
  let n = g(null);
  try {
    t[y] &= -129, t[y] |= 256, t[Z] && ht(t[Z]), jp(e12, t), Fp(e12, t), t[m].type === 1 && t[O].destroy();
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
function ml(e12, t, n, r) {
  let o = e12?.[He];
  if (o == null || o.leave == null || !o.leave.has(t.index))
    return r(false);
  e12 && ct.add(e12[Ce]), yu(n, () => {
    if (o.leave && o.leave.has(t.index)) {
      let s = o.leave.get(t.index), a = [];
      if (s) {
        for (let c = 0; c < s.animateFns.length; c++) {
          let l = s.animateFns[c], { promise: u } = l();
          a.push(u);
        }
        o.detachedLeaveAnimationFns = void 0;
      }
      o.running = Promise.allSettled(a), Lp(e12, r);
    } else
      e12 && ct.delete(e12[Ce]), r(false);
  }, o);
}
function Lp(e12, t) {
  let n = e12[He]?.running;
  if (n) {
    n.then(() => {
      e12[He].running = void 0, ct.delete(e12[Ce]), t(true);
    });
    return;
  }
  t(false);
}
function Fp(e12, t) {
  let n = e12.cleanup, r = t[Mt];
  if (n !== null)
    for (let s = 0; s < n.length - 1; s += 2)
      if (typeof n[s] == "string") {
        let a = n[s + 3];
        a >= 0 ? r[a]() : r[-a].unsubscribe(), s += 2;
      } else {
        let a = r[n[s + 1]];
        n[s].call(a);
      }
  r !== null && (t[Mt] = null);
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
function jp(e12, t) {
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
function Hp(e12, t, n) {
  return Vp(e12, t.parent, n);
}
function Vp(e12, t, n) {
  let r = t;
  for (; r !== null && r.type & 168; )
    t = r, r = t.parent;
  if (r === null)
    return n[re];
  if (St(r)) {
    let { encapsulation: o } = e12.data[r.directiveStart + r.componentOffset];
    if (o === se.None || o === se.Emulated)
      return null;
  }
  return pe(r, n);
}
function Bp(e12, t, n) {
  return Up(e12, t, n);
}
function $p(e12, t, n) {
  return e12.type & 40 ? pe(e12, n) : null;
}
var Up = $p;
var yl;
function Ys(e12, t, n, r) {
  let o = Hp(e12, r, t), i = t[O], s = r.parent || t[X], a = Bp(s, r, t);
  if (o != null)
    if (Array.isArray(n))
      for (let c = 0; c < n.length; c++)
        fl(i, o, n[c], a, false);
    else
      fl(i, o, n, a, false);
  yl !== void 0 && yl(i, r, t, n, o);
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
        let r = Eu(e12, t);
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
function Eu(e12, t) {
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
    if (s && t === 0 && (c && Ft(te(c), r), n.flags |= 2), !Fs(n))
      if (l & 8)
        Ks(e12, t, n.child, r, o, i, false), Pt(t, e12, a, o, c, n, i, r);
      else if (l & 32) {
        let u = qs(n, r), d;
        for (; d = u(); )
          Pt(t, e12, a, o, d, n, i, r);
        Pt(t, e12, a, o, c, n, i, r);
      } else
        l & 16 ? zp(e12, t, r, n, o, i) : Pt(t, e12, a, o, c, n, i, r);
    n = s ? n.projectionNext : n.next;
  }
}
function Kr(e12, t, n, r, o, i) {
  Ks(n, r, e12.firstChild, t, o, i, false);
}
function zp(e12, t, n, r, o, i) {
  let s = n[ee], c = s[X].projection[r.projection];
  if (Array.isArray(c))
    for (let l = 0; l < c.length; l++) {
      let u = c[l];
      Pt(t, e12, n[be], o, u, r, i, n);
    }
  else {
    let l = c, u = s[A];
    zl(r) && (l.flags |= 128), Ks(e12, t, l, u, o, i, true);
  }
}
function Wp(e12, t, n, r, o, i, s) {
  let a = r[Ve], c = te(r);
  a !== c && Pt(t, e12, n, i, a, o, s);
  for (let l = S; l < r.length; l++) {
    let u = r[l];
    Kr(u[m], u, e12, t, i, a);
  }
}
function Gp(e12, t, n, r, o) {
  if (t)
    o ? e12.addClass(n, r) : e12.removeClass(n, r);
  else {
    let i = r.indexOf("-") === -1 ? void 0 : Se.DashCase;
    o == null ? e12.removeStyle(n, r, i) : (typeof o == "string" && o.endsWith("!important") && (o = o.slice(0, -10), i |= Se.Important), e12.setStyle(n, r, o, i));
  }
}
function Iu(e12, t, n, r, o) {
  let i = $e(), s = r & 2;
  try {
    Ue(-1), s && t.length > B && hu(e12, t, B, false);
    let a = s ? C.TemplateUpdateStart : C.TemplateCreateStart;
    T(a, o, n), n(r, o);
  } finally {
    Ue(i);
    let a = s ? C.TemplateUpdateEnd : C.TemplateCreateEnd;
    T(a, o, n);
  }
}
function qp(e12, t, n) {
  Jp(e12, t, n), (n.flags & 64) === 64 && Xp(e12, t, n);
}
function Du(e12, t, n = pe) {
  let r = t.localNames;
  if (r !== null) {
    let o = t.index + 1;
    for (let i = 0; i < r.length; i += 2) {
      let s = r[i + 1], a = s === -1 ? n(t, e12) : e12[s];
      e12[o++] = a;
    }
  }
}
function Zp(e12, t, n, r) {
  let i = r.get(Xl, Jl) || n === se.ShadowDom || n === se.ExperimentalIsolatedShadowDom, s = e12.selectRootElement(t, i);
  return Qp(s), s;
}
function Qp(e12) {
  Yp(e12);
}
var Yp = () => null;
function Kp(e12, t, n, r, o, i) {
  if (e12.type & 3) {
    let s = pe(e12, t);
    r = i != null ? i(r, e12.value || "", n) : r, o.setProperty(s, n, r);
  } else
    e12.type & 12;
}
function Jp(e12, t, n) {
  let r = n.directiveStart, o = n.directiveEnd;
  St(n) && _p(t, n, e12.data[r + n.componentOffset]), e12.firstCreatePass || Fl(n, t);
  let i = n.initialInputs;
  for (let s = r; s < o; s++) {
    let a = e12.data[s], c = Ar(t, e12, s, n);
    if (Ft(c, t), i !== null && th(t, s - r, c, a, n, i), Nt(a)) {
      let l = we(n.index, t);
      l[N] = Ar(t, e12, s, n);
    }
  }
}
function Xp(e12, t, n) {
  let r = n.directiveStart, o = n.directiveEnd, i = n.index, s = Pc();
  try {
    Ue(i);
    for (let a = r; a < o; a++) {
      let c = e12.data[a], l = t[a];
      pr(a), (c.hostBindings !== null || c.hostVars !== 0 || c.hostAttrs !== null) && eh(c, l);
    }
  } finally {
    Ue(-1), pr(s);
  }
}
function eh(e12, t) {
  e12.hostBindings !== null && e12.hostBindings(1, t);
}
function th(e12, t, n, r, o, i) {
  let s = i[t];
  if (s !== null)
    for (let a = 0; a < s.length; a += 2) {
      let c = s[a], l = s[a + 1];
      ls(r, n, c, l);
    }
}
function nh(e12, t, n, r, o) {
  let i = B + n, s = t[m], a = o(s, t, e12, r, n);
  t[i] = a, At(e12, true);
  let c = e12.type === 2;
  return c ? (du(t[O], a, e12), (Cc() === 0 || wi(e12)) && Ft(a, t), wc()) : Ft(a, t), yr() && (!c || !Fs(e12)) && Ys(s, t, a, e12), e12;
}
function rh(e12) {
  let t = e12;
  return Ai() ? xc() : (t = t.parent, At(t, false)), t;
}
function oh(e12, t) {
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
function ih(e12, t, n, r, o) {
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
function sh(e12, t) {
  let n = we(t, e12), r = n[m];
  ah(r, n);
  let o = n[re];
  o !== null && n[Tt] === null && (n[Tt] = eu(o, n[be])), T(C.ComponentStart);
  try {
    Js(r, n, n[N]);
  } finally {
    T(C.ComponentEnd, n[N]);
  }
}
function ah(e12, t) {
  for (let n = t.length; n < e12.blueprint.length; n++)
    t.push(e12.blueprint[n]);
}
function Js(e12, t, n) {
  gr(t);
  try {
    let r = e12.viewQuery;
    r !== null && Xi(1, r, n);
    let o = e12.template;
    o !== null && Iu(e12, t, o, 1, n), e12.firstCreatePass && (e12.firstCreatePass = false), t[fe]?.finishViewCreation(e12), e12.staticContentQueries && tu(e12, t), e12.staticViewQueries && Xi(2, e12.viewQuery, n);
    let i = e12.components;
    i !== null && ch(t, i);
  } catch (r) {
    throw e12.firstCreatePass && (e12.incompleteFirstPass = true, e12.firstCreatePass = false), r;
  } finally {
    t[y] &= -5, mr();
  }
}
function ch(e12, t) {
  for (let n = 0; n < t.length; n++)
    sh(e12, t[n]);
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
  return !t || t.firstChild === null || zl(e12);
}
function dn(e12, t, n, r, o = false) {
  for (; n !== null; ) {
    if (n.type === 128) {
      n = o ? n.projectionNext : n.next;
      continue;
    }
    let i = t[n.index];
    i !== null && r.push(te(i)), oe(i) && bu(i, r);
    let s = n.type;
    if (s & 8)
      dn(e12, t, n.child, r);
    else if (s & 32) {
      let a = qs(n, t), c;
      for (; c = a(); )
        r.push(c);
    } else if (s & 16) {
      let a = Eu(t, n);
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
function bu(e12, t) {
  for (let n = S; n < e12.length; n++) {
    let r = e12[n], o = r[m].firstChild;
    o !== null && dn(r[m], r, o, t);
  }
  e12[Ve] !== e12[re] && t.push(e12[Ve]);
}
function Cu(e12) {
  if (e12[lr] !== null) {
    for (let t of e12[lr])
      t.impl.addSequence(t);
    e12[lr].length = 0;
  }
}
var wu = [];
function lh(e12) {
  return e12[Z] ?? uh(e12);
}
function uh(e12) {
  let t = wu.pop() ?? Object.create(fh);
  return t.lView = e12, t;
}
function dh(e12) {
  e12.lView[Z] !== e12 && (e12.lView = null, wu.push(e12));
}
var fh = R(x({}, pt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e12) => {
  Rt(e12.lView);
}, consumerOnSignalRead() {
  this.lView[Z] = this;
} });
function ph(e12) {
  let t = e12[Z] ?? Object.create(hh);
  return t.lView = e12, t;
}
var hh = R(x({}, pt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e12) => {
  let t = Le(e12.lView);
  for (; t && !Tu(t[m]); )
    t = Le(t);
  t && _i(t);
}, consumerOnSignalRead() {
  this.lView[Z] = this;
} });
function Tu(e12) {
  return e12.type !== 2;
}
function Mu(e12) {
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
var gh = 100;
function _u(e12, t = 0) {
  let r = e12[de].rendererFactory, o = false;
  o || r.begin?.();
  try {
    mh(e12, t);
  } finally {
    o || r.end?.();
  }
}
function mh(e12, t) {
  let n = Oi();
  try {
    Qt(true), fs(e12, t);
    let r = 0;
    for (; nn(e12); ) {
      if (r === gh)
        throw new v(103, false);
      r++, fs(e12, 1);
    }
  } finally {
    Qt(n);
  }
}
function yh(e12, t, n, r) {
  if (it(t))
    return;
  let o = t[y], i = false, s = false;
  gr(t);
  let a = true, c = null, l = null;
  i || (Tu(e12) ? (l = lh(t), c = zt(l)) : Pn() === null ? (a = false, l = ph(t), c = zt(l)) : t[Z] && (ht(t[Z]), t[Z] = null));
  try {
    Mi(t), Rc(e12.bindingStartIndex), n !== null && Iu(e12, t, n, 2, r);
    let u = (o & 3) === 3;
    if (!i)
      if (u) {
        let p = e12.preOrderCheckHooks;
        p !== null && Tr(t, p, null);
      } else {
        let p = e12.preOrderHooks;
        p !== null && Mr(t, p, 0, null), Ui(t, 0);
      }
    if (s || vh(t), Mu(t), Su(t, 0), e12.contentQueries !== null && tu(e12, t), !i)
      if (u) {
        let p = e12.contentCheckHooks;
        p !== null && Tr(t, p);
      } else {
        let p = e12.contentHooks;
        p !== null && Mr(t, p, 1), Ui(t, 1);
      }
    Ih(e12, t);
    let d = e12.components;
    d !== null && xu(t, d, 0);
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
    i || (Cu(t), t[y] &= -73);
  } catch (u) {
    throw i || Rt(t), u;
  } finally {
    l !== null && (Ln(l, c), a && dh(l)), mr();
  }
}
function Su(e12, t) {
  for (let n = Gl(e12); n !== null; n = ql(n))
    for (let r = S; r < n.length; r++) {
      let o = n[r];
      Nu(o, t);
    }
}
function vh(e12) {
  for (let t = Gl(e12); t !== null; t = ql(t)) {
    if (!(t[y] & 2))
      continue;
    let n = t[ot];
    for (let r = 0; r < n.length; r++) {
      let o = n[r];
      _i(o);
    }
  }
}
function Eh(e12, t, n) {
  T(C.ComponentStart);
  let r = we(t, e12);
  try {
    Nu(r, n);
  } finally {
    T(C.ComponentEnd, r[N]);
  }
}
function Nu(e12, t) {
  dr(e12) && fs(e12, t);
}
function fs(e12, t) {
  let r = e12[m], o = e12[y], i = e12[Z], s = !!(t === 0 && o & 16);
  if (s ||= !!(o & 64 && t === 0), s ||= !!(o & 1024), s ||= !!(i?.dirty && Fn(i)), s ||= false, i && (i.dirty = false), e12[y] &= -9217, s)
    yh(r, e12, r.template, e12[N]);
  else if (o & 8192) {
    let a = g(null);
    try {
      Mu(e12), Su(e12, 1);
      let c = r.components;
      c !== null && xu(e12, c, 1), Cu(e12);
    } finally {
      g(a);
    }
  }
}
function xu(e12, t, n) {
  for (let r = 0; r < t.length; r++)
    Eh(e12, t[r], n);
}
function Ih(e12, t) {
  let n = e12.hostBindingOpCodes;
  if (n !== null)
    try {
      for (let r = 0; r < n.length; r++) {
        let o = n[r];
        if (o < 0)
          Ue(~o);
        else {
          let i = o, s = n[++r], a = n[++r];
          kc(s, i);
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
    if (xt(e12) && !r)
      return e12;
    e12 = r;
  }
  return null;
}
function Ru(e12, t, n, r) {
  return [e12, true, 0, t, null, r, null, n, null, null];
}
function Au(e12, t) {
  let n = S + t;
  if (n < e12.length)
    return e12[n];
}
function Xr(e12, t, n, r = true) {
  let o = t[m];
  if (Dh(o, t, e12, n), r) {
    let s = ds(n, e12), a = t[O], c = a.parentNode(e12[Ve]);
    c !== null && kp(o, e12[X], a, t, c, s);
  }
  let i = t[Tt];
  i !== null && i.firstChild !== null && (i.firstChild = null);
}
function Ou(e12, t) {
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
    let i = Jt(e12, S + t);
    Op(r[m], r);
    let s = i[fe];
    s !== null && s.detachView(i[m]), r[A] = null, r[J] = null, r[y] &= -129;
  }
  return r;
}
function Dh(e12, t, n, r) {
  let o = S + r, i = n.length;
  r > 0 && (n[o - 1][J] = t), r < i - S ? (t[J] = n[o], gi(n, S + r, t)) : (n.push(t), t[J] = null), t[A] = n;
  let s = t[je];
  s !== null && n !== s && ku(s, t);
  let a = t[fe];
  a !== null && a.insertView(e12), fr(t), t[y] |= 128;
}
function ku(e12, t) {
  let n = e12[ot], r = t[A];
  if (Be(r))
    e12[y] |= 2;
  else {
    let o = r[A][ee];
    t[ee] !== o && (e12[y] |= 2);
  }
  n === null ? e12[ot] = [t] : n.push(t);
}
var jt = class {
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
    return this._lView[N];
  }
  set context(t) {
    this._lView[N] = t;
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
        r > -1 && (fn(t, r), Jt(n, r));
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
    this._lView[y] |= 1024, _u(this._lView);
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
    let t = xt(this._lView), n = this._lView[je];
    n !== null && !t && Qs(n, this._lView), vu(this._lView[m], this._lView);
  }
  attachToAppRef(t) {
    if (this._attachedToViewContainer)
      throw new v(902, false);
    this._appRef = t;
    let n = xt(this._lView), r = this._lView[je];
    r !== null && !n && ku(r, this._lView), fr(this._lView);
  }
};
var pn = /* @__PURE__ */ (() => {
  class e12 {
    _declarationLView;
    _declarationTContainer;
    elementRef;
    static __NG_ELEMENT_ID__ = bh;
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
      return new jt(i);
    }
  }
  return e12;
})();
function bh() {
  return ea(ge(), M());
}
function ea(e12, t) {
  return e12.type & 4 ? new pn(t, e12, Vt(e12, t)) : null;
}
function eo(e12, t, n, r, o) {
  let i = e12.data[t];
  if (i === null)
    i = Ch(e12, t, n, r, o), Oc() && (i.flags |= 32);
  else if (i.type & 64) {
    i.type = n, i.value = r, i.attrs = o;
    let s = Nc();
    i.injectorIndex = s === null ? -1 : s.injectorIndex;
  }
  return At(i, true), i;
}
function Ch(e12, t, n, r, o) {
  let i = Ri(), s = Ai(), a = s ? i : i && i.parent, c = e12.data[t] = Th(e12, a, n, t, r, o);
  return wh(e12, c, i, s), c;
}
function wh(e12, t, n, r) {
  e12.firstChild === null && (e12.firstChild = t), n !== null && (r ? n.child == null && t.parent !== null && (n.child = t) : n.next === null && (n.next = t, t.prev = n));
}
function Th(e12, t, n, r, o, i) {
  let s = t ? t.injectorIndex : -1, a = 0;
  return Mc() && (a |= 128), { type: n, index: r, insertBeforeIndex: null, injectorIndex: s, directiveStart: -1, directiveEnd: -1, directiveStylingLast: -1, componentOffset: -1, controlDirectiveIndex: -1, customControlIndex: -1, propertyBindings: null, flags: a, providerIndexes: 0, value: o, attrs: i, mergedAttrs: null, localNames: null, initialInputs: null, inputs: null, hostDirectiveInputs: null, outputs: null, hostDirectiveOutputs: null, directiveToIndex: null, tView: null, next: null, prev: null, projectionNext: null, child: null, parent: t, projection: null, styles: null, stylesWithoutHost: null, residualStyles: void 0, classes: null, classesWithoutHost: null, residualClasses: void 0, classBindings: 0, styleBindings: 0 };
}
function Mh(e12) {
  let t = e12[bi] ?? [], r = e12[A][O], o = [];
  for (let i of t)
    i.data[Kl] !== void 0 ? o.push(i) : _h(i, r);
  e12[bi] = o;
}
function _h(e12, t) {
  let n = 0, r = e12.firstChild;
  if (r) {
    let o = e12.data[Yl];
    for (; n < o; ) {
      let i = r.nextSibling;
      uu(t, r, false), r = i, n++;
    }
  }
}
var Sh = () => null;
var Nh = () => null;
function ps(e12, t) {
  return Sh(e12, t);
}
function Pu(e12, t, n) {
  return Nh(e12, t, n);
}
var Lu = class {
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
var Fu = (() => {
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
function ju(e12, t = 0) {
  let n = M();
  if (n === null)
    return b(e12, t);
  let r = ge();
  return Bl(r, n, q(e12), t);
}
function xh(e12, t, n, r, o) {
  let i = r === null ? null : { "": -1 }, s = o(e12, n);
  if (s !== null) {
    let a = s, c = null, l = null;
    for (let u of s)
      if (u.resolveHostDirectives !== null) {
        [a, c, l] = u.resolveHostDirectives(s);
        break;
      }
    Oh(e12, t, n, a, i, c, l);
  }
  i !== null && r !== null && Rh(n, r, i);
}
function Rh(e12, t, n) {
  let r = e12.localNames = [];
  for (let o = 0; o < t.length; o += 2) {
    let i = n[t[o + 1]];
    if (i == null)
      throw new v(-301, false);
    r.push(t[o], i);
  }
}
function Ah(e12, t, n) {
  t.componentOffset = n, (e12.components ??= []).push(t.index);
}
function Oh(e12, t, n, r, o, i, s) {
  let a = r.length, c = null;
  for (let f = 0; f < a; f++) {
    let p = r[f];
    c === null && Nt(p) && (c = p, Ah(e12, n, f)), kf(Fl(n, t), e12, p.type);
  }
  Hh(n, e12.data.length, a), c?.viewProvidersResolver && c.viewProvidersResolver(c);
  for (let f = 0; f < a; f++) {
    let p = r[f];
    p.providersResolver && p.providersResolver(p);
  }
  let l = false, u = false, d = pu(e12, t, a, null);
  a > 0 && (n.directiveToIndex = /* @__PURE__ */ new Map());
  for (let f = 0; f < a; f++) {
    let p = r[f];
    if (n.mergedAttrs = $r(n.mergedAttrs, p.hostAttrs), Ph(e12, n, t, d, p), jh(d, p, o), s !== null && s.has(p)) {
      let [L, H] = s.get(p);
      n.directiveToIndex.set(p.type, [d, L + n.directiveStart, H + n.directiveStart]);
    } else
      (i === null || !i.has(p)) && n.directiveToIndex.set(p.type, d);
    p.contentQueries !== null && (n.flags |= 4), (p.hostBindings !== null || p.hostAttrs !== null || p.hostVars !== 0) && (n.flags |= 64);
    let h = p.type.prototype;
    !l && (h.ngOnChanges || h.ngOnInit || h.ngDoCheck) && ((e12.preOrderHooks ??= []).push(n.index), l = true), !u && (h.ngOnChanges || h.ngDoCheck) && ((e12.preOrderCheckHooks ??= []).push(n.index), u = true), d++;
  }
  kh(e12, n, i);
}
function kh(e12, t, n) {
  for (let r = t.directiveStart; r < t.directiveEnd; r++) {
    let o = e12.data[r];
    if (n === null || !n.has(o))
      vl(0, t, o, r), vl(1, t, o, r), Il(t, r, false);
    else {
      let i = n.get(o);
      El(0, t, i, r), El(1, t, i, r), Il(t, r, true);
    }
  }
}
function vl(e12, t, n, r) {
  let o = e12 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s;
      e12 === 0 ? s = t.inputs ??= {} : s = t.outputs ??= {}, s[i] ??= [], s[i].push(r), Hu(t, i);
    }
}
function El(e12, t, n, r) {
  let o = e12 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s = o[i], a;
      e12 === 0 ? a = t.hostDirectiveInputs ??= {} : a = t.hostDirectiveOutputs ??= {}, a[s] ??= [], a[s].push(r, i), Hu(t, s);
    }
}
function Hu(e12, t) {
  t === "class" ? e12.flags |= 8 : t === "style" && (e12.flags |= 16);
}
function Il(e12, t, n) {
  let { attrs: r, inputs: o, hostDirectiveInputs: i } = e12;
  if (r === null || !n && o === null || n && i === null || Dp(e12)) {
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
function Ph(e12, t, n, r, o) {
  e12.data[r] = o;
  let i = o.factory || (o.factory = bt(o.type, true)), s = new ln(i, Nt(o), ju, null);
  e12.blueprint[r] = s, n[r] = s, Lh(e12, t, r, pu(e12, n, o.hostVars, Re), o);
}
function Lh(e12, t, n, r, o) {
  let i = o.hostBindings;
  if (i) {
    let s = e12.hostBindingOpCodes;
    s === null && (s = e12.hostBindingOpCodes = []);
    let a = ~t.index;
    Fh(s) != a && s.push(a), s.push(n, r, i);
  }
}
function Fh(e12) {
  let t = e12.length;
  for (; t > 0; ) {
    let n = e12[--t];
    if (typeof n == "number" && n < 0)
      return n;
  }
  return 0;
}
function jh(e12, t, n) {
  if (n) {
    if (t.exportAs)
      for (let r = 0; r < t.exportAs.length; r++)
        n[t.exportAs[r]] = e12;
    Nt(t) && (n[""] = e12);
  }
}
function Hh(e12, t, n) {
  e12.flags |= 1, e12.directiveStart = t, e12.directiveEnd = t + n, e12.providerIndexes = t;
}
function Vh(e12, t, n, r, o, i, s, a) {
  let c = t[m], l = c.consts, u = he(l, s), d = eo(c, e12, n, r, u);
  return i && xh(c, t, d, he(l, a), o), d.mergedAttrs = $r(d.mergedAttrs, d.attrs), d.attrs !== null && Pr(d, d.attrs, false), d.mergedAttrs !== null && Pr(d, d.mergedAttrs, true), c.queries !== null && c.queries.elementStart(c, d), d;
}
function Bh(e12, t) {
  Mf(e12, t), Ci(t) && e12.queries.elementEnd(t);
}
function $h(e12, t, n, r, o, i) {
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
function Uh(e12, t, n) {
  return function r(o) {
    let i = r.__ngNativeEl__;
    i !== void 0 && Gf(o, i);
    let s = St(e12) ? we(e12.index, t) : t;
    Xs(s, 5);
    let a = t[N], c = Dl(t, a, n, o), l = r.__ngNextListenerFn__;
    for (; l; )
      c = Dl(t, a, l, o) && c, l = l.__ngNextListenerFn__;
    return c;
  };
}
function Dl(e12, t, n, r) {
  let o = g(null);
  try {
    return T(C.OutputStart, t, n), n(r) !== false;
  } catch (i) {
    return oh(e12, i), false;
  } finally {
    T(C.OutputEnd, t, n), g(o);
  }
}
function zh(e12, t, n, r, o, i, s, a) {
  let c = wi(e12), l = false, u = null;
  if (!r && c && (u = Gh(t, n, i, e12.index)), u !== null) {
    let d = u.__ngLastListenerFn__ || u;
    d.__ngNextListenerFn__ = s, u.__ngLastListenerFn__ = s, l = true;
  } else {
    let d = pe(e12, n), f = r ? r(d) : d;
    Zf(n, f, i, a), r || (a.__ngNativeEl__ = d);
    let p = o.listen(f, i, a);
    if (!Wh(i)) {
      let h = r ? (L) => r(te(L[e12.index])) : e12.index;
      qh(h, t, n, i, a, p, false);
    }
  }
  return l;
}
function Wh(e12) {
  return e12.startsWith("animation") || e12.startsWith("transition");
}
function Gh(e12, t, n, r) {
  let o = e12.cleanup;
  if (o != null)
    for (let i = 0; i < o.length - 1; i += 2) {
      let s = o[i];
      if (s === n && o[i + 1] === r) {
        let a = t[Mt], c = o[i + 2];
        return a && a.length > c ? a[c] : null;
      }
      typeof s == "string" && (i += 2);
    }
  return null;
}
function qh(e12, t, n, r, o, i, s) {
  let a = t.firstCreatePass ? xi(t) : null, c = Ni(n), l = c.length;
  c.push(o, i), a && a.push(r, e12, l, (l + 1) * (s ? -1 : 1));
}
var ms = Symbol("BINDING");
function Zh(e12) {
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
function Qh(e12) {
  return Object.keys(e12).map((t) => {
    let [n, r, o] = e12[t], i = { propName: n, templateName: t, isSignal: (r & Qr.SignalBased) !== 0 };
    return o && (i.transform = o), i;
  });
}
function Yh(e12) {
  return Object.keys(e12).map((t) => ({ propName: e12[t], templateName: t }));
}
function Kh(e12, t, n) {
  let r = t instanceof Y ? t : t?.injector;
  return r && e12.getStandaloneInjector !== null && (r = e12.getStandaloneInjector(r) || r), r ? new gs(n, r) : n;
}
function Jh(e12) {
  let t = e12.get(lt, null);
  if (t === null)
    throw new v(407, false);
  let n = e12.get(Fu, null), r = e12.get(Ke, null), o = e12.get(Bt, null, { optional: true });
  return { rendererFactory: t, sanitizer: n, changeDetectionScheduler: r, ngReflect: false, tracingService: o };
}
function Xh(e12, t) {
  let n = Vu(e12);
  return cu(t, n, n === "svg" ? mc : n === "math" ? yc : null);
}
function Vu(e12) {
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
    return this.cachedInputs ??= Qh(this.componentDef.inputs), this.cachedInputs;
  }
  get outputs() {
    return this.cachedOutputs ??= Yh(this.componentDef.outputs), this.cachedOutputs;
  }
  constructor(t, n) {
    super(), this.componentDef = t, this.ngModule = n, this.componentType = t.type, this.selector = Cp(t.selectors), this.ngContentSelectors = t.ngContentSelectors ?? [], this.isBoundToModule = !!n;
  }
  create(t, n, r, o, i, s) {
    T(C.DynamicComponentStart);
    let a = g(null);
    try {
      let c = this.componentDef, l = Kh(c, o || this.ngModule, t), u = Jh(l), d = u.tracingService;
      return d && d.componentCreate ? d.componentCreate(Zh(c), () => this.createComponentRef(u, l, n, r, i, s)) : this.createComponentRef(u, l, n, r, i, s);
    } finally {
      g(a);
    }
  }
  createComponentRef(t, n, r, o, i, s) {
    let a = this.componentDef, c = eg(o, a, s, i), l = t.rendererFactory.createRenderer(null, a), u = o ? Zp(l, o, a.encapsulation, n) : Xh(a, l), d = s?.some(bl) || i?.some((h) => typeof h != "function" && h.bindings.some(bl)), f = Ws(null, c, null, 512 | fu(a), null, null, t, l, n, null, eu(u, n, true));
    f[B] = u, gr(f);
    let p = null;
    try {
      let h = Vh(B, f, 2, "#host", () => c.directiveRegistry, true, 0);
      du(l, u, h), Ft(u, f), qp(c, f, h), Yf(c, h, f), Bh(c, h), r !== void 0 && ng(h, this.ngContentSelectors, r), p = we(h.index, f), f[N] = p[N], Js(c, f, null);
    } catch (h) {
      throw p !== null && Ki(p), Ki(f), h;
    } finally {
      T(C.DynamicComponentEnd), mr();
    }
    return new Lr(this.componentType, f, !!d);
  }
};
function eg(e12, t, n, r) {
  let o = e12 ? ["ng-version", "21.2.11"] : wp(t.selectors[0]), i = null, s = null, a = 0;
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
  return zs(0, null, tg(i, s), 1, a, c, null, null, null, [o], null);
}
function tg(e12, t) {
  return !e12 && !t ? null : (n) => {
    if (n & 1 && e12)
      for (let r of e12)
        r.create();
    if (n & 2 && t)
      for (let r of t)
        r.update();
  };
}
function bl(e12) {
  let t = e12[ms].kind;
  return t === "input" || t === "twoWay";
}
var Lr = class extends Lu {
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
    super(), this._rootLView = n, this._hasInputBindings = r, this._tNode = ur(n[m], B), this.location = Vt(this._tNode, n), this.instance = we(this._tNode.index, n)[N], this.hostView = this.changeDetectorRef = new jt(n, void 0), this.componentType = t;
  }
  setInput(t, n) {
    this._hasInputBindings;
    let r = this._tNode;
    if (this.previousInputValues ??= /* @__PURE__ */ new Map(), this.previousInputValues.has(t) && Object.is(this.previousInputValues.get(t), n))
      return;
    let o = this._rootLView, i = ih(r, o[m], o, t, n);
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
function ng(e12, t, n) {
  let r = e12.projection = [];
  for (let o = 0; o < t.length; o++) {
    let i = n[o];
    r.push(i != null && i.length ? Array.from(i) : null);
  }
}
var ro = /* @__PURE__ */ (() => {
  class e12 {
    static __NG_ELEMENT_ID__ = rg;
  }
  return e12;
})();
function rg() {
  let e12 = ge();
  return Bu(e12, M());
}
var vs = class e4 extends ro {
  _lContainer;
  _hostTNode;
  _hostLView;
  constructor(t, n, r) {
    super(), this._lContainer = t, this._hostTNode = n, this._hostLView = r;
  }
  get element() {
    return Vt(this._hostTNode, this._hostLView);
  }
  get injector() {
    return new at(this._hostTNode, this._hostLView);
  }
  get parentInjector() {
    let t = ks(this._hostTNode, this._hostLView);
    if (kl(t)) {
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
    let n = Cl(this._lContainer);
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
    let c = t && !If(t), l;
    if (c)
      l = n;
    else {
      let H = n || {};
      l = H.index, r = H.injector, o = H.projectableNodes, i = H.environmentInjector || H.ngModuleRef, s = H.directives, a = H.bindings;
    }
    let u = c ? t : new hn(Xe(t)), d = r || this.parentInjector;
    if (!i && u.ngModule == null) {
      let ft = (c ? d : this.parentInjector).get(Y, null);
      ft && (i = ft);
    }
    let f = Xe(u.componentType ?? {}), p = ps(this._lContainer, f?.id ?? null), h = p?.firstChild ?? null, L = u.create(d, o, h, i, s, a);
    return this.insertImpl(L.hostView, l, un(this._hostTNode, p)), L;
  }
  insert(t, n) {
    return this.insertImpl(t, n, true);
  }
  insertImpl(t, n, r) {
    let o = t._lView;
    if (Ec(o)) {
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
    let n = Cl(this._lContainer);
    return n !== null ? n.indexOf(t) : -1;
  }
  remove(t) {
    let n = this._adjustIndex(t, -1), r = fn(this._lContainer, n);
    r && (Jt(Gi(this._lContainer), n), Yr(r[m], r));
  }
  detach(t) {
    let n = this._adjustIndex(t, -1), r = fn(this._lContainer, n);
    return r && Jt(Gi(this._lContainer), n) != null ? new jt(r) : null;
  }
  _adjustIndex(t, n = 0) {
    return t ?? this.length + n;
  }
};
function Cl(e12) {
  return e12[tn];
}
function Gi(e12) {
  return e12[tn] || (e12[tn] = []);
}
function Bu(e12, t) {
  let n, r = t[e12.index];
  return oe(r) ? n = r : (n = Ru(r, t, null, e12), t[e12.index] = n, Gs(t, n)), ig(n, t, e12, r), new vs(n, e12, t);
}
function og(e12, t) {
  let n = e12[O], r = n.createComment(""), o = pe(t, e12), i = n.parentNode(o);
  return kr(n, i, r, n.nextSibling(o), false), r;
}
var ig = cg;
var sg = () => false;
function ag(e12, t, n) {
  return sg(e12, t, n);
}
function cg(e12, t, n, r) {
  if (e12[Ve])
    return;
  let o;
  n.type & 8 ? o = te(r) : o = og(t, n), e12[Ve] = o;
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
    this.flags = n, this.read = r, typeof t == "string" ? this.predicate = mg(t) : this.predicate = t;
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
        this.matchTNodeWithReadOption(t, n, lg(n, i)), this.matchTNodeWithReadOption(t, n, _r(n, t, i, false, false));
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
function lg(e12, t) {
  let n = e12.localNames;
  if (n !== null) {
    for (let r = 0; r < n.length; r += 2)
      if (n[r] === t)
        return n[r + 1];
  }
  return null;
}
function ug(e12, t) {
  return e12.type & 11 ? Vt(e12, t) : e12.type & 4 ? ea(e12, t) : null;
}
function dg(e12, t, n, r) {
  return n === -1 ? ug(t, e12) : n === -2 ? fg(e12, t, r) : Ar(e12, e12[m], n, t);
}
function fg(e12, t, n) {
  if (n === yn)
    return Vt(t, e12);
  if (n === pn)
    return ea(t, e12);
  if (n === ro)
    return Bu(t, e12);
}
function $u(e12, t, n, r) {
  let o = t[fe].queries[r];
  if (o.matches === null) {
    let i = e12.data, s = n.matches, a = [];
    for (let c = 0; s !== null && c < s.length; c += 2) {
      let l = s[c];
      if (l < 0)
        a.push(null);
      else {
        let u = i[l];
        a.push(dg(t, u, s[c + 1], n.metadata.read));
      }
    }
    o.matches = a;
  }
  return o.matches;
}
function ws(e12, t, n, r) {
  let o = e12.queries.getByIndex(n), i = o.matches;
  if (i !== null) {
    let s = $u(e12, t, o, n);
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
function pg(e12, t) {
  return e12[fe].queries[t].queryList;
}
function hg(e12, t, n) {
  let r = new Or((n & 4) === 4);
  return bc(e12, t, r, r.destroy), (t[fe] ??= new Is()).queries.push(new Es(r)) - 1;
}
function gg(e12, t, n) {
  let r = ie();
  return r.firstCreatePass && (yg(r, new Ds(e12, t, n), -1), (t & 2) === 2 && (r.staticViewQueries = true)), hg(r, M(), t);
}
function mg(e12) {
  return e12.split(",").map((t) => t.trim());
}
function yg(e12, t, n) {
  e12.queries === null && (e12.queries = new bs()), e12.queries.track(new Cs(t, n));
}
function ta(e12, t) {
  return e12.queries.getByIndex(t);
}
function vg(e12, t) {
  let n = e12[m], r = ta(n, t);
  return r.crossesNgTemplate ? ws(n, e12, t, []) : $u(n, e12, r, t);
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
function Uu(e12, t, n = null) {
  return new gn({ providers: e12, parent: t, debugName: n, runEnvironmentInitializers: true }).injector;
}
var Eg = (() => {
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
        let r = vi(false, n.type), o = r.length > 0 ? Uu([r], this._injector, "") : null;
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
  return Nl(() => {
    let t = Cg(e12), n = R(x({}, t), { decls: e12.decls, vars: e12.vars, template: e12.template, consts: e12.consts || null, ngContentSelectors: e12.ngContentSelectors, onPush: e12.changeDetection === Ps.OnPush, directiveDefs: null, pipeDefs: null, dependencies: t.standalone && e12.dependencies || null, getStandaloneInjector: t.standalone ? (o) => o.get(Eg).getOrCreateStandaloneInjector(n) : null, getExternalStyles: null, signals: e12.signals ?? false, data: e12.data || {}, encapsulation: e12.encapsulation || se.Emulated, styles: e12.styles || ke, _: null, schemas: e12.schemas || null, tView: null, id: "" });
    t.standalone && dt("NgStandalone"), wg(n);
    let r = e12.dependencies;
    return n.directiveDefs = wl(r, Ig), n.pipeDefs = wl(r, tc), n.id = Tg(n), n;
  });
}
function Ig(e12) {
  return Xe(e12) || ui(e12);
}
function Dg(e12, t) {
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
function bg(e12) {
  if (e12 == null)
    return et;
  let t = {};
  for (let n in e12)
    e12.hasOwnProperty(n) && (t[e12[n]] = n);
  return t;
}
function Cg(e12) {
  let t = {};
  return { type: e12.type, providersResolver: null, viewProvidersResolver: null, factory: null, hostBindings: e12.hostBindings || null, hostVars: e12.hostVars || 0, hostAttrs: e12.hostAttrs || null, contentQueries: e12.contentQueries || null, declaredInputs: t, inputConfig: e12.inputs || et, exportAs: e12.exportAs || null, standalone: e12.standalone ?? true, signals: e12.signals === true, selectors: e12.selectors || ke, viewQuery: e12.viewQuery || null, features: e12.features || null, setInput: null, resolveHostDirectives: null, hostDirectives: null, controlDef: null, inputs: Dg(e12.inputs, t), outputs: bg(e12.outputs), debugInfo: null };
}
function wg(e12) {
  e12.features?.forEach((t) => t(e12));
}
function wl(e12, t) {
  return e12 ? () => {
    let n = typeof e12 == "function" ? e12() : e12, r = [];
    for (let o of n) {
      let i = t(o);
      i !== null && r.push(i);
    }
    return r;
  } : null;
}
function Tg(e12) {
  let t = 0, n = typeof e12.consts == "function" ? "" : e12.consts, r = [e12.selectors, e12.ngContentSelectors, e12.hostVars, e12.hostAttrs, n, e12.vars, e12.decls, e12.encapsulation, e12.standalone, e12.signals, e12.exportAs, JSON.stringify(e12.inputs), JSON.stringify(e12.outputs), Object.getOwnPropertyNames(e12.type.prototype), !!e12.contentQueries, !!e12.viewQuery];
  for (let i of r.join("|"))
    t = Math.imul(31, t) + i.charCodeAt(0) << 0;
  return t += 2147483648, "c" + t;
}
function Mg(e12, t, n, r, o, i, s, a) {
  if (n.firstCreatePass) {
    e12.mergedAttrs = $r(e12.mergedAttrs, e12.attrs);
    let u = e12.tView = zs(2, e12, o, i, s, n.directiveRegistry, n.pipeRegistry, null, n.schemas, n.consts, null);
    n.queries !== null && (n.queries.template(n, e12), u.queries = n.queries.embeddedTView(e12));
  }
  a && (e12.flags |= a), At(e12, false);
  let c = _g(n, t, e12, r);
  yr() && Ys(n, t, c, e12), Ft(c, t);
  let l = Ru(c, t, c, e12);
  t[r + B] = l, Gs(t, l), ag(l, e12, t);
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
  return Mg(f, e12, t, n, r, o, i, c), l != null && Du(e12, f, u), f;
}
var _g = Sg;
function Sg(e12, t, n, r) {
  return vr(true), t[O].createComment("");
}
var ra = new D("");
function oa(e12) {
  return !!e12 && typeof e12.then == "function";
}
function zu(e12) {
  return !!e12 && typeof e12.subscribe == "function";
}
var Wu = new D("");
var ia = (() => {
  class e12 {
    resolve;
    reject;
    initialized = false;
    done = false;
    donePromise = new Promise((n, r) => {
      this.resolve = n, this.reject = r;
    });
    appInits = E(Wu, { optional: true }) ?? [];
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
        else if (zu(i)) {
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
var Gu = new D("");
function qu() {
  Ao(() => {
    let e12 = "";
    throw new v(600, e12);
  });
}
function Zu(e12) {
  return e12.isBoundToModule;
}
var Ng = 10;
var Dn = (() => {
  class e12 {
    _runningTick = false;
    _destroyed = false;
    _destroyListeners = [];
    _views = [];
    internalErrorHandler = E(st);
    afterRenderManager = E(gu);
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
    internalPendingTask = E(kt);
    get isStable() {
      return this.internalPendingTask.hasPendingTasksObservable.pipe(zo((n) => !n));
    }
    constructor() {
      E(Bt, { optional: true });
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
        let l = Zu(c) ? void 0 : this._injector.get(Fr), u = r || c.selector, d = c.create(o, [], u, l), f = d.location.nativeElement, p = d.injector.get(ra, null);
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
      for (; this.dirtyFlags !== 0 && n++ < Ng; ) {
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
          _u(o, i), n = true;
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
      this.components.push(n), this._injector.get(Gu, []).forEach((o) => o(n));
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
function xg(e12, t, n, r) {
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
      let H = n(s, u), ft = n(a, p), Ut = n(s, d);
      if (Object.is(Ut, ft)) {
        let Io = n(l, h);
        Object.is(Io, H) ? (e12.swap(s, a), e12.updateValue(a, h), l--, a--) : e12.move(a, s), e12.updateValue(s, d), s++;
        continue;
      }
      if (o ??= new Hr(), i ??= Ml(e12, s, a, n), Ms(e12, o, s, Ut))
        e12.updateValue(s, d), s++, a++;
      else if (i.has(Ut))
        o.set(H, e12.detach(s)), a--;
      else {
        let Io = e12.create(s, t[s]);
        e12.attach(s, Io), s++, a++;
      }
    }
    for (; s <= l; )
      Tl(e12, o, n, s, t[s]), s++;
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
        o ??= new Hr(), i ??= Ml(e12, s, a, n);
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
      Tl(e12, o, n, e12.length, u.value), u = l.next();
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
function Tl(e12, t, n, r, o) {
  if (Ms(e12, t, r, n(r, o)))
    e12.updateValue(r, o);
  else {
    let i = e12.create(r, o);
    e12.attach(r, i);
  }
}
function Ml(e12, t, n, r) {
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
  dt("NgControlFlow");
  let c = M(), l = ie(), u = he(l.consts, i);
  return jr(c, l, e12, t, n, r, o, u, 256, s, a), sa;
}
function sa(e12, t, n, r, o, i, s, a) {
  dt("NgControlFlow");
  let c = M(), l = ie(), u = he(l.consts, i);
  return jr(c, l, e12, t, n, r, o, u, 512, s, a), sa;
}
function Cn(e12, t) {
  dt("NgControlFlow");
  let n = M(), r = rn(), o = n[r] !== Re ? n[r] : -1, i = o !== -1 ? Vr(n, B + o) : void 0, s = 0;
  if (In(n, r, e12)) {
    let a = g(null);
    try {
      if (i !== void 0 && Ou(i, s), e12 !== -1) {
        let c = B + e12, l = Vr(n, c), u = xs(n[m], c), d = Pu(l, u, n), f = Jr(n, u, t, { dehydratedView: d });
        Xr(l, f, s, un(u, d));
      }
    } finally {
      g(a);
    }
  } else if (i !== void 0) {
    let a = Au(i, s);
    a !== void 0 && (a[N] = t);
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
  dt("NgControlFlow");
  let p = M(), h = ie(), L = c !== void 0, H = M(), ft = a ? s.bind(H[ee][N]) : s, Ut = new Ss(L, ft);
  H[B + e12] = Ut, jr(p, h, e12 + 1, t, n, r, o, he(h.consts, i), 256), L && jr(p, h, e12 + 2, c, l, u, d, he(h.consts, f), 512);
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
    return this.getLView(t)[N].$implicit;
  }
  attach(t, n) {
    let r = n[Tt];
    this.needsIndexUpdate ||= t !== this.length, Xr(this.lContainer, n, t, un(this.templateTNode, r)), Rg(this.lContainer, t);
  }
  detach(t) {
    return this.needsIndexUpdate ||= t !== this.length - 1, Ag(this.lContainer, t), Og(this.lContainer, t);
  }
  create(t, n) {
    let r = ps(this.lContainer, this.templateTNode.tView.ssrId);
    return Jr(this.hostLView, this.templateTNode, new _s(this.lContainer, n, t), { dehydratedView: r });
  }
  destroy(t) {
    Yr(t[m], t);
  }
  updateValue(t, n) {
    this.getLView(t)[N].$implicit = n;
  }
  reset() {
    this.needsIndexUpdate = false;
  }
  updateIndexes() {
    if (this.needsIndexUpdate)
      for (let t = 0; t < this.length; t++)
        this.getLView(t)[N].$index = t;
  }
  getLView(t) {
    return kg(this.lContainer, t);
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
    if (xg(c, e12, i.trackByFn, t), c.updateIndexes(), i.hasEmptyBlock) {
      let l = rn(), u = c.length === 0;
      if (In(r, l, u)) {
        let d = n + 2, f = Vr(r, d);
        if (u) {
          let p = xs(o, d), h = Pu(f, p, r), L = Jr(r, p, void 0, { dehydratedView: h });
          Xr(f, L, 0, un(p, h));
        } else
          o.firstUpdatePass && Mh(f), Ou(f, 0);
      }
    }
  } finally {
    g(t);
  }
}
function Vr(e12, t) {
  return e12[t];
}
function Rg(e12, t) {
  if (e12.length <= S)
    return;
  let n = S + t, r = e12[n], o = r ? r[He] : void 0;
  if (r && o && o.detachedLeaveAnimationFns && o.detachedLeaveAnimationFns.length > 0) {
    let i = r[be];
    Rp(i, o), ct.delete(r[Ce]), o.detachedLeaveAnimationFns = void 0;
  }
}
function Ag(e12, t) {
  if (e12.length <= S)
    return;
  let n = S + t, r = e12[n], o = r ? r[He] : void 0;
  o && o.leave && o.leave.size > 0 && (o.detachedLeaveAnimationFns = []);
}
function Og(e12, t) {
  return fn(e12, t);
}
function kg(e12, t) {
  return Au(e12, t);
}
function xs(e12, t) {
  return ur(e12, t);
}
function k(e12, t, n, r) {
  let o = M(), i = o[m], s = e12 + B, a = i.firstCreatePass ? $h(s, i, 2, t, n, r) : i.data[s];
  return nh(a, o, e12, t, Pg), r != null && Du(o, a), k;
}
function P() {
  let e12 = ge(), t = rh(e12);
  return _c(t) && Sc(), Tc(), P;
}
function ao(e12, t, n, r) {
  return k(e12, t, n, r), P(), ao;
}
var Pg = (e12, t, n, r, o) => (vr(true), cu(t[O], r, $c()));
function co() {
  return M();
}
function ae(e12, t, n) {
  let r = M(), o = rn();
  if (In(r, o, t)) {
    let i = ie(), s = Bc();
    Kp(s, r, e12, t, r[O], n);
  }
  return ae;
}
var wn = "en-US";
var Lg = wn;
function Qu(e12) {
  typeof e12 == "string" && (Lg = e12.toLowerCase().replace(/_/g, "-"));
}
function Ae(e12, t, n) {
  let r = M(), o = ie(), i = ge();
  return (i.type & 3 || n) && zh(i, o, r, n, r[O], e12, t, Uh(i, r, t)), Ae;
}
function ce(e12 = 1) {
  return Vc(e12);
}
function lo(e12, t, n) {
  return gg(e12, t, n), lo;
}
function aa(e12) {
  let t = M(), n = ie(), r = ki();
  hr(r + 1);
  let o = ta(n, r);
  if (e12.dirty && vc(t) === ((o.metadata.flags & 2) === 2)) {
    if (o.matches === null)
      e12.reset([]);
    else {
      let i = vg(t, r);
      e12.reset(i, Vf), e12.notifyOnChanges();
    }
    return true;
  }
  return false;
}
function ca() {
  return pg(M(), ki());
}
function wr(e12, t) {
  return e12 << 17 | t << 2;
}
function ut(e12) {
  return e12 >> 17 & 32767;
}
function Fg(e12) {
  return (e12 & 2) == 2;
}
function jg(e12, t) {
  return e12 & 131071 | t << 17;
}
function Rs(e12) {
  return e12 | 2;
}
function Ht(e12) {
  return (e12 & 131068) >> 2;
}
function Zi(e12, t) {
  return e12 & -131069 | t << 2;
}
function Hg(e12) {
  return (e12 & 1) === 1;
}
function As(e12) {
  return e12 | 1;
}
function Vg(e12, t, n, r, o, i) {
  let s = i ? t.classBindings : t.styleBindings, a = ut(s), c = Ht(s);
  e12[r] = n;
  let l = false, u;
  if (Array.isArray(n)) {
    let d = n;
    u = d[1], (u === null || Ct(d, u) > 0) && (l = true);
  } else
    u = n;
  if (o)
    if (c !== 0) {
      let f = ut(e12[a + 1]);
      e12[r + 1] = wr(f, a), f !== 0 && (e12[f + 1] = Zi(e12[f + 1], r)), e12[a + 1] = jg(e12[a + 1], r);
    } else
      e12[r + 1] = wr(a, 0), a !== 0 && (e12[a + 1] = Zi(e12[a + 1], r)), a = r;
  else
    e12[r + 1] = wr(c, 0), a === 0 ? a = r : e12[c + 1] = Zi(e12[c + 1], r), c = r;
  l && (e12[r + 1] = Rs(e12[r + 1])), _l(e12, u, r, true), _l(e12, u, r, false), Bg(t, u, e12, r, i), s = wr(a, c), i ? t.classBindings = s : t.styleBindings = s;
}
function Bg(e12, t, n, r, o) {
  let i = o ? e12.residualClasses : e12.residualStyles;
  i != null && typeof t == "string" && Ct(i, t) >= 0 && (n[r + 1] = As(n[r + 1]));
}
function _l(e12, t, n, r) {
  let o = e12[n + 1], i = t === null, s = r ? ut(o) : Ht(o), a = false;
  for (; s !== 0 && (a === false || i); ) {
    let c = e12[s], l = e12[s + 1];
    $g(c, t) && (a = true, e12[s + 1] = r ? As(l) : Rs(l)), s = r ? ut(l) : Ht(l);
  }
  a && (e12[n + 1] = r ? Rs(o) : As(o));
}
function $g(e12, t) {
  return e12 === null || t == null || (Array.isArray(e12) ? e12[1] : e12) === t ? true : Array.isArray(e12) && typeof t == "string" ? Ct(e12, t) >= 0 : false;
}
function uo(e12, t) {
  return Ug(e12, t, null, true), uo;
}
function Ug(e12, t, n, r) {
  let o = M(), i = ie(), s = Ac(2);
  if (i.firstUpdatePass && Wg(i, e12, s, r), t !== Re && In(o, s, t)) {
    let a = i.data[$e()];
    Yg(i, a, o, o[O], e12, o[s + 1] = Kg(t, n), r, s);
  }
}
function zg(e12, t) {
  return t >= e12.expandoStartIndex;
}
function Wg(e12, t, n, r) {
  let o = e12.data;
  if (o[n + 1] === null) {
    let i = o[$e()], s = zg(e12, n);
    Jg(i, r) && t === null && !s && (t = false), t = Gg(o, i, t, r), Vg(o, i, t, n, s, r);
  }
}
function Gg(e12, t, n, r) {
  let o = Lc(e12), i = r ? t.residualClasses : t.residualStyles;
  if (o === null)
    (r ? t.classBindings : t.styleBindings) === 0 && (n = Qi(null, e12, t, n, r), n = mn(n, t.attrs, r), i = null);
  else {
    let s = t.directiveStylingLast;
    if (s === -1 || e12[s] !== o)
      if (n = Qi(o, e12, t, n, r), i === null) {
        let c = qg(e12, t, r);
        c !== void 0 && Array.isArray(c) && (c = Qi(null, e12, t, c[1], r), c = mn(c, t.attrs, r), Zg(e12, t, r, c));
      } else
        i = Qg(e12, t, r);
  }
  return i !== void 0 && (r ? t.residualClasses = i : t.residualStyles = i), n;
}
function qg(e12, t, n) {
  let r = n ? t.classBindings : t.styleBindings;
  if (Ht(r) !== 0)
    return e12[ut(r)];
}
function Zg(e12, t, n, r) {
  let o = n ? t.classBindings : t.styleBindings;
  e12[ut(o)] = r;
}
function Qg(e12, t, n) {
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
      typeof s == "number" ? o = s : o === r && (Array.isArray(e12) || (e12 = e12 === void 0 ? [] : ["", e12]), cc(e12, s, n ? true : t[++i]));
    }
  return e12 === void 0 ? null : e12;
}
function Yg(e12, t, n, r, o, i, s, a) {
  if (!(t.type & 3))
    return;
  let c = e12.data, l = c[a + 1], u = Hg(l) ? Sl(c, t, n, o, Ht(l), s) : void 0;
  if (!Br(u)) {
    Br(i) || Fg(l) && (i = Sl(c, null, n, o, a, s));
    let d = Ti($e(), n);
    Gp(r, s, d, o, i);
  }
}
function Sl(e12, t, n, r, o, i) {
  let s = t === null, a;
  for (; o > 0; ) {
    let c = e12[o], l = Array.isArray(c), u = l ? c[1] : c, d = u === null, f = n[o + 1];
    f === Re && (f = d ? ke : void 0);
    let p = d ? sr(f, r) : u === r ? f : void 0;
    if (l && !Br(p) && (p = sr(c, r)), Br(p) && (a = p, s))
      return a;
    let h = e12[o + 1];
    o = s ? ut(h) : Ht(h);
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
function Kg(e12, t) {
  return e12 == null || e12 === "" || (typeof t == "string" ? e12 = e12 + t : typeof e12 == "object" && (e12 = er(Ne(e12)))), e12;
}
function Jg(e12, t) {
  return (e12.flags & (t ? 8 : 16)) !== 0;
}
function W(e12, t = "") {
  let n = M(), r = ie(), o = e12 + B, i = r.firstCreatePass ? eo(r, o, 1, t, null) : r.data[o], s = Xg(r, n, i, t);
  n[o] = s, yr() && Ys(r, n, s, i), At(i, false);
}
var Xg = (e12, t, n, r) => (vr(true), gp(t[O], r));
function em(e12, t, n, r = "") {
  return In(e12, rn(), n) ? t + fi(n) + r : Re;
}
function Oe(e12) {
  return la("", e12), Oe;
}
function la(e12, t, n) {
  let r = M(), o = em(r, e12, t, n);
  return o !== Re && tm(r, $e(), o), la;
}
function tm(e12, t, n) {
  let r = Ti(t, e12);
  mp(e12[O], r, n);
}
var Yu = (() => {
  class e12 {
    applicationErrorHandler = E(st);
    appRef = E(Dn);
    taskService = E(kt);
    ngZone = E(K);
    zonelessEnabled = E(on);
    tracing = E(Bt, { optional: true });
    zoneIsDefined = typeof Zone < "u" && !!Zone.root.run;
    schedulerTickApplyArgs = [{ data: { __scheduler_tick__: true } }];
    subscriptions = new $();
    angularZoneId = this.zoneIsDefined ? this.ngZone._inner?.get(Yt) : null;
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
      let r = this.useMicrotaskScheduler ? qc : Fi;
      this.pendingRenderTaskId = this.taskService.add(), this.scheduleInRootZone ? this.cancelScheduledCallback = Zone.root.run(() => r(() => this.tick())) : this.cancelScheduledCallback = this.ngZone.runOutsideAngular(() => r(() => this.tick()));
    }
    shouldScheduleTick() {
      return !(this.appRef.destroyed || this.pendingRenderTaskId !== null || this.runningTick || this.appRef._runningTick || !this.zonelessEnabled && this.zoneIsDefined && Zone.current.get(Yt + this.angularZoneId));
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
function ua() {
  return dt("NgZoneless"), wt([...da(), []]);
}
function da() {
  return [{ provide: Ke, useExisting: Yu }, { provide: K, useClass: Kt }, { provide: on, useValue: true }];
}
function nm() {
  return typeof $localize < "u" && $localize.locale || wn;
}
var fa = new D("", { factory: () => E(fa, { optional: true, skipSelf: true }) || nm() });
function We(e12, t) {
  return jn(e12, t?.equal);
}
var pa = new D("");
var fm = new D("");
function Tn(e12) {
  return !e12.moduleRef;
}
function pm(e12) {
  let t = Tn(e12) ? e12.r3Injector : e12.moduleRef.injector, n = t.get(K);
  return n.run(() => {
    Tn(e12) ? e12.r3Injector.resolveInjectorInitializers() : e12.moduleRef.resolveInjectorInitializers();
    let r = t.get(st), o;
    if (n.runOutsideAngular(() => {
      o = n.onError.subscribe({ next: r });
    }), Tn(e12)) {
      let i = () => t.destroy(), s = e12.platformInjector.get(pa);
      s.add(i), t.onDestroy(() => {
        o.unsubscribe(), s.delete(i);
      });
    } else {
      let i = () => e12.moduleRef.destroy(), s = e12.platformInjector.get(pa);
      s.add(i), e12.moduleRef.onDestroy(() => {
        cn(e12.allPlatformModules, e12.moduleRef), o.unsubscribe(), s.delete(i);
      });
    }
    return gm(r, n, () => {
      let i = t.get(kt), s = i.add(), a = t.get(ia);
      return a.runInitializers(), a.donePromise.then(() => {
        let c = t.get(fa, wn);
        if (Qu(c || wn), !t.get(fm, true))
          return Tn(e12) ? t.get(Dn) : (e12.allPlatformModules.push(e12.moduleRef), e12.moduleRef);
        if (Tn(e12)) {
          let u = t.get(Dn);
          return e12.rootComponent !== void 0 && u.bootstrap(e12.rootComponent), u;
        } else
          return hm?.(e12.moduleRef, e12.allPlatformModules), e12.moduleRef;
      }).finally(() => {
        i.remove(s);
      });
    });
  });
}
var hm;
function gm(e12, t, n) {
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
function mm(e12 = [], t) {
  return ue.create({ name: t, providers: [{ provide: Xt, useValue: "platform" }, { provide: pa, useValue: /* @__PURE__ */ new Set([() => fo = null]) }, ...e12] });
}
function ym(e12 = []) {
  if (fo)
    return fo;
  let t = mm(e12);
  return fo = t, qu(), vm(t), t;
}
function vm(e12) {
  let t = e12.get(zr, null);
  ar(e12, () => {
    t?.forEach((n) => n());
  });
}
var Em = 1e4;
var WM = Em - 1e3;
function Ju(e12) {
  let { rootComponent: t, appProviders: n, platformProviders: r, platformRef: o } = e12;
  T(C.BootstrapApplicationStart);
  try {
    let i = o?.injector ?? ym(r), s = [da(), Qc, ...n || []], a = new gn({ providers: s, parent: i, debugName: "", runEnvironmentInitializers: false });
    return pm({ r3Injector: a.injector, platformInjector: i, rootComponent: t });
  } catch (i) {
    return Promise.reject(i);
  } finally {
    T(C.BootstrapApplicationEnd);
  }
}
var Xu = null;
function $t() {
  return Xu;
}
function ha(e12) {
  Xu ??= e12;
}
var _n = class {
};
function ga(e12, t) {
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
var ed = "browser";
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
var Ea = (() => {
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
var ma = "ng-app-id";
function td(e12) {
  for (let t of e12)
    t.remove();
}
function nd(e12, t) {
  let n = t.createElement("style");
  return n.textContent = e12, n;
}
function Im(e12, t, n, r) {
  let o = e12.head?.querySelectorAll(`style[${ma}="${t}"],link[${ma}="${t}"]`);
  if (o)
    for (let i of o)
      i.removeAttribute(ma), i instanceof HTMLLinkElement ? r.set(i.href.slice(i.href.lastIndexOf("/") + 1), { usage: 0, elements: [i] }) : i.textContent && n.set(i.textContent, { usage: 0, elements: [i] });
}
function va(e12, t) {
  let n = t.createElement("link");
  return n.setAttribute("rel", "stylesheet"), n.setAttribute("href", e12), n;
}
var Ia = (() => {
  class e12 {
    doc;
    appId;
    nonce;
    inline = /* @__PURE__ */ new Map();
    external = /* @__PURE__ */ new Map();
    hosts = /* @__PURE__ */ new Set();
    constructor(n, r, o, i = {}) {
      this.doc = n, this.appId = r, this.nonce = o, Im(n, r, this.inline, this.external), this.hosts.add(n.head);
    }
    addStyles(n, r) {
      for (let o of n)
        this.addUsage(o, this.inline, nd);
      r?.forEach((o) => this.addUsage(o, this.external, va));
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
      o && (o.usage--, o.usage <= 0 && (td(o.elements), r.delete(n)));
    }
    ngOnDestroy() {
      for (let [, { elements: n }] of [...this.inline, ...this.external])
        td(n);
      this.hosts.clear();
    }
    addHost(n) {
      this.hosts.add(n);
      for (let [r, { elements: o }] of this.inline)
        o.push(this.addElement(n, nd(r, this.doc)));
      for (let [r, { elements: o }] of this.external)
        o.push(this.addElement(n, va(r, this.doc)));
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
var ya = { svg: "http://www.w3.org/2000/svg", xhtml: "http://www.w3.org/1999/xhtml", xlink: "http://www.w3.org/1999/xlink", xml: "http://www.w3.org/XML/1998/namespace", xmlns: "http://www.w3.org/2000/xmlns/", math: "http://www.w3.org/1998/Math/MathML" };
var Da = /%COMP%/g;
var od = "%COMP%";
var Dm = `_nghost-${od}`;
var bm = `_ngcontent-${od}`;
var Cm = true;
var wm = new D("", { factory: () => Cm });
function Tm(e12) {
  return bm.replace(Da, e12);
}
function Mm(e12) {
  return Dm.replace(Da, e12);
}
function id(e12, t) {
  return t.map((n) => n.replace(Da, e12));
}
var ba = (() => {
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
      return new (r || e12)(b(Ea), b(Ia), b(Ur), b(wm), b(z), b(K), b(Wr), b(Bt, 8));
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
    return n ? this.doc.createElementNS(ya[n] || n, t) : this.doc.createElement(t);
  }
  createComment(t) {
    return this.doc.createComment(t);
  }
  createText(t) {
    return this.doc.createTextNode(t);
  }
  appendChild(t, n) {
    (rd(t) ? t.content : t).appendChild(n);
  }
  insertBefore(t, n, r) {
    t && (rd(t) ? t.content : t).insertBefore(n, r);
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
      let i = ya[o];
      i ? t.setAttributeNS(i, n, r) : t.setAttribute(n, r);
    } else
      t.setAttribute(n, r);
  }
  removeAttribute(t, n, r) {
    if (r) {
      let o = ya[r];
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
    if (typeof t == "string" && (t = $t().getGlobalEventTarget(this.doc, t), !t))
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
function rd(e12) {
  return e12.tagName === "TEMPLATE" && e12.content !== void 0;
}
var ho = class extends xn {
  hostEl;
  sharedStylesHost;
  shadowRoot;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, o, i, a), this.hostEl = n, this.sharedStylesHost = c, this.shadowRoot = n.attachShadow({ mode: "open" }), this.sharedStylesHost && this.sharedStylesHost.addHost(this.shadowRoot);
    let l = r.styles;
    l = id(r.id, l);
    for (let d of l) {
      let f = document.createElement("style");
      s && f.setAttribute("nonce", s), f.textContent = d, this.shadowRoot.appendChild(f);
    }
    let u = r.getExternalStyles?.();
    if (u)
      for (let d of u) {
        let f = va(d, o);
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
    this.styles = c ? id(c, l) : l, this.styleUrls = r.getExternalStyles?.(c);
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
    super(t, n, r, i, s, a, c, l), this.contentAttr = Tm(l), this.hostAttr = Mm(l);
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
    ha(new e9());
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
    let n = _m();
    return n == null ? null : Sm(n);
  }
  resetBaseElement() {
    An = null;
  }
  getUserAgent() {
    return window.navigator.userAgent;
  }
  getCookie(t) {
    return ga(document.cookie, t);
  }
};
var An = null;
function _m() {
  return An = An || document.head.querySelector("base"), An ? An.getAttribute("href") : null;
}
function Sm(e12) {
  return new URL(e12, document.baseURI).pathname;
}
var Nm = (() => {
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
var sd = ["alt", "control", "meta", "shift"];
var xm = { "\b": "Backspace", "	": "Tab", "\x7F": "Delete", "\x1B": "Escape", Del: "Delete", Esc: "Escape", Left: "ArrowLeft", Right: "ArrowRight", Up: "ArrowUp", Down: "ArrowDown", Menu: "ContextMenu", Scroll: "ScrollLock", Win: "OS" };
var Rm = { alt: (e12) => e12.altKey, control: (e12) => e12.ctrlKey, meta: (e12) => e12.metaKey, shift: (e12) => e12.shiftKey };
var ad = (() => {
  class e12 extends Nn {
    constructor(n) {
      super(n);
    }
    supports(n) {
      return e12.parseEventName(n) != null;
    }
    addEventListener(n, r, o, i) {
      let s = e12.parseEventName(r), a = e12.eventCallback(s.fullKey, o, this.manager.getZone());
      return this.manager.getZone().runOutsideAngular(() => $t().onAndCancel(n, s.domEventName, a, i));
    }
    static parseEventName(n) {
      let r = n.toLowerCase().split("."), o = r.shift();
      if (r.length === 0 || !(o === "keydown" || o === "keyup"))
        return null;
      let i = e12._normalizeKey(r.pop()), s = "", a = r.indexOf("code");
      if (a > -1 && (r.splice(a, 1), s = "code."), sd.forEach((l) => {
        let u = r.indexOf(l);
        u > -1 && (r.splice(u, 1), s += l + ".");
      }), s += i, r.length != 0 || i.length === 0)
        return null;
      let c = {};
      return c.domEventName = o, c.fullKey = s, c;
    }
    static matchEventFullKeyCode(n, r) {
      let o = xm[n.key] || n.key, i = "";
      return r.indexOf("code.") > -1 && (o = n.code, i = "code."), o == null || !o ? false : (o = o.toLowerCase(), o === " " ? o = "space" : o === "." && (o = "dot"), sd.forEach((s) => {
        if (s !== o) {
          let a = Rm[s];
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
async function Ca(e12, t) {
  return Ju(Am(e12, t));
}
function Am(e12, t) {
  return { platformRef: t?.platformRef, appProviders: [...Fm, ...e12?.providers ?? []], platformProviders: Lm };
}
function Om() {
  yo.makeCurrent();
}
function km() {
  return new De();
}
function Pm() {
  return Ls(document), document;
}
var Lm = [{ provide: vn, useValue: ed }, { provide: zr, useValue: Om, multi: true }, { provide: z, useFactory: Pm }];
var Fm = [{ provide: Xt, useValue: "root" }, { provide: De, useFactory: km }, { provide: mo, useClass: po, multi: true }, { provide: mo, useClass: ad, multi: true }, ba, Ia, Ea, { provide: lt, useExisting: ba }, { provide: Sn, useClass: Nm }, []];
var wa = (() => {
  class e12 {
    static \u0275fac = function(r) {
      return new (r || e12)();
    };
    static \u0275prov = _({ token: e12, factory: function(r) {
      let o = null;
      return r ? o = new (r || e12)() : o = b(jm), o;
    }, providedIn: "root" });
  }
  return e12;
})();
var jm = (() => {
  class e12 extends wa {
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
    this.pageSize.set(t), this.page.set(0), this.model && (this.model.set("page_size", t), this.model.set("page", 0), this.model.save_changes());
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
var Hm = ["tableContainer"];
var Vm = ["app-root", ""];
function Bm(e12, t) {
  if (e12 & 1 && (k(0, "div", 2), W(1), P()), e12 & 2) {
    let n = ce();
    F(), Oe(n.errorMessage());
  }
}
function $m(e12, t) {
  e12 & 1 && (ao(0, "span", 7), W(1, " Run Query "));
}
function Um(e12, t) {
  e12 & 1 && W(0, " Run Query ");
}
function zm(e12, t) {
  if (e12 & 1) {
    let n = co();
    k(0, "div", 3)(1, "div", 4)(2, "p", 5), W(3), P(), k(4, "button", 6), Ae("click", function() {
      Te(n);
      let o = ce();
      return Me(o.handleRunQuery());
    }), bn(5, $m, 2, 0)(6, Um, 1, 0), P()()();
  }
  if (e12 & 2) {
    let n = ce();
    F(3), Oe(n.dryRunInfo()), F(), ae("disabled", n.isLoading()), F(), Cn(n.isLoading() ? 5 : 6);
  }
}
function Wm(e12, t) {
  if (e12 & 1 && (k(0, "option", 18), W(1), P()), e12 & 2) {
    let n = t.$implicit;
    ae("value", n), F(), Oe(n === 0 ? "All" : n);
  }
}
function Gm(e12, t) {
  if (e12 & 1 && (k(0, "option", 18), W(1), P()), e12 & 2) {
    let n = t.$implicit;
    ae("value", n), F(), Oe(n);
  }
}
function qm(e12, t) {
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
    }), io(17, Wm, 2, 2, "option", 18, oo), P()(), k(19, "div", 19)(20, "label", 20), W(21, "Page size:"), P(), k(22, "select", 21), Ae("change", function(o) {
      Te(n);
      let i = ce();
      return Me(i.handlePageSizeChange(o));
    }), io(23, Gm, 2, 2, "option", 18, oo), P()()()();
  }
  if (e12 & 2) {
    let n = ce();
    ae("innerHTML", n.sanitizedHtml(), Us), F(4), Oe(n.rowCountText()), F(2), ae("disabled", n.prevPageDisabled()), F(3), Oe(n.pageIndicatorText()), F(), ae("disabled", n.nextPageDisabled()), F(6), ae("value", n.maxColumns()), F(), so(n.maxColumnOptions), F(5), ae("value", n.pageSize()), F(), so(n.pageSizeOptions);
  }
}
var Eo = class e11 {
  state = E(vo);
  sanitizer = E(wa);
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
  tableContainerRef;
  isHeightInitialized = false;
  constructor() {
    $i(() => {
      let t = this.state.tableHtml(), n = this.state.sortContext(), r = this.state.orderableColumns();
      this.isDeferredMode() && (this.isHeightInitialized = false), setTimeout(() => {
        this.applySortIndicators(), this.lockInitialHeight();
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
    let i = this.getColumnName(o), s = this.state.orderableColumns();
    if (!i || !s.includes(i))
      return;
    let a = [...this.state.sortContext()], c = a.findIndex((u) => u.column === i), l = [...a];
    t.shiftKey ? c !== -1 ? l[c].ascending ? l[c] = R(x({}, l[c]), { ascending: false }) : l.splice(c, 1) : l.push({ column: i, ascending: true }) : c !== -1 && l.length === 1 ? l[c].ascending ? l[c] = R(x({}, l[c]), { ascending: false }) : l = [] : l = [{ column: i, ascending: true }], this.state.setSortContext(l);
  }
  getColumnName(t) {
    let n = t.cloneNode(true);
    return n.querySelector(".sort-indicator")?.remove(), n.textContent?.trim() || "";
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
      let c = this.getColumnName(a);
      if (c && n.includes(c)) {
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
  lockInitialHeight() {
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
  static \u0275cmp = na({ type: e11, selectors: [["", "app-root", ""]], viewQuery: function(n, r) {
    if (n & 1 && lo(Hm, 5), n & 2) {
      let o;
      aa(o = ca()) && (r.tableContainerRef = o.first);
    }
  }, attrs: Vm, decls: 4, vars: 4, consts: [["tableContainer", ""], [1, "bigframes-widget"], [1, "bigframes-error-message"], [1, "deferred-container"], [1, "deferred-card"], [1, "deferred-estimate"], [1, "run-query-button", 3, "click", "disabled"], [1, "spinner"], [1, "table-container", 3, "click", "innerHTML"], [1, "footer"], [1, "row-count"], [1, "pagination"], [3, "click", "disabled"], [1, "page-indicator"], [1, "settings"], [1, "max-columns"], ["for", "max-cols-select"], ["id", "max-cols-select", 3, "change", "value"], [3, "value"], [1, "page-size"], ["for", "page-size-select"], ["id", "page-size-select", 3, "change", "value"]], template: function(n, r) {
    n & 1 && (k(0, "div", 1), bn(1, Bm, 2, 1, "div", 2), bn(2, zm, 7, 3, "div", 3)(3, qm, 25, 7), P()), n & 2 && (uo("bigframes-dark-mode", r.isDarkMode()), F(), Cn(r.errorMessage() ? 1 : -1), F(), Cn(r.isDeferredMode() ? 2 : 3));
  }, styles: [".bigframes-widget.bigframes-widget[_ngcontent-%COMP%]{--bf-bg: white;--bf-border-color: #ccc;--bf-error-bg: #fbe;--bf-error-border: red;--bf-error-fg: black;--bf-fg: black;--bf-header-bg: #f5f5f5;--bf-null-fg: gray;--bf-row-even-bg: #f5f5f5;--bf-row-odd-bg: white;background-color:var(--bf-bg);box-sizing:border-box;color:var(--bf-fg);display:flex;flex-direction:column;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;margin:0;padding:0;width:100%}.bigframes-widget[_ngcontent-%COMP%]   *[_ngcontent-%COMP%]{box-sizing:border-box}@media(prefers-color-scheme:dark){.bigframes-widget.bigframes-widget[_ngcontent-%COMP%]{--bf-bg: var(--vscode-editor-background, #202124);--bf-border-color: #444;--bf-error-bg: #511;--bf-error-border: #f88;--bf-error-fg: #fcc;--bf-fg: white;--bf-header-bg: var(--vscode-editor-background, black);--bf-null-fg: #aaa;--bf-row-even-bg: #202124;--bf-row-odd-bg: #383838}}.bigframes-widget.bigframes-dark-mode.bigframes-dark-mode[_ngcontent-%COMP%]{--bf-bg: var(--vscode-editor-background, #202124);--bf-border-color: #444;--bf-error-bg: #511;--bf-error-border: #f88;--bf-error-fg: #fcc;--bf-fg: white;--bf-header-bg: var(--vscode-editor-background, black);--bf-null-fg: #aaa;--bf-row-even-bg: #202124;--bf-row-odd-bg: #383838}.bigframes-widget[_ngcontent-%COMP%]   .table-container[_ngcontent-%COMP%]{background-color:var(--bf-bg);margin:0;overflow:auto;padding:0}.bigframes-widget[_ngcontent-%COMP%]   .footer[_ngcontent-%COMP%]{align-items:center;background-color:var(--bf-bg);color:var(--bf-fg);display:flex;font-size:.8rem;justify-content:space-between;padding:8px}.bigframes-widget[_ngcontent-%COMP%]   .footer[_ngcontent-%COMP%] > *[_ngcontent-%COMP%]{flex:1}.bigframes-widget[_ngcontent-%COMP%]   .pagination[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:4px;justify-content:center;padding:4px}.bigframes-widget[_ngcontent-%COMP%]   .page-indicator[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .row-count[_ngcontent-%COMP%]{margin:0 8px}.bigframes-widget[_ngcontent-%COMP%]   .settings[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:16px;justify-content:end}.bigframes-widget[_ngcontent-%COMP%]   .page-size[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .max-columns[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:4px}.bigframes-widget[_ngcontent-%COMP%]   .page-size[_ngcontent-%COMP%]   label[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .max-columns[_ngcontent-%COMP%]   label[_ngcontent-%COMP%]{margin-right:8px}.bigframes-widget[_ngcontent-%COMP%]     table.bigframes-widget-table, .bigframes-widget[_ngcontent-%COMP%]     table.dataframe{background-color:var(--bf-bg);border:1px solid var(--bf-border-color);border-collapse:collapse;border-spacing:0;box-shadow:none;color:var(--bf-fg);margin:0;outline:none;text-align:left;width:auto}.bigframes-widget[_ngcontent-%COMP%]     tr{border:none}.bigframes-widget[_ngcontent-%COMP%]     th{background-color:var(--bf-header-bg);border:1px solid var(--bf-border-color);color:var(--bf-fg);padding:0;position:sticky;text-align:left;top:0;z-index:1}.bigframes-widget[_ngcontent-%COMP%]     td{border:1px solid var(--bf-border-color);color:var(--bf-fg);padding:.5em}.bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(odd), .bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(odd) td{background-color:var(--bf-row-odd-bg)}.bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(2n), .bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(2n) td{background-color:var(--bf-row-even-bg)}.bigframes-widget[_ngcontent-%COMP%]     .bf-header-content{box-sizing:border-box;height:100%;overflow:auto;padding:.5em;resize:horizontal;width:100%}.bigframes-widget[_ngcontent-%COMP%]     th .sort-indicator{padding-left:4px;visibility:hidden}.bigframes-widget[_ngcontent-%COMP%]     th:hover .sort-indicator{visibility:visible}.bigframes-widget[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]{background-color:transparent;border:1px solid currentColor;border-radius:4px;color:inherit;cursor:pointer;display:inline-block;padding:2px 8px;text-align:center;text-decoration:none;-webkit-user-select:none;user-select:none;vertical-align:middle}.bigframes-widget[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]:disabled{opacity:.65;pointer-events:none}.bigframes-widget[_ngcontent-%COMP%]   .bigframes-error-message[_ngcontent-%COMP%]{background-color:var(--bf-error-bg);border:1px solid var(--bf-error-border);border-radius:4px;color:var(--bf-error-fg);font-size:14px;margin-bottom:8px;padding:8px}.bigframes-widget[_ngcontent-%COMP%]     .cell-align-right{text-align:right}.bigframes-widget[_ngcontent-%COMP%]     .cell-align-left{text-align:left}.bigframes-widget[_ngcontent-%COMP%]     .null-value{color:var(--bf-null-fg)}.bigframes-widget[_ngcontent-%COMP%]     .debug-info{border-top:1px solid var(--bf-border-color)}.bigframes-widget[_ngcontent-%COMP%]   .deferred-container[_ngcontent-%COMP%]{align-items:center;display:flex;justify-content:center;min-height:220px;padding:24px;width:100%}.bigframes-widget[_ngcontent-%COMP%]   .deferred-card[_ngcontent-%COMP%]{background:linear-gradient(135deg,#fff9,#ffffff4d);border:1px solid rgba(255,255,255,.4);border-radius:16px;box-shadow:0 8px 32px #1f268712;display:flex;flex-direction:column;gap:16px;max-width:500px;padding:32px;text-align:center;transition:all .3s ease-in-out}.bigframes-widget.bigframes-dark-mode[_ngcontent-%COMP%]   .deferred-card[_ngcontent-%COMP%]{background:linear-gradient(135deg,#20212499,#2021244d);border:1px solid rgba(255,255,255,.1);box-shadow:0 8px 32px #0000004d}@media(prefers-color-scheme:dark){.bigframes-widget[_ngcontent-%COMP%]   .deferred-card[_ngcontent-%COMP%]{background:linear-gradient(135deg,#20212499,#2021244d);border:1px solid rgba(255,255,255,.1);box-shadow:0 8px 32px #0000004d}}.bigframes-widget[_ngcontent-%COMP%]   .deferred-title[_ngcontent-%COMP%]{font-size:1.1rem;font-weight:600;margin:0}.bigframes-widget[_ngcontent-%COMP%]   .deferred-estimate[_ngcontent-%COMP%]{color:var(--bf-null-fg);font-size:.9rem;margin:0}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]{align-items:center;background-color:var(--bf-fg);border:1px solid var(--bf-fg);border-radius:8px;color:var(--bf-bg);cursor:pointer;display:inline-flex;font-size:14px;font-weight:600;gap:8px;justify-content:center;padding:10px 20px;transition:transform .2s ease,opacity .2s ease}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]:hover{opacity:.9;transform:translateY(-1px)}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]:active{transform:translateY(0)}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]:disabled{cursor:not-allowed;opacity:.6}.bigframes-widget[_ngcontent-%COMP%]   .spinner[_ngcontent-%COMP%]{animation:_ngcontent-%COMP%_spin 1s linear infinite;border:2px solid currentColor;border-radius:50%;border-top-color:transparent;display:inline-block;height:12px;width:12px}@keyframes _ngcontent-%COMP%_spin{to{transform:rotate(360deg)}}"] });
};
function Zm({ model: e12, el: t }) {
  let n = document.createElement("div");
  n.setAttribute("app-root", ""), t.appendChild(n);
  let r = { providers: [Vi(), ua(), { provide: "ANYWIDGET_MODEL", useValue: e12 }] };
  Ca(r).then((o) => {
    o.bootstrap(Eo, n), n.removeAttribute("app-root");
  }).catch((o) => console.error(o));
}
var sS = { render: Zm };
export {
  sS as default
};
