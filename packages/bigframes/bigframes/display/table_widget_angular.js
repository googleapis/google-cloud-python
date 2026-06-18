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
var yd = Object.defineProperty;
var vd = Object.defineProperties;
var Ed = Object.getOwnPropertyDescriptors;
var Oa = Object.getOwnPropertySymbols;
var Id = Object.prototype.hasOwnProperty;
var Dd = Object.prototype.propertyIsEnumerable;
var ka = (e12, t, n) => t in e12 ? yd(e12, t, { enumerable: true, configurable: true, writable: true, value: n }) : e12[t] = n;
var A = (e12, t) => {
  for (var n in t ||= {})
    Id.call(t, n) && ka(e12, n, t[n]);
  if (Oa)
    for (var n of Oa(t))
      Dd.call(t, n) && ka(e12, n, t[n]);
  return e12;
};
var O = (e12, t) => vd(e12, Ed(t));
var V = null;
var Ln = false;
var _o = 1;
var bd = null;
var K = Symbol("SIGNAL");
function g(e12) {
  let t = V;
  return V = e12, t;
}
function jn() {
  return V;
}
var mt = { version: 0, lastCleanEpoch: 0, dirty: false, producers: void 0, producersTail: void 0, consumers: void 0, consumersTail: void 0, recomputing: false, consumerAllowSignalWrites: false, consumerIsAlwaysLive: false, kind: "unknown", producerMustRecompute: () => false, producerRecomputeValue: () => {
}, consumerMarkedDirty: () => {
}, consumerOnSignalRead: () => {
} };
function So(e12) {
  if (Ln)
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
  if (o !== void 0 && o.consumer === V && (!r || wd(o, V)))
    return;
  let i = vt(V), s = { producer: e12, consumer: V, nextProducer: n, prevConsumer: o, lastReadVersion: e12.version, nextConsumer: void 0 };
  V.producersTail = s, t !== void 0 ? t.nextProducer = s : V.producers = s, i && ja(e12, s);
}
function Pa() {
  _o++;
}
function No(e12) {
  if (!(vt(e12) && !e12.dirty) && !(!e12.dirty && e12.lastCleanEpoch === _o)) {
    if (!e12.producerMustRecompute(e12) && !Vn(e12)) {
      Mo(e12);
      return;
    }
    e12.producerRecomputeValue(e12), Mo(e12);
  }
}
function xo(e12) {
  if (e12.consumers === void 0)
    return;
  let t = Ln;
  Ln = true;
  try {
    for (let n = e12.consumers; n !== void 0; n = n.nextConsumer) {
      let r = n.consumer;
      r.dirty || Cd(r);
    }
  } finally {
    Ln = t;
  }
}
function Ro() {
  return V?.consumerAllowSignalWrites !== false;
}
function Cd(e12) {
  e12.dirty = true, xo(e12), e12.consumerMarkedDirty?.(e12);
}
function Mo(e12) {
  e12.dirty = false, e12.lastCleanEpoch = _o;
}
function Gt(e12) {
  return e12 && La(e12), g(e12);
}
function La(e12) {
  e12.producersTail = void 0, e12.recomputing = true;
}
function Hn(e12, t) {
  g(t), e12 && Fa(e12);
}
function Fa(e12) {
  e12.recomputing = false;
  let t = e12.producersTail, n = t !== void 0 ? t.nextProducer : e12.producers;
  if (n !== void 0) {
    if (vt(e12))
      do
        n = Ao(n);
      while (n !== void 0);
    t !== void 0 ? t.nextProducer = void 0 : e12.producers = void 0;
  }
}
function Vn(e12) {
  for (let t = e12.producers; t !== void 0; t = t.nextProducer) {
    let n = t.producer, r = t.lastReadVersion;
    if (r !== n.version || (No(n), r !== n.version))
      return true;
  }
  return false;
}
function yt(e12) {
  if (vt(e12)) {
    let t = e12.producers;
    for (; t !== void 0; )
      t = Ao(t);
  }
  e12.producers = void 0, e12.producersTail = void 0, e12.consumers = void 0, e12.consumersTail = void 0;
}
function ja(e12, t) {
  let n = e12.consumersTail, r = vt(e12);
  if (n !== void 0 ? (t.nextConsumer = n.nextConsumer, n.nextConsumer = t) : (t.nextConsumer = void 0, e12.consumers = t), t.prevConsumer = n, e12.consumersTail = t, !r)
    for (let o = e12.producers; o !== void 0; o = o.nextProducer)
      ja(o.producer, o);
}
function Ao(e12) {
  let t = e12.producer, n = e12.nextProducer, r = e12.nextConsumer, o = e12.prevConsumer;
  if (e12.nextConsumer = void 0, e12.prevConsumer = void 0, r !== void 0 ? r.prevConsumer = o : t.consumersTail = o, o !== void 0)
    o.nextConsumer = r;
  else if (t.consumers = r, !vt(t)) {
    let i = t.producers;
    for (; i !== void 0; )
      i = Ao(i);
  }
  return n;
}
function vt(e12) {
  return e12.consumerIsAlwaysLive || e12.consumers !== void 0;
}
function Oo(e12) {
  bd?.(e12);
}
function wd(e12, t) {
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
function ko(e12, t) {
  return Object.is(e12, t);
}
function Bn(e12, t) {
  let n = Object.create(Td);
  n.computation = e12, t !== void 0 && (n.equal = t);
  let r = () => {
    if (No(n), So(n), n.value === Fn)
      throw n.error;
    return n.value;
  };
  return r[K] = n, Oo(n), r;
}
var wo = Symbol("UNSET");
var To = Symbol("COMPUTING");
var Fn = Symbol("ERRORED");
var Td = O(A({}, mt), { value: wo, dirty: true, error: null, equal: ko, kind: "computed", producerMustRecompute(e12) {
  return e12.value === wo || e12.value === To;
}, producerRecomputeValue(e12) {
  if (e12.value === To)
    throw new Error("");
  let t = e12.value;
  e12.value = To;
  let n = Gt(e12), r, o = false;
  try {
    r = e12.computation(), g(null), o = t !== wo && t !== Fn && r !== Fn && e12.equal(t, r);
  } catch (i) {
    r = Fn, e12.error = i;
  } finally {
    Hn(e12, n);
  }
  if (o) {
    e12.value = t;
    return;
  }
  e12.value = r, e12.version++;
} });
function Md() {
  throw new Error();
}
var Ha = Md;
function Va(e12) {
  Ha(e12);
}
function Po(e12) {
  Ha = e12;
}
var _d = null;
function Lo(e12, t) {
  let n = Object.create(Ua);
  n.value = e12, t !== void 0 && (n.equal = t);
  let r = () => Ba(n);
  return r[K] = n, Oo(n), [r, (s) => Fo(n, s), (s) => $a(n, s)];
}
function Ba(e12) {
  return So(e12), e12.value;
}
function Fo(e12, t) {
  Ro() || Va(e12), e12.equal(e12.value, t) || (e12.value = t, Sd(e12));
}
function $a(e12, t) {
  Ro() || Va(e12), Fo(e12, t(e12.value));
}
var Ua = O(A({}, mt), { equal: ko, value: void 0, kind: "signal" });
function Sd(e12) {
  e12.version++, Pa(), xo(e12), _d?.(e12);
}
var jo = O(A({}, mt), { consumerIsAlwaysLive: true, consumerAllowSignalWrites: true, dirty: true, kind: "effect" });
function Ho(e12) {
  if (e12.dirty = false, e12.version > 0 && !Vn(e12))
    return;
  e12.version++;
  let t = Gt(e12);
  try {
    e12.cleanup(), e12.fn();
  } finally {
    Hn(e12, t);
  }
}
function z(e12) {
  return typeof e12 == "function";
}
function $n(e12) {
  let n = e12((r) => {
    Error.call(r), r.stack = new Error().stack;
  });
  return n.prototype = Object.create(Error.prototype), n.prototype.constructor = n, n;
}
var Un = $n((e12) => function(n) {
  e12(this), this.message = n ? `${n.length} errors occurred during unsubscription:
${n.map((r, o) => `${o + 1}) ${r.toString()}`).join(`
  `)}` : "", this.name = "UnsubscriptionError", this.errors = n;
});
function qt(e12, t) {
  if (e12) {
    let n = e12.indexOf(t);
    0 <= n && e12.splice(n, 1);
  }
}
var U = class e {
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
      if (z(r))
        try {
          r();
        } catch (i) {
          t = i instanceof Un ? i.errors : [i];
        }
      let { _finalizers: o } = this;
      if (o) {
        this._finalizers = null;
        for (let i of o)
          try {
            za(i);
          } catch (s) {
            t = t ?? [], s instanceof Un ? t = [...t, ...s.errors] : t.push(s);
          }
      }
      if (t)
        throw new Un(t);
    }
  }
  add(t) {
    var n;
    if (t && t !== this)
      if (this.closed)
        za(t);
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
    n === t ? this._parentage = null : Array.isArray(n) && qt(n, t);
  }
  remove(t) {
    let { _finalizers: n } = this;
    n && qt(n, t), t instanceof e && t._removeParent(this);
  }
};
U.EMPTY = (() => {
  let e12 = new U();
  return e12.closed = true, e12;
})();
var Vo = U.EMPTY;
function zn(e12) {
  return e12 instanceof U || e12 && "closed" in e12 && z(e12.remove) && z(e12.add) && z(e12.unsubscribe);
}
function za(e12) {
  z(e12) ? e12() : e12.unsubscribe();
}
var oe = { onUnhandledError: null, onStoppedNotification: null, Promise: void 0, useDeprecatedSynchronousErrorHandling: false, useDeprecatedNextContext: false };
var Et = { setTimeout(e12, t, ...n) {
  let { delegate: r } = Et;
  return r?.setTimeout ? r.setTimeout(e12, t, ...n) : setTimeout(e12, t, ...n);
}, clearTimeout(e12) {
  let { delegate: t } = Et;
  return (t?.clearTimeout || clearTimeout)(e12);
}, delegate: void 0 };
function Wa(e12) {
  Et.setTimeout(() => {
    let { onUnhandledError: t } = oe;
    if (t)
      t(e12);
    else
      throw e12;
  });
}
function Bo() {
}
var Ga = $o("C", void 0, void 0);
function qa(e12) {
  return $o("E", void 0, e12);
}
function Za(e12) {
  return $o("N", e12, void 0);
}
function $o(e12, t, n) {
  return { kind: e12, value: t, error: n };
}
var qe = null;
function It(e12) {
  if (oe.useDeprecatedSynchronousErrorHandling) {
    let t = !qe;
    if (t && (qe = { errorThrown: false, error: null }), e12(), t) {
      let { errorThrown: n, error: r } = qe;
      if (qe = null, n)
        throw r;
    }
  } else
    e12();
}
function Qa(e12) {
  oe.useDeprecatedSynchronousErrorHandling && qe && (qe.errorThrown = true, qe.error = e12);
}
var Ze = class extends U {
  constructor(t) {
    super(), this.isStopped = false, t ? (this.destination = t, zn(t) && t.add(this)) : this.destination = Rd;
  }
  static create(t, n, r) {
    return new Dt(t, n, r);
  }
  next(t) {
    this.isStopped ? zo(Za(t), this) : this._next(t);
  }
  error(t) {
    this.isStopped ? zo(qa(t), this) : (this.isStopped = true, this._error(t));
  }
  complete() {
    this.isStopped ? zo(Ga, this) : (this.isStopped = true, this._complete());
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
var Nd = Function.prototype.bind;
function Uo(e12, t) {
  return Nd.call(e12, t);
}
var Wo = class {
  constructor(t) {
    this.partialObserver = t;
  }
  next(t) {
    let { partialObserver: n } = this;
    if (n.next)
      try {
        n.next(t);
      } catch (r) {
        Wn(r);
      }
  }
  error(t) {
    let { partialObserver: n } = this;
    if (n.error)
      try {
        n.error(t);
      } catch (r) {
        Wn(r);
      }
    else
      Wn(t);
  }
  complete() {
    let { partialObserver: t } = this;
    if (t.complete)
      try {
        t.complete();
      } catch (n) {
        Wn(n);
      }
  }
};
var Dt = class extends Ze {
  constructor(t, n, r) {
    super();
    let o;
    if (z(t) || !t)
      o = { next: t ?? void 0, error: n ?? void 0, complete: r ?? void 0 };
    else {
      let i;
      this && oe.useDeprecatedNextContext ? (i = Object.create(t), i.unsubscribe = () => this.unsubscribe(), o = { next: t.next && Uo(t.next, i), error: t.error && Uo(t.error, i), complete: t.complete && Uo(t.complete, i) }) : o = t;
    }
    this.destination = new Wo(o);
  }
};
function Wn(e12) {
  oe.useDeprecatedSynchronousErrorHandling ? Qa(e12) : Wa(e12);
}
function xd(e12) {
  throw e12;
}
function zo(e12, t) {
  let { onStoppedNotification: n } = oe;
  n && Et.setTimeout(() => n(e12, t));
}
var Rd = { closed: true, next: Bo, error: xd, complete: Bo };
var Ya = typeof Symbol == "function" && Symbol.observable || "@@observable";
function Ka(e12) {
  return e12;
}
function Ja(e12) {
  return e12.length === 0 ? Ka : e12.length === 1 ? e12[0] : function(n) {
    return e12.reduce((r, o) => o(r), n);
  };
}
var bt = (() => {
  class e12 {
    constructor(n) {
      n && (this._subscribe = n);
    }
    lift(n) {
      let r = new e12();
      return r.source = this, r.operator = n, r;
    }
    subscribe(n, r, o) {
      let i = Od(n) ? n : new Dt(n, r, o);
      return It(() => {
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
      return r = Xa(r), new r((o, i) => {
        let s = new Dt({ next: (a) => {
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
    [Ya]() {
      return this;
    }
    pipe(...n) {
      return Ja(n)(this);
    }
    toPromise(n) {
      return n = Xa(n), new n((r, o) => {
        let i;
        this.subscribe((s) => i = s, (s) => o(s), () => r(i));
      });
    }
  }
  return e12.create = (t) => new e12(t), e12;
})();
function Xa(e12) {
  var t;
  return (t = e12 ?? oe.Promise) !== null && t !== void 0 ? t : Promise;
}
function Ad(e12) {
  return e12 && z(e12.next) && z(e12.error) && z(e12.complete);
}
function Od(e12) {
  return e12 && e12 instanceof Ze || Ad(e12) && zn(e12);
}
function kd(e12) {
  return z(e12?.lift);
}
function ec(e12) {
  return (t) => {
    if (kd(t))
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
function tc(e12, t, n, r, o) {
  return new Go(e12, t, n, r, o);
}
var Go = class extends Ze {
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
var nc = $n((e12) => function() {
  e12(this), this.name = "ObjectUnsubscribedError", this.message = "object unsubscribed";
});
var Ee = (() => {
  class e12 extends bt {
    constructor() {
      super(), this.closed = false, this.currentObservers = null, this.observers = [], this.isStopped = false, this.hasError = false, this.thrownError = null;
    }
    lift(n) {
      let r = new Gn(this, this);
      return r.operator = n, r;
    }
    _throwIfClosed() {
      if (this.closed)
        throw new nc();
    }
    next(n) {
      It(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.currentObservers || (this.currentObservers = Array.from(this.observers));
          for (let r of this.currentObservers)
            r.next(n);
        }
      });
    }
    error(n) {
      It(() => {
        if (this._throwIfClosed(), !this.isStopped) {
          this.hasError = this.isStopped = true, this.thrownError = n;
          let { observers: r } = this;
          for (; r.length; )
            r.shift().error(n);
        }
      });
    }
    complete() {
      It(() => {
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
      return r || o ? Vo : (this.currentObservers = null, i.push(n), new U(() => {
        this.currentObservers = null, qt(i, n);
      }));
    }
    _checkFinalizedStatuses(n) {
      let { hasError: r, thrownError: o, isStopped: i } = this;
      r ? n.error(o) : i && n.complete();
    }
    asObservable() {
      let n = new bt();
      return n.source = this, n;
    }
  }
  return e12.create = (t, n) => new Gn(t, n), e12;
})();
var Gn = class extends Ee {
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
    return (r = (n = this.source) === null || n === void 0 ? void 0 : n.subscribe(t)) !== null && r !== void 0 ? r : Vo;
  }
};
var Zt = class extends Ee {
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
function qo(e12, t) {
  return ec((n, r) => {
    let o = 0;
    n.subscribe(tc(r, (i) => {
      r.next(e12.call(t, i, o++));
    }));
  });
}
var Zo;
function qn() {
  return Zo;
}
function de(e12) {
  let t = Zo;
  return Zo = e12, t;
}
var rc = Symbol("NotFound");
function Ct(e12) {
  return e12 === rc || e12?.name === "\u0275NotFound";
}
var er = "https://angular.dev/best-practices/security#preventing-cross-site-scripting-xss";
var v = class extends Error {
  code;
  constructor(t, n) {
    super(tr(t, n)), this.code = t;
  }
};
function Pd(e12) {
  return `NG0${Math.abs(e12)}`;
}
function tr(e12, t) {
  return `${Pd(e12)}${t ? ": " + t : ""}`;
}
var je = globalThis;
function w(e12) {
  for (let t in e12)
    if (e12[t] === w)
      return t;
  throw Error("");
}
function nr(e12) {
  if (typeof e12 == "string")
    return e12;
  if (Array.isArray(e12))
    return `[${e12.map(nr).join(", ")}]`;
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
function ci(e12, t) {
  return e12 ? t ? `${e12} ${t}` : e12 : t || "";
}
var Ld = w({ __forward_ref__: w });
function rr(e12) {
  return e12.__forward_ref__ = rr, e12;
}
function B(e12) {
  return cc(e12) ? e12() : e12;
}
function cc(e12) {
  return typeof e12 == "function" && e12.hasOwnProperty(Ld) && e12.__forward_ref__ === rr;
}
function _(e12) {
  return { token: e12.token, providedIn: e12.providedIn || null, factory: e12.factory, value: void 0 };
}
function or(e12) {
  return Fd(e12, ir);
}
function Fd(e12, t) {
  return e12.hasOwnProperty(t) && e12[t] || null;
}
function jd(e12) {
  let t = e12?.[ir] ?? null;
  return t || null;
}
function Yo(e12) {
  return e12 && e12.hasOwnProperty(Qn) ? e12[Qn] : null;
}
var ir = w({ \u0275prov: w });
var Qn = w({ \u0275inj: w });
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
function li(e12) {
  return e12 && !!e12.\u0275providers;
}
var ui = w({ \u0275cmp: w });
var di = w({ \u0275dir: w });
var fi = w({ \u0275pipe: w });
var Ko = w({ \u0275fac: w });
var et = w({ __NG_ELEMENT_ID__: w });
var oc = w({ __NG_ENV_ID__: w });
function tt(e12) {
  return hi(e12, "@Component"), e12[ui] || null;
}
function pi(e12) {
  return hi(e12, "@Directive"), e12[di] || null;
}
function lc(e12) {
  return hi(e12, "@Pipe"), e12[fi] || null;
}
function hi(e12, t) {
  if (e12 == null)
    throw new v(-919, false);
}
function gi(e12) {
  return typeof e12 == "string" ? e12 : e12 == null ? "" : String(e12);
}
var uc = w({ ngErrorCode: w });
var Hd = w({ ngErrorMessage: w });
var Vd = w({ ngTokenPath: w });
function mi(e12, t) {
  return dc("", -200, t);
}
function sr(e12, t) {
  throw new v(-201, false);
}
function dc(e12, t, n) {
  let r = new v(t, e12);
  return r[uc] = t, r[Hd] = e12, n && (r[Vd] = n), r;
}
function Bd(e12) {
  return e12[uc];
}
var Jo;
function fc() {
  return Jo;
}
function q(e12) {
  let t = Jo;
  return Jo = e12, t;
}
function yi(e12, t, n) {
  let r = or(e12);
  if (r && r.providedIn == "root")
    return r.value === void 0 ? r.value = r.factory() : r.value;
  if (n & 8)
    return null;
  if (t !== void 0)
    return t;
  sr(e12, "");
}
var $d = {};
var Qe = $d;
var Ud = "__NG_DI_FLAG__";
var Xo = class {
  injector;
  constructor(t) {
    this.injector = t;
  }
  retrieve(t, n) {
    let r = Ye(n) || 0;
    try {
      return this.injector.get(t, r & 8 ? null : Qe, r);
    } catch (o) {
      if (Ct(o))
        return o;
      throw o;
    }
  }
};
function zd(e12, t = 0) {
  let n = qn();
  if (n === void 0)
    throw new v(-203, false);
  if (n === null)
    return yi(e12, void 0, t);
  {
    let r = Wd(t), o = n.retrieve(e12, r);
    if (Ct(o)) {
      if (r.optional)
        return null;
      throw o;
    }
    return o;
  }
}
function b(e12, t = 0) {
  return (fc() || zd)(B(e12), t);
}
function E(e12, t) {
  return b(e12, Ye(t));
}
function Ye(e12) {
  return typeof e12 > "u" || typeof e12 == "number" ? e12 : 0 | (e12.optional && 8) | (e12.host && 1) | (e12.self && 2) | (e12.skipSelf && 4);
}
function Wd(e12) {
  return { optional: !!(e12 & 8), host: !!(e12 & 1), self: !!(e12 & 2), skipSelf: !!(e12 & 4) };
}
function ei(e12) {
  let t = [];
  for (let n = 0; n < e12.length; n++) {
    let r = B(e12[n]);
    if (Array.isArray(r)) {
      if (r.length === 0)
        throw new v(900, false);
      let o, i = 0;
      for (let s = 0; s < r.length; s++) {
        let a = r[s], c = Gd(a);
        typeof c == "number" ? c === -1 ? o = a.token : i |= c : o = a;
      }
      t.push(b(o, i));
    } else
      t.push(b(r));
  }
  return t;
}
function Gd(e12) {
  return e12[Ud];
}
function Tt(e12, t) {
  let n = e12.hasOwnProperty(Ko);
  return n ? e12[Ko] : null;
}
function pc(e12, t, n) {
  if (e12.length !== t.length)
    return false;
  for (let r = 0; r < e12.length; r++) {
    let o = e12[r], i = t[r];
    if (n && (o = n(o), i = n(i)), i !== o)
      return false;
  }
  return true;
}
function hc(e12) {
  return e12.flat(Number.POSITIVE_INFINITY);
}
function ar(e12, t) {
  e12.forEach((n) => Array.isArray(n) ? ar(n, t) : t(n));
}
function vi(e12, t, n) {
  t >= e12.length ? e12.push(n) : e12.splice(t, 0, n);
}
function en(e12, t) {
  return t >= e12.length - 1 ? e12.pop() : e12.splice(t, 1)[0];
}
function gc(e12, t, n, r) {
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
function mc(e12, t, n) {
  let r = Mt(e12, t);
  return r >= 0 ? e12[r | 1] = n : (r = ~r, gc(e12, r, t, n)), r;
}
function cr(e12, t) {
  let n = Mt(e12, t);
  if (n >= 0)
    return e12[n | 1];
}
function Mt(e12, t) {
  return qd(e12, t, 1);
}
function qd(e12, t, n) {
  let r = 0, o = e12.length >> n;
  for (; o !== r; ) {
    let i = r + (o - r >> 1), s = e12[i << n];
    if (t === s)
      return i << n;
    s > t ? o = i : r = i + 1;
  }
  return ~(o << n);
}
var nt = {};
var Pe = [];
var rt = new D("");
var Ei = new D("", -1);
var Ii = new D("");
var Yt = class {
  get(t, n = Qe) {
    if (n === Qe) {
      let o = dc("", -201);
      throw o.name = "\u0275NotFound", o;
    }
    return n;
  }
};
function _t(e12) {
  return { \u0275providers: e12 };
}
function yc(e12) {
  return _t([{ provide: rt, multi: true, useValue: e12 }]);
}
function vc(...e12) {
  return { \u0275providers: Di(true, e12), \u0275fromNgModule: true };
}
function Di(e12, ...t) {
  let n = [], r = /* @__PURE__ */ new Set(), o, i = (s) => {
    n.push(s);
  };
  return ar(t, (s) => {
    let a = s;
    Yn(a, i, [], r) && (o ||= [], o.push(a));
  }), o !== void 0 && Ec(o, i), n;
}
function Ec(e12, t) {
  for (let n = 0; n < e12.length; n++) {
    let { ngModule: r, providers: o } = e12[n];
    bi(o, (i) => {
      t(i, r);
    });
  }
}
function Yn(e12, t, n, r) {
  if (e12 = B(e12), !e12)
    return false;
  let o = null, i = Yo(e12), s = !i && tt(e12);
  if (!i && !s) {
    let c = e12.ngModule;
    if (i = Yo(c), i)
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
        Yn(l, t, n, r);
    }
  } else if (i) {
    if (i.imports != null && !a) {
      r.add(o);
      let l;
      ar(i.imports, (u) => {
        Yn(u, t, n, r) && (l ||= [], l.push(u));
      }), l !== void 0 && Ec(l, t);
    }
    if (!a) {
      let l = Tt(o) || (() => new o());
      t({ provide: o, useFactory: l, deps: Pe }, o), t({ provide: Ii, useValue: o, multi: true }, o), t({ provide: rt, useValue: () => b(o), multi: true }, o);
    }
    let c = i.providers;
    if (c != null && !a) {
      let l = e12;
      bi(c, (u) => {
        t(u, l);
      });
    }
  } else
    return false;
  return o !== e12 && e12.providers !== void 0;
}
function bi(e12, t) {
  for (let n of e12)
    li(n) && (n = n.\u0275providers), Array.isArray(n) ? bi(n, t) : t(n);
}
var Zd = w({ provide: String, useValue: w });
function Ic(e12) {
  return e12 !== null && typeof e12 == "object" && Zd in e12;
}
function Qd(e12) {
  return !!(e12 && e12.useExisting);
}
function Yd(e12) {
  return !!(e12 && e12.useFactory);
}
function Ke(e12) {
  return typeof e12 == "function";
}
function Dc(e12) {
  return !!e12.useClass;
}
var tn = new D("");
var Zn = {};
var ic = {};
var Qo;
function nn() {
  return Qo === void 0 && (Qo = new Yt()), Qo;
}
var J = class {
};
var Je = class extends J {
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
    super(), this.parent = n, this.source = r, this.scopes = o, ni(t, (s) => this.processProvider(s)), this.records.set(Ei, wt(void 0, this)), o.has("environment") && this.records.set(J, wt(void 0, this));
    let i = this.records.get(tn);
    i != null && typeof i.value == "string" && this.scopes.add(i.value), this.injectorDefTypes = new Set(this.get(Ii, Pe, { self: true }));
  }
  retrieve(t, n) {
    let r = Ye(n) || 0;
    try {
      return this.get(t, Qe, r);
    } catch (o) {
      if (Ct(o))
        return o;
      throw o;
    }
  }
  destroy() {
    Qt(this), this._destroyed = true;
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
    return Qt(this), this._onDestroyHooks.push(t), () => this.removeOnDestroy(t);
  }
  runInContext(t) {
    Qt(this);
    let n = de(this), r = q(void 0), o;
    try {
      return t();
    } finally {
      de(n), q(r);
    }
  }
  get(t, n = Qe, r) {
    if (Qt(this), t.hasOwnProperty(oc))
      return t[oc](this);
    let o = Ye(r), i, s = de(this), a = q(void 0);
    try {
      if (!(o & 4)) {
        let l = this.records.get(t);
        if (l === void 0) {
          let u = tf(t) && or(t);
          u && this.injectableDefInScope(u) ? l = wt(ti(t), Zn) : l = null, this.records.set(t, l);
        }
        if (l != null)
          return this.hydrate(t, l, o);
      }
      let c = o & 2 ? nn() : this.parent;
      return n = o & 8 && n === Qe ? null : n, c.get(t, n);
    } catch (c) {
      let l = Bd(c);
      throw l === -200 || l === -201 ? new v(l, null) : c;
    } finally {
      q(a), de(s);
    }
  }
  resolveInjectorInitializers() {
    let t = g(null), n = de(this), r = q(void 0), o;
    try {
      let i = this.get(rt, Pe, { self: true });
      for (let s of i)
        s();
    } finally {
      de(n), q(r), g(t);
    }
  }
  toString() {
    return "R3Injector[...]";
  }
  processProvider(t) {
    t = B(t);
    let n = Ke(t) ? t : B(t && t.provide), r = Jd(t);
    if (!Ke(t) && t.multi === true) {
      let o = this.records.get(n);
      o || (o = wt(void 0, Zn, true), o.factory = () => ei(o.multi), this.records.set(n, o)), n = t, o.multi.push(t);
    }
    this.records.set(n, r);
  }
  hydrate(t, n, r) {
    let o = g(null);
    try {
      if (n.value === ic)
        throw mi("");
      return n.value === Zn && (n.value = ic, n.value = n.factory(void 0, r)), typeof n.value == "object" && n.value && ef(n.value) && this._ngOnDestroyHooks.add(n.value), n.value;
    } finally {
      g(o);
    }
  }
  injectableDefInScope(t) {
    if (!t.providedIn)
      return false;
    let n = B(t.providedIn);
    return typeof n == "string" ? n === "any" || this.scopes.has(n) : this.injectorDefTypes.has(n);
  }
  removeOnDestroy(t) {
    let n = this._onDestroyHooks.indexOf(t);
    n !== -1 && this._onDestroyHooks.splice(n, 1);
  }
};
function ti(e12) {
  let t = or(e12), n = t !== null ? t.factory : Tt(e12);
  if (n !== null)
    return n;
  if (e12 instanceof D)
    throw new v(-204, false);
  if (e12 instanceof Function)
    return Kd(e12);
  throw new v(-204, false);
}
function Kd(e12) {
  if (e12.length > 0)
    throw new v(-204, false);
  let n = jd(e12);
  return n !== null ? () => n.factory(e12) : () => new e12();
}
function Jd(e12) {
  if (Ic(e12))
    return wt(void 0, e12.useValue);
  {
    let t = Ci(e12);
    return wt(t, Zn);
  }
}
function Ci(e12, t, n) {
  let r;
  if (Ke(e12)) {
    let o = B(e12);
    return Tt(o) || ti(o);
  } else if (Ic(e12))
    r = () => B(e12.useValue);
  else if (Yd(e12))
    r = () => e12.useFactory(...ei(e12.deps || []));
  else if (Qd(e12))
    r = (o, i) => b(B(e12.useExisting), i !== void 0 && i & 8 ? 8 : void 0);
  else {
    let o = B(e12 && (e12.useClass || e12.provide));
    if (Xd(e12))
      r = () => new o(...ei(e12.deps));
    else
      return Tt(o) || ti(o);
  }
  return r;
}
function Qt(e12) {
  if (e12.destroyed)
    throw new v(-205, false);
}
function wt(e12, t, n = false) {
  return { factory: e12, value: t, multi: n ? [] : void 0 };
}
function Xd(e12) {
  return !!e12.deps;
}
function ef(e12) {
  return e12 !== null && typeof e12 == "object" && typeof e12.ngOnDestroy == "function";
}
function tf(e12) {
  return typeof e12 == "function" || typeof e12 == "object" && e12.ngMetadataName === "InjectionToken";
}
function ni(e12, t) {
  for (let n of e12)
    Array.isArray(n) ? ni(n, t) : n && li(n) ? ni(n.\u0275providers, t) : t(n);
}
function lr(e12, t) {
  let n;
  e12 instanceof Je ? (Qt(e12), n = e12) : n = new Xo(e12);
  let r, o = de(n), i = q(void 0);
  try {
    return t();
  } finally {
    de(o), q(i);
  }
}
function bc() {
  return fc() !== void 0 || qn() != null;
}
var ie = 0;
var m = 1;
var y = 2;
var k = 3;
var ee = 4;
var te = 5;
var St = 6;
var Nt = 7;
var N = 8;
var Ce = 9;
var pe = 10;
var P = 11;
var xt = 12;
var wi = 13;
var ot = 14;
var ne = 15;
var He = 16;
var it = 17;
var he = 18;
var we = 19;
var Ti = 20;
var De = 21;
var ur = 22;
var Le = 23;
var Z = 24;
var dr = 25;
var Ve = 26;
var $ = 27;
var Cc = 1;
var Mi = 6;
var Be = 7;
var rn = 8;
var st = 9;
var S = 10;
function $e(e12) {
  return Array.isArray(e12) && typeof e12[Cc] == "object";
}
function se(e12) {
  return Array.isArray(e12) && e12[Cc] === true;
}
function _i(e12) {
  return (e12.flags & 4) !== 0;
}
function Rt(e12) {
  return e12.componentOffset > -1;
}
function Si(e12) {
  return (e12.flags & 1) === 1;
}
function at(e12) {
  return !!e12.template;
}
function At(e12) {
  return (e12[y] & 512) !== 0;
}
function ct(e12) {
  return (e12[y] & 256) === 256;
}
var wc = "svg";
var Tc = "math";
function re(e12) {
  for (; Array.isArray(e12); )
    e12 = e12[ie];
  return e12;
}
function Ni(e12, t) {
  return re(t[e12]);
}
function ge(e12, t) {
  return re(t[e12.index]);
}
function fr(e12, t) {
  return e12.data[t];
}
function Te(e12, t) {
  let n = t[e12];
  return $e(n) ? n : n[ie];
}
function Mc(e12) {
  return (e12[y] & 4) === 4;
}
function pr(e12) {
  return (e12[y] & 128) === 128;
}
function _c(e12) {
  return se(e12[k]);
}
function me(e12, t) {
  return t == null ? null : e12[t];
}
function xi(e12) {
  e12[it] = 0;
}
function Ri(e12) {
  e12[y] & 1024 || (e12[y] |= 1024, pr(e12) && Ot(e12));
}
function Sc(e12, t) {
  for (; e12 > 0; )
    t = t[ot], e12--;
  return t;
}
function on(e12) {
  return !!(e12[y] & 9216 || e12[Z]?.dirty);
}
function hr(e12) {
  e12[pe].changeDetectionScheduler?.notify(8), e12[y] & 64 && (e12[y] |= 1024), on(e12) && Ot(e12);
}
function Ot(e12) {
  e12[pe].changeDetectionScheduler?.notify(0);
  let t = Fe(e12);
  for (; t !== null && !(t[y] & 8192 || (t[y] |= 8192, !pr(t))); )
    t = Fe(t);
}
function Ai(e12, t) {
  if (ct(e12))
    throw new v(911, false);
  e12[De] === null && (e12[De] = []), e12[De].push(t);
}
function Nc(e12, t) {
  if (e12[De] === null)
    return;
  let n = e12[De].indexOf(t);
  n !== -1 && e12[De].splice(n, 1);
}
function Fe(e12) {
  let t = e12[k];
  return se(t) ? t[k] : t;
}
function Oi(e12) {
  return e12[Nt] ??= [];
}
function ki(e12) {
  return e12.cleanup ??= [];
}
function xc(e12, t, n, r) {
  let o = Oi(t);
  o.push(n), e12.firstCreatePass && ki(e12).push(r, o.length - 1);
}
var I = { lFrame: Gc(null), bindingsEnabled: true, skipHydrationRootTNode: null };
var ri = false;
function Rc() {
  return I.lFrame.elementDepthCount;
}
function Ac() {
  I.lFrame.elementDepthCount++;
}
function Oc() {
  I.lFrame.elementDepthCount--;
}
function kc() {
  return I.skipHydrationRootTNode !== null;
}
function Pc(e12) {
  return I.skipHydrationRootTNode === e12;
}
function Lc() {
  I.skipHydrationRootTNode = null;
}
function T() {
  return I.lFrame.lView;
}
function Q() {
  return I.lFrame.tView;
}
function Me(e12) {
  return I.lFrame.contextLView = e12, e12[N];
}
function _e(e12) {
  return I.lFrame.contextLView = null, e12;
}
function ae() {
  let e12 = Pi();
  for (; e12 !== null && e12.type === 64; )
    e12 = e12.parent;
  return e12;
}
function Pi() {
  return I.lFrame.currentTNode;
}
function Fc() {
  let e12 = I.lFrame, t = e12.currentTNode;
  return e12.isParent ? t : t.parent;
}
function kt(e12, t) {
  let n = I.lFrame;
  n.currentTNode = e12, n.isParent = t;
}
function Li() {
  return I.lFrame.isParent;
}
function jc() {
  I.lFrame.isParent = false;
}
function Fi() {
  return ri;
}
function Kt(e12) {
  let t = ri;
  return ri = e12, t;
}
function Hc(e12) {
  return I.lFrame.bindingIndex = e12;
}
function sn() {
  return I.lFrame.bindingIndex++;
}
function Vc(e12) {
  let t = I.lFrame, n = t.bindingIndex;
  return t.bindingIndex = t.bindingIndex + e12, n;
}
function Bc() {
  return I.lFrame.inI18n;
}
function $c(e12, t) {
  let n = I.lFrame;
  n.bindingIndex = n.bindingRootIndex = e12, gr(t);
}
function Uc() {
  return I.lFrame.currentDirectiveIndex;
}
function gr(e12) {
  I.lFrame.currentDirectiveIndex = e12;
}
function zc(e12) {
  let t = I.lFrame.currentDirectiveIndex;
  return t === -1 ? null : e12[t];
}
function ji() {
  return I.lFrame.currentQueryIndex;
}
function mr(e12) {
  I.lFrame.currentQueryIndex = e12;
}
function nf(e12) {
  let t = e12[m];
  return t.type === 2 ? t.declTNode : t.type === 1 ? e12[te] : null;
}
function Hi(e12, t, n) {
  if (n & 4) {
    let o = t, i = e12;
    for (; o = o.parent, o === null && !(n & 1); )
      if (o = nf(i), o === null || (i = i[ot], o.type & 10))
        break;
    if (o === null)
      return false;
    t = o, e12 = i;
  }
  let r = I.lFrame = Wc();
  return r.currentTNode = t, r.lView = e12, true;
}
function yr(e12) {
  let t = Wc(), n = e12[m];
  I.lFrame = t, t.currentTNode = n.firstChild, t.lView = e12, t.tView = n, t.contextLView = e12, t.bindingIndex = n.bindingStartIndex, t.inI18n = false;
}
function Wc() {
  let e12 = I.lFrame, t = e12 === null ? null : e12.child;
  return t === null ? Gc(e12) : t;
}
function Gc(e12) {
  let t = { currentTNode: null, isParent: true, lView: null, tView: null, selectedIndex: -1, contextLView: null, elementDepthCount: 0, currentNamespace: null, currentDirectiveIndex: -1, bindingRootIndex: -1, bindingIndex: -1, currentQueryIndex: 0, parent: e12, child: null, inI18n: false };
  return e12 !== null && (e12.child = t), t;
}
function qc() {
  let e12 = I.lFrame;
  return I.lFrame = e12.parent, e12.currentTNode = null, e12.lView = null, e12;
}
var Vi = qc;
function vr() {
  let e12 = qc();
  e12.isParent = true, e12.tView = null, e12.selectedIndex = -1, e12.contextLView = null, e12.elementDepthCount = 0, e12.currentDirectiveIndex = -1, e12.currentNamespace = null, e12.bindingRootIndex = -1, e12.bindingIndex = -1, e12.currentQueryIndex = 0;
}
function Zc(e12) {
  return (I.lFrame.contextLView = Sc(e12, I.lFrame.contextLView))[N];
}
function Ue() {
  return I.lFrame.selectedIndex;
}
function ze(e12) {
  I.lFrame.selectedIndex = e12;
}
function Qc() {
  let e12 = I.lFrame;
  return fr(e12.tView, e12.selectedIndex);
}
function Yc() {
  return I.lFrame.currentNamespace;
}
var Kc = true;
function Er() {
  return Kc;
}
function Ir(e12) {
  Kc = e12;
}
function oi(e12, t = null, n = null, r) {
  let o = Jc(e12, t, n, r);
  return o.resolveInjectorInitializers(), o;
}
function Jc(e12, t = null, n = null, r, o = /* @__PURE__ */ new Set()) {
  let i = [n || Pe, vc(e12)], s;
  return new Je(i, t || nn(), s || null, o);
}
var fe = class e2 {
  static THROW_IF_NOT_FOUND = Qe;
  static NULL = new Yt();
  static create(t, n) {
    if (Array.isArray(t))
      return oi({ name: "" }, n, t, "");
    {
      let r = t.name ?? "";
      return oi({ name: r }, t.parent, t.providers, r);
    }
  }
  static \u0275prov = _({ token: e2, providedIn: "any", factory: () => b(Ei) });
  static __NG_ELEMENT_ID__ = -1;
};
var W = new D("");
var Pt = /* @__PURE__ */ (() => {
  class e12 {
    static __NG_ELEMENT_ID__ = rf;
    static __NG_ENV_ID__ = (n) => n;
  }
  return e12;
})();
var Kn = class extends Pt {
  _lView;
  constructor(t) {
    super(), this._lView = t;
  }
  get destroyed() {
    return ct(this._lView);
  }
  onDestroy(t) {
    let n = this._lView;
    return Ai(n, t), () => Nc(n, t);
  }
};
function rf() {
  return new Kn(T());
}
var Xc = false;
var el = new D("");
var Lt = (() => {
  class e12 {
    taskId = 0;
    pendingTasks = /* @__PURE__ */ new Set();
    destroyed = false;
    pendingTask = new Zt(false);
    debugTaskTracker = E(el, { optional: true });
    get hasPendingTasks() {
      return this.destroyed ? false : this.pendingTask.value;
    }
    get hasPendingTasksObservable() {
      return this.destroyed ? new bt((n) => {
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
var ii = class extends Ee {
  __isAsync;
  destroyRef = void 0;
  pendingTasks = void 0;
  constructor(t = false) {
    super(), this.__isAsync = t, bc() && (this.destroyRef = E(Pt, { optional: true }) ?? void 0, this.pendingTasks = E(Lt, { optional: true }) ?? void 0);
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
    return t instanceof U && t.add(a), a;
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
var Ie = ii;
function Jn(...e12) {
}
function Bi(e12) {
  let t, n;
  function r() {
    e12 = Jn;
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
function tl(e12) {
  return queueMicrotask(() => e12()), () => {
    e12 = Jn;
  };
}
var $i = "isAngularZone";
var Jt = $i + "_ID";
var of = 0;
var X = class e3 {
  hasPendingMacrotasks = false;
  hasPendingMicrotasks = false;
  isStable = true;
  onUnstable = new Ie(false);
  onMicrotaskEmpty = new Ie(false);
  onStable = new Ie(false);
  onError = new Ie(false);
  constructor(t) {
    let { enableLongStackTrace: n = false, shouldCoalesceEventChangeDetection: r = false, shouldCoalesceRunChangeDetection: o = false, scheduleInRootZone: i = Xc } = t;
    if (typeof Zone > "u")
      throw new v(908, false);
    Zone.assertZonePatched();
    let s = this;
    s._nesting = 0, s._outer = s._inner = Zone.current, Zone.TaskTrackingZoneSpec && (s._inner = s._inner.fork(new Zone.TaskTrackingZoneSpec())), n && Zone.longStackTraceZoneSpec && (s._inner = s._inner.fork(Zone.longStackTraceZoneSpec)), s.shouldCoalesceEventChangeDetection = !o && r, s.shouldCoalesceRunChangeDetection = o, s.callbackScheduled = false, s.scheduleInRootZone = i, cf(s);
  }
  static isInAngularZone() {
    return typeof Zone < "u" && Zone.current.get($i) === true;
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
    let i = this._inner, s = i.scheduleEventTask("NgZoneEvent: " + o, t, sf, Jn, Jn);
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
var sf = {};
function Ui(e12) {
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
function af(e12) {
  if (e12.isCheckStableRunning || e12.callbackScheduled)
    return;
  e12.callbackScheduled = true;
  function t() {
    Bi(() => {
      e12.callbackScheduled = false, si(e12), e12.isCheckStableRunning = true, Ui(e12), e12.isCheckStableRunning = false;
    });
  }
  e12.scheduleInRootZone ? Zone.root.run(() => {
    t();
  }) : e12._outer.run(() => {
    t();
  }), si(e12);
}
function cf(e12) {
  let t = () => {
    af(e12);
  }, n = of++;
  e12._inner = e12._inner.fork({ name: "angular", properties: { [$i]: true, [Jt]: n, [Jt + n]: true }, onInvokeTask: (r, o, i, s, a, c) => {
    if (lf(c))
      return r.invokeTask(i, s, a, c);
    try {
      return sc(e12), r.invokeTask(i, s, a, c);
    } finally {
      (e12.shouldCoalesceEventChangeDetection && s.type === "eventTask" || e12.shouldCoalesceRunChangeDetection) && t(), ac(e12);
    }
  }, onInvoke: (r, o, i, s, a, c, l) => {
    try {
      return sc(e12), r.invoke(i, s, a, c, l);
    } finally {
      e12.shouldCoalesceRunChangeDetection && !e12.callbackScheduled && !uf(c) && t(), ac(e12);
    }
  }, onHasTask: (r, o, i, s) => {
    r.hasTask(i, s), o === i && (s.change == "microTask" ? (e12._hasPendingMicrotasks = s.microTask, si(e12), Ui(e12)) : s.change == "macroTask" && (e12.hasPendingMacrotasks = s.macroTask));
  }, onHandleError: (r, o, i, s) => (r.handleError(i, s), e12.runOutsideAngular(() => e12.onError.emit(s)), false) });
}
function si(e12) {
  e12._hasPendingMicrotasks || (e12.shouldCoalesceEventChangeDetection || e12.shouldCoalesceRunChangeDetection) && e12.callbackScheduled === true ? e12.hasPendingMicrotasks = true : e12.hasPendingMicrotasks = false;
}
function sc(e12) {
  e12._nesting++, e12.isStable && (e12.isStable = false, e12.onUnstable.emit(null));
}
function ac(e12) {
  e12._nesting--, Ui(e12);
}
var Xt = class {
  hasPendingMicrotasks = false;
  hasPendingMacrotasks = false;
  isStable = true;
  onUnstable = new Ie();
  onMicrotaskEmpty = new Ie();
  onStable = new Ie();
  onError = new Ie();
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
function lf(e12) {
  return nl(e12, "__ignore_ng_zone__");
}
function uf(e12) {
  return nl(e12, "__scheduler_tick__");
}
function nl(e12, t) {
  return !Array.isArray(e12) || e12.length !== 1 ? false : e12[0]?.data?.[t] === true;
}
var be = class {
  _console = console;
  handleError(t) {
    this._console.error("ERROR", t);
  }
};
var lt = new D("", { factory: () => {
  let e12 = E(X), t = E(J), n;
  return (r) => {
    e12.runOutsideAngular(() => {
      t.destroyed && !n ? setTimeout(() => {
        throw r;
      }) : (n ??= t.get(be), n.handleError(r));
    });
  };
} });
var rl = { provide: rt, useValue: () => {
  let e12 = E(be, { optional: true });
}, multi: true };
var df = new D("", { factory: () => {
  let e12 = E(W).defaultView;
  if (!e12)
    return;
  let t = E(lt), n = (i) => {
    t(i.reason), i.preventDefault();
  }, r = (i) => {
    i.error ? t(i.error) : t(new Error(i.message, { cause: i })), i.preventDefault();
  }, o = () => {
    e12.addEventListener("unhandledrejection", n), e12.addEventListener("error", r);
  };
  typeof Zone < "u" ? Zone.root.run(o) : o(), E(Pt).onDestroy(() => {
    e12.removeEventListener("error", r), e12.removeEventListener("unhandledrejection", n);
  });
} });
function zi() {
  return _t([yc(() => {
    E(df);
  })]);
}
function H(e12, t) {
  let [n, r, o] = Lo(e12, t?.equal), i = n, s = i[K];
  return i.set = r, i.update = o, i.asReadonly = ol.bind(i), i;
}
function ol() {
  let e12 = this[K];
  if (e12.readonlyFn === void 0) {
    let t = () => this();
    t[K] = e12, e12.readonlyFn = t;
  }
  return e12.readonlyFn;
}
var Dr = /* @__PURE__ */ (() => {
  class e12 {
    view;
    node;
    constructor(n, r) {
      this.view = n, this.node = r;
    }
    static __NG_ELEMENT_ID__ = ff;
  }
  return e12;
})();
function ff() {
  return new Dr(T(), ae());
}
var Xe = class {
};
var an = new D("", { factory: () => true });
var Wi = new D("");
var br = (() => {
  class e12 {
    static \u0275prov = _({ token: e12, providedIn: "root", factory: () => new ai() });
  }
  return e12;
})();
var ai = class {
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
var Xn = class {
  [K];
  constructor(t) {
    this[K] = t;
  }
  destroy() {
    this[K].destroy();
  }
};
function Cr(e12, t) {
  let n = t?.injector ?? E(fe), r = t?.manualCleanup !== true ? n.get(Pt) : null, o, i = n.get(Dr, null, { optional: true }), s = n.get(Xe);
  return i !== null ? (o = gf(i.view, s, e12), r instanceof Kn && r._lView === i.view && (r = null)) : o = mf(e12, n.get(br), s), o.injector = n, r !== null && (o.onDestroyFns = [r.onDestroy(() => o.destroy())]), new Xn(o);
}
var il = O(A({}, jo), { cleanupFns: void 0, zone: null, onDestroyFns: null, run() {
  let e12 = Kt(false);
  try {
    Ho(this);
  } finally {
    Kt(e12);
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
var pf = O(A({}, il), { consumerMarkedDirty() {
  this.scheduler.schedule(this), this.notifier.notify(12);
}, destroy() {
  if (yt(this), this.onDestroyFns !== null)
    for (let e12 of this.onDestroyFns)
      e12();
  this.cleanup(), this.scheduler.remove(this);
} });
var hf = O(A({}, il), { consumerMarkedDirty() {
  this.view[y] |= 8192, Ot(this.view), this.notifier.notify(13);
}, destroy() {
  if (yt(this), this.onDestroyFns !== null)
    for (let e12 of this.onDestroyFns)
      e12();
  this.cleanup(), this.view[Le]?.delete(this);
} });
function gf(e12, t, n) {
  let r = Object.create(hf);
  return r.view = e12, r.zone = typeof Zone < "u" ? Zone.current : null, r.notifier = t, r.fn = sl(r, n), e12[Le] ??= /* @__PURE__ */ new Set(), e12[Le].add(r), r.consumerMarkedDirty(r), r;
}
function mf(e12, t, n) {
  let r = Object.create(pf);
  return r.fn = sl(r, e12), r.scheduler = t, r.notifier = n, r.zone = typeof Zone < "u" ? Zone.current : null, r.scheduler.add(r), r.notifier.notify(12), r;
}
function sl(e12, t) {
  return () => {
    t((n) => (e12.cleanupFns ??= []).push(n));
  };
}
function jl(e12) {
  return { toString: e12 }.toString();
}
function Nf(e12) {
  return typeof e12 == "function";
}
function Hl(e12, t, n, r) {
  t !== null ? t.applyValueToInputSignal(t, r) : e12[n] = r;
}
var Ar = class {
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
function xf(e12) {
  return e12.type.prototype.ngOnChanges && (e12.setInput = Af), Rf;
}
function Rf() {
  let e12 = Bl(this), t = e12?.current;
  if (t) {
    let n = e12.previous;
    if (n === nt)
      e12.previous = t;
    else
      for (let r in t)
        n[r] = t[r];
    e12.current = null, this.ngOnChanges(t);
  }
}
function Af(e12, t, n, r, o) {
  let i = this.declaredInputs[r], s = Bl(e12) || Of(e12, { previous: nt, current: null }), a = s.current || (s.current = {}), c = s.previous, l = c[i];
  a[i] = new Ar(l && l.currentValue, n, c === nt), Hl(e12, t, o, n);
}
var Vl = "__ngSimpleChanges__";
function Bl(e12) {
  return e12[Vl] || null;
}
function Of(e12, t) {
  return e12[Vl] = t;
}
var al = [];
var M = function(e12, t = null, n) {
  for (let r = 0; r < al.length; r++) {
    let o = al[r];
    o(e12, t, n);
  }
};
var C = function(e12) {
  return e12[e12.TemplateCreateStart = 0] = "TemplateCreateStart", e12[e12.TemplateCreateEnd = 1] = "TemplateCreateEnd", e12[e12.TemplateUpdateStart = 2] = "TemplateUpdateStart", e12[e12.TemplateUpdateEnd = 3] = "TemplateUpdateEnd", e12[e12.LifecycleHookStart = 4] = "LifecycleHookStart", e12[e12.LifecycleHookEnd = 5] = "LifecycleHookEnd", e12[e12.OutputStart = 6] = "OutputStart", e12[e12.OutputEnd = 7] = "OutputEnd", e12[e12.BootstrapApplicationStart = 8] = "BootstrapApplicationStart", e12[e12.BootstrapApplicationEnd = 9] = "BootstrapApplicationEnd", e12[e12.BootstrapComponentStart = 10] = "BootstrapComponentStart", e12[e12.BootstrapComponentEnd = 11] = "BootstrapComponentEnd", e12[e12.ChangeDetectionStart = 12] = "ChangeDetectionStart", e12[e12.ChangeDetectionEnd = 13] = "ChangeDetectionEnd", e12[e12.ChangeDetectionSyncStart = 14] = "ChangeDetectionSyncStart", e12[e12.ChangeDetectionSyncEnd = 15] = "ChangeDetectionSyncEnd", e12[e12.AfterRenderHooksStart = 16] = "AfterRenderHooksStart", e12[e12.AfterRenderHooksEnd = 17] = "AfterRenderHooksEnd", e12[e12.ComponentStart = 18] = "ComponentStart", e12[e12.ComponentEnd = 19] = "ComponentEnd", e12[e12.DeferBlockStateStart = 20] = "DeferBlockStateStart", e12[e12.DeferBlockStateEnd = 21] = "DeferBlockStateEnd", e12[e12.DynamicComponentStart = 22] = "DynamicComponentStart", e12[e12.DynamicComponentEnd = 23] = "DynamicComponentEnd", e12[e12.HostBindingsUpdateStart = 24] = "HostBindingsUpdateStart", e12[e12.HostBindingsUpdateEnd = 25] = "HostBindingsUpdateEnd", e12;
}(C || {});
function kf(e12, t, n) {
  let { ngOnChanges: r, ngOnInit: o, ngDoCheck: i } = t.type.prototype;
  if (r) {
    let s = xf(t);
    (n.preOrderHooks ??= []).push(e12, s), (n.preOrderCheckHooks ??= []).push(e12, s);
  }
  o && (n.preOrderHooks ??= []).push(0 - e12, o), i && ((n.preOrderHooks ??= []).push(e12, i), (n.preOrderCheckHooks ??= []).push(e12, i));
}
function Pf(e12, t) {
  for (let n = t.directiveStart, r = t.directiveEnd; n < r; n++) {
    let i = e12.data[n].type.prototype, { ngAfterContentInit: s, ngAfterContentChecked: a, ngAfterViewInit: c, ngAfterViewChecked: l, ngOnDestroy: u } = i;
    s && (e12.contentHooks ??= []).push(-n, s), a && ((e12.contentHooks ??= []).push(n, a), (e12.contentCheckHooks ??= []).push(n, a)), c && (e12.viewHooks ??= []).push(-n, c), l && ((e12.viewHooks ??= []).push(n, l), (e12.viewCheckHooks ??= []).push(n, l)), u != null && (e12.destroyHooks ??= []).push(n, u);
  }
}
function Sr(e12, t, n) {
  $l(e12, t, 3, n);
}
function Nr(e12, t, n, r) {
  (e12[y] & 3) === n && $l(e12, t, n, r);
}
function Gi(e12, t) {
  let n = e12[y];
  (n & 3) === t && (n &= 16383, n += 1, e12[y] = n);
}
function $l(e12, t, n, r) {
  let o = r !== void 0 ? e12[it] & 65535 : 0, i = r ?? -1, s = t.length - 1, a = 0;
  for (let c = o; c < s; c++)
    if (typeof t[c + 1] == "number") {
      if (a = t[c], r != null && a >= r)
        break;
    } else
      t[c] < 0 && (e12[it] += 65536), (a < i || i == -1) && (Lf(e12, n, t, c), e12[it] = (e12[it] & 4294901760) + c + 2), c++;
}
function cl(e12, t) {
  M(C.LifecycleHookStart, e12, t);
  let n = g(null);
  try {
    t.call(e12);
  } finally {
    g(n), M(C.LifecycleHookEnd, e12, t);
  }
}
function Lf(e12, t, n, r) {
  let o = n[r] < 0, i = n[r + 1], s = o ? -n[r] : n[r], a = e12[s];
  o ? e12[y] >> 14 < e12[it] >> 16 && (e12[y] & 3) === t && (e12[y] += 16384, cl(a, i)) : cl(a, i);
}
var jt = -1;
var dt = class {
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
function Ff(e12, t, n) {
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
      jf(i) ? e12.setProperty(t, i, s) : e12.setAttribute(t, i, s), r++;
    }
  }
  return r;
}
function jf(e12) {
  return e12.charCodeAt(0) === 64;
}
function Wr(e12, t) {
  if (!(t === null || t.length === 0))
    if (e12 === null || e12.length === 0)
      e12 = t.slice();
    else {
      let n = -1;
      for (let r = 0; r < t.length; r++) {
        let o = t[r];
        typeof o == "number" ? n = o : n === 0 || (n === -1 || n === 2 ? ll(e12, n, o, null, t[++r]) : ll(e12, n, o, null, null));
      }
    }
  return e12;
}
function ll(e12, t, n, r, o) {
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
function Ul(e12) {
  return e12 !== jt;
}
function Or(e12) {
  return e12 & 32767;
}
function Hf(e12) {
  return e12 >> 16;
}
function kr(e12, t) {
  let n = Hf(e12), r = t;
  for (; n > 0; )
    r = r[ot], n--;
  return r;
}
var ts = true;
function ul(e12) {
  let t = ts;
  return ts = e12, t;
}
var Vf = 256;
var zl = Vf - 1;
var Wl = 5;
var Bf = 0;
var ye = {};
function $f(e12, t, n) {
  let r;
  typeof n == "string" ? r = n.charCodeAt(0) || 0 : n.hasOwnProperty(et) && (r = n[et]), r == null && (r = n[et] = Bf++);
  let o = r & zl, i = 1 << o;
  t.data[e12 + (o >> Wl)] |= i;
}
function Pr(e12, t) {
  let n = Gl(e12, t);
  if (n !== -1)
    return n;
  let r = t[m];
  r.firstCreatePass && (e12.injectorIndex = t.length, qi(r.data, e12), qi(t, null), qi(r.blueprint, null));
  let o = Bs(e12, t), i = e12.injectorIndex;
  if (Ul(o)) {
    let s = Or(o), a = kr(o, t), c = a[m].data;
    for (let l = 0; l < 8; l++)
      t[i + l] = a[s + l] | c[s + l];
  }
  return t[i + 8] = o, i;
}
function qi(e12, t) {
  e12.push(0, 0, 0, 0, 0, 0, 0, 0, t);
}
function Gl(e12, t) {
  return e12.injectorIndex === -1 || e12.parent && e12.parent.injectorIndex === e12.injectorIndex || t[e12.injectorIndex + 8] === null ? -1 : e12.injectorIndex;
}
function Bs(e12, t) {
  if (e12.parent && e12.parent.injectorIndex !== -1)
    return e12.parent.injectorIndex;
  let n = 0, r = null, o = t;
  for (; o !== null; ) {
    if (r = Kl(o), r === null)
      return jt;
    if (n++, o = o[ot], r.injectorIndex !== -1)
      return r.injectorIndex | n << 16;
  }
  return jt;
}
function ns(e12, t, n) {
  $f(e12, t, n);
}
function ql(e12, t, n) {
  if (n & 8 || e12 !== void 0)
    return e12;
  sr(t, "NodeInjector");
}
function Zl(e12, t, n, r) {
  if (n & 8 && r === void 0 && (r = null), (n & 3) === 0) {
    let o = e12[Ce], i = q(void 0);
    try {
      return o ? o.get(t, r, n & 8) : yi(t, r, n & 8);
    } finally {
      q(i);
    }
  }
  return ql(r, t, n);
}
function Ql(e12, t, n, r = 0, o) {
  if (e12 !== null) {
    if (t[y] & 2048 && !(r & 2)) {
      let s = Gf(e12, t, n, r, ye);
      if (s !== ye)
        return s;
    }
    let i = Yl(e12, t, n, r, ye);
    if (i !== ye)
      return i;
  }
  return Zl(t, n, r, o);
}
function Yl(e12, t, n, r, o) {
  let i = zf(n);
  if (typeof i == "function") {
    if (!Hi(t, e12, r))
      return r & 1 ? ql(o, n, r) : Zl(t, n, r, o);
    try {
      let s;
      if (s = i(r), s == null && !(r & 8))
        sr(n);
      else
        return s;
    } finally {
      Vi();
    }
  } else if (typeof i == "number") {
    let s = null, a = Gl(e12, t), c = jt, l = r & 1 ? t[ne][te] : null;
    for ((a === -1 || r & 4) && (c = a === -1 ? Bs(e12, t) : t[a + 8], c === jt || !fl(r, false) ? a = -1 : (s = t[m], a = Or(c), t = kr(c, t))); a !== -1; ) {
      let u = t[m];
      if (dl(i, a, u.data)) {
        let d = Uf(a, t, n, s, r, l);
        if (d !== ye)
          return d;
      }
      c = t[a + 8], c !== jt && fl(r, t[m].data[a + 8] === l) && dl(i, a, t) ? (s = u, a = Or(c), t = kr(c, t)) : a = -1;
    }
  }
  return o;
}
function Uf(e12, t, n, r, o, i) {
  let s = t[m], a = s.data[e12 + 8], c = r == null ? Rt(a) && ts : r != s && (a.type & 3) !== 0, l = o & 1 && i === a, u = xr(a, s, n, c, l);
  return u !== null ? dn(t, s, u, a, o) : ye;
}
function xr(e12, t, n, r, o) {
  let i = e12.providerIndexes, s = t.data, a = i & 1048575, c = e12.directiveStart, l = e12.directiveEnd, u = i >> 20, d = r ? a : a + u, p = o ? a + u : l;
  for (let f = d; f < p; f++) {
    let h = s[f];
    if (f < c && n === h || f >= c && h.type === n)
      return f;
  }
  if (o) {
    let f = s[c];
    if (f && at(f) && f.type === n)
      return c;
  }
  return null;
}
function dn(e12, t, n, r, o) {
  let i = e12[n], s = t.data;
  if (i instanceof dt) {
    let a = i;
    if (a.resolving)
      throw mi("");
    let c = ul(a.canSeeViewProviders);
    a.resolving = true;
    let l = s[n].type || s[n], u, d = a.injectImpl ? q(a.injectImpl) : null, p = Hi(e12, r, 0);
    try {
      i = e12[n] = a.factory(void 0, o, s, e12, r), t.firstCreatePass && n >= r.directiveStart && kf(n, s[n], t);
    } finally {
      d !== null && q(d), ul(c), a.resolving = false, Vi();
    }
  }
  return i;
}
function zf(e12) {
  if (typeof e12 == "string")
    return e12.charCodeAt(0) || 0;
  let t = e12.hasOwnProperty(et) ? e12[et] : void 0;
  return typeof t == "number" ? t >= 0 ? t & zl : Wf : t;
}
function dl(e12, t, n) {
  let r = 1 << e12;
  return !!(n[t + (e12 >> Wl)] & r);
}
function fl(e12, t) {
  return !(e12 & 2) && !(e12 & 1 && t);
}
var ut = class {
  _tNode;
  _lView;
  constructor(t, n) {
    this._tNode = t, this._lView = n;
  }
  get(t, n, r) {
    return Ql(this._tNode, this._lView, t, Ye(r), n);
  }
};
function Wf() {
  return new ut(ae(), T());
}
function Gf(e12, t, n, r, o) {
  let i = e12, s = t;
  for (; i !== null && s !== null && s[y] & 2048 && !At(s); ) {
    let a = Yl(i, s, n, r | 2, ye);
    if (a !== ye)
      return a;
    let c = i.parent;
    if (!c) {
      let l = s[Ti];
      if (l) {
        let u = l.get(n, ye, r & -5);
        if (u !== ye)
          return u;
      }
      c = Kl(s), s = s[ot];
    }
    i = c;
  }
  return o;
}
function Kl(e12) {
  let t = e12[m], n = t.type;
  return n === 2 ? t.declTNode : n === 1 ? e12[te] : null;
}
function qf() {
  return $t(ae(), T());
}
function $t(e12, t) {
  return new En(ge(e12, t));
}
var En = /* @__PURE__ */ (() => {
  class e12 {
    nativeElement;
    constructor(n) {
      this.nativeElement = n;
    }
    static __NG_ELEMENT_ID__ = qf;
  }
  return e12;
})();
function Zf(e12) {
  return e12 instanceof En ? e12.nativeElement : e12;
}
function Qf() {
  return this._results[Symbol.iterator]();
}
var Lr = class {
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
    return this._changes ??= new Ee();
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
    let r = hc(t);
    (this._changesDetected = !pc(this._results, r, n)) && (this._results = r, this.length = r.length, this.last = r[this.length - 1], this.first = r[0]);
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
  [Symbol.iterator] = Qf;
};
function Jl(e12) {
  return (e12.flags & 128) === 128;
}
var $s = function(e12) {
  return e12[e12.OnPush = 0] = "OnPush", e12[e12.Eager = 1] = "Eager", e12[e12.Default = 1] = "Default", e12;
}($s || {});
var Xl = /* @__PURE__ */ new Map();
var Yf = 0;
function Kf() {
  return Yf++;
}
function Jf(e12) {
  Xl.set(e12[we], e12);
}
function rs(e12) {
  Xl.delete(e12[we]);
}
var pl = "__ngContext__";
function Ht(e12, t) {
  $e(t) ? (e12[pl] = t[we], Jf(t)) : e12[pl] = t;
}
function eu(e12) {
  return nu(e12[xt]);
}
function tu(e12) {
  return nu(e12[ee]);
}
function nu(e12) {
  for (; e12 !== null && !se(e12); )
    e12 = e12[ee];
  return e12;
}
var os;
function Us(e12) {
  os = e12;
}
function ru() {
  if (os !== void 0)
    return os;
  if (typeof document < "u")
    return document;
  throw new v(210, false);
}
var Gr = new D("", { factory: () => Xf });
var Xf = "ng";
var qr = new D("");
var In = new D("", { providedIn: "platform", factory: () => "unknown" });
var Zr = new D("", { factory: () => E(W).body?.querySelector("[ngCspNonce]")?.getAttribute("ngCspNonce") || null });
var ou = "r";
var iu = "di";
var su = false;
var au = new D("", { factory: () => su });
var hl = /* @__PURE__ */ new WeakMap();
function ep(e12, t) {
  if (e12 == null || typeof e12 != "object")
    return;
  let n = hl.get(e12);
  n || (n = /* @__PURE__ */ new WeakSet(), hl.set(e12, n)), n.add(t);
}
var tp = (e12, t, n, r) => {
};
function np(e12, t, n, r) {
  tp(e12, t, n, r);
}
function zs(e12) {
  return (e12.flags & 32) === 32;
}
var rp = () => null;
function cu(e12, t, n = false) {
  return rp(e12, t, n);
}
function lu(e12, t) {
  let n = e12.contentQueries;
  if (n !== null) {
    let r = g(null);
    try {
      for (let o = 0; o < n.length; o += 2) {
        let i = n[o], s = n[o + 1];
        if (s !== -1) {
          let a = e12.data[s];
          mr(i), a.contentQueries(2, t[s], s);
        }
      }
    } finally {
      g(r);
    }
  }
}
function is(e12, t, n) {
  mr(0);
  let r = g(null);
  try {
    t(e12, n);
  } finally {
    g(r);
  }
}
function op(e12, t, n) {
  if (_i(t)) {
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
var ce = function(e12) {
  return e12[e12.Emulated = 0] = "Emulated", e12[e12.None = 2] = "None", e12[e12.ShadowDom = 3] = "ShadowDom", e12[e12.ExperimentalIsolatedShadowDom = 4] = "ExperimentalIsolatedShadowDom", e12;
}(ce || {});
var wr;
function ip() {
  if (wr === void 0 && (wr = null, je.trustedTypes))
    try {
      wr = je.trustedTypes.createPolicy("angular", { createHTML: (e12) => e12, createScript: (e12) => e12, createScriptURL: (e12) => e12 });
    } catch {
    }
  return wr;
}
function Qr(e12) {
  return ip()?.createHTML(e12) || e12;
}
var Tr;
function sp() {
  if (Tr === void 0 && (Tr = null, je.trustedTypes))
    try {
      Tr = je.trustedTypes.createPolicy("angular#unsafe-bypass", { createHTML: (e12) => e12, createScript: (e12) => e12, createScriptURL: (e12) => e12 });
    } catch {
    }
  return Tr;
}
function gl(e12) {
  return sp()?.createHTML(e12) || e12;
}
var Se = class {
  changingThisBreaksApplicationSecurity;
  constructor(t) {
    this.changingThisBreaksApplicationSecurity = t;
  }
  toString() {
    return `SafeValue must use [property]=binding: ${this.changingThisBreaksApplicationSecurity} (see ${er})`;
  }
};
var ss = class extends Se {
  getTypeName() {
    return "HTML";
  }
};
var as = class extends Se {
  getTypeName() {
    return "Style";
  }
};
var cs = class extends Se {
  getTypeName() {
    return "Script";
  }
};
var ls = class extends Se {
  getTypeName() {
    return "URL";
  }
};
var us = class extends Se {
  getTypeName() {
    return "ResourceURL";
  }
};
function xe(e12) {
  return e12 instanceof Se ? e12.changingThisBreaksApplicationSecurity : e12;
}
function We(e12, t) {
  let n = uu(e12);
  if (n != null && n !== t) {
    if (n === "ResourceURL" && t === "URL")
      return true;
    throw new Error(`Required a safe ${t}, got a ${n} (see ${er})`);
  }
  return n === t;
}
function uu(e12) {
  return e12 instanceof Se && e12.getTypeName() || null;
}
function Ws(e12) {
  return new ss(e12);
}
function Gs(e12) {
  return new as(e12);
}
function qs(e12) {
  return new cs(e12);
}
function Zs(e12) {
  return new ls(e12);
}
function Qs(e12) {
  return new us(e12);
}
function ap(e12) {
  let t = new fs(e12);
  return cp() ? new ds(t) : t;
}
var ds = class {
  inertDocumentHelper;
  constructor(t) {
    this.inertDocumentHelper = t;
  }
  getInertBodyElement(t) {
    t = "<body><remove></remove>" + t;
    try {
      let n = new window.DOMParser().parseFromString(Qr(t), "text/html").body;
      return n === null ? this.inertDocumentHelper.getInertBodyElement(t) : (n.firstChild?.remove(), n);
    } catch {
      return null;
    }
  }
};
var fs = class {
  defaultDoc;
  inertDocument;
  constructor(t) {
    this.defaultDoc = t, this.inertDocument = this.defaultDoc.implementation.createHTMLDocument("sanitization-inert");
  }
  getInertBodyElement(t) {
    let n = this.inertDocument.createElement("template");
    return n.innerHTML = Qr(t), n;
  }
};
function cp() {
  try {
    return !!new window.DOMParser().parseFromString(Qr(""), "text/html");
  } catch {
    return false;
  }
}
var lp = /^(?!javascript:)(?:[a-z0-9+.-]+:|[^&:\/?#]*(?:[\/?#]|$))/i;
function Yr(e12) {
  return e12 = String(e12), e12.match(lp) ? e12 : "unsafe:" + e12;
}
function Re(e12) {
  let t = {};
  for (let n of e12.split(","))
    t[n] = true;
  return t;
}
function Dn(...e12) {
  let t = {};
  for (let n of e12)
    for (let r in n)
      n.hasOwnProperty(r) && (t[r] = true);
  return t;
}
var du = Re("area,br,col,hr,img,wbr");
var fu = Re("colgroup,dd,dt,li,p,tbody,td,tfoot,th,thead,tr");
var pu = Re("rp,rt");
var up = Dn(pu, fu);
var dp = Dn(fu, Re("address,article,aside,blockquote,caption,center,del,details,dialog,dir,div,dl,figure,figcaption,footer,h1,h2,h3,h4,h5,h6,header,hgroup,hr,ins,main,map,menu,nav,ol,pre,section,summary,table,ul"));
var fp = Dn(pu, Re("a,abbr,acronym,audio,b,bdi,bdo,big,br,cite,code,del,dfn,em,font,i,img,ins,kbd,label,map,mark,picture,q,ruby,rp,rt,s,samp,small,source,span,strike,strong,sub,sup,time,track,tt,u,var,video"));
var ml = Dn(du, dp, fp, up);
var hu = Re("background,cite,href,itemtype,longdesc,poster,src,xlink:href");
var pp = Re("abbr,accesskey,align,alt,autoplay,axis,bgcolor,border,cellpadding,cellspacing,class,clear,color,cols,colspan,compact,controls,coords,datetime,default,dir,download,face,headers,height,hidden,hreflang,hspace,ismap,itemscope,itemprop,kind,label,lang,language,loop,media,muted,nohref,nowrap,open,preload,rel,rev,role,rows,rowspan,rules,scope,scrolling,shape,size,sizes,span,srclang,srcset,start,summary,tabindex,target,title,translate,type,usemap,valign,value,vspace,width");
var hp = Re("aria-activedescendant,aria-atomic,aria-autocomplete,aria-busy,aria-checked,aria-colcount,aria-colindex,aria-colspan,aria-controls,aria-current,aria-describedby,aria-details,aria-disabled,aria-dropeffect,aria-errormessage,aria-expanded,aria-flowto,aria-grabbed,aria-haspopup,aria-hidden,aria-invalid,aria-keyshortcuts,aria-label,aria-labelledby,aria-level,aria-live,aria-modal,aria-multiline,aria-multiselectable,aria-orientation,aria-owns,aria-placeholder,aria-posinset,aria-pressed,aria-readonly,aria-relevant,aria-required,aria-roledescription,aria-rowcount,aria-rowindex,aria-rowspan,aria-selected,aria-setsize,aria-sort,aria-valuemax,aria-valuemin,aria-valuenow,aria-valuetext");
var gp = Dn(hu, pp, hp);
var mp = Re("script,style,template");
var ps = class {
  sanitizedSomething = false;
  buf = [];
  sanitizeChildren(t) {
    let n = t.firstChild, r = true, o = [];
    for (; n; ) {
      if (n.nodeType === Node.ELEMENT_NODE ? r = this.startElement(n) : n.nodeType === Node.TEXT_NODE ? this.chars(n.nodeValue) : this.sanitizedSomething = true, r && n.firstChild) {
        o.push(n), n = Ep(n);
        continue;
      }
      for (; n; ) {
        n.nodeType === Node.ELEMENT_NODE && this.endElement(n);
        let i = vp(n);
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
    let n = yl(t).toLowerCase();
    if (!ml.hasOwnProperty(n))
      return this.sanitizedSomething = true, !mp.hasOwnProperty(n);
    this.buf.push("<"), this.buf.push(n);
    let r = t.attributes;
    for (let o = 0; o < r.length; o++) {
      let i = r.item(o), s = i.name, a = s.toLowerCase();
      if (!gp.hasOwnProperty(a)) {
        this.sanitizedSomething = true;
        continue;
      }
      let c = i.value;
      hu[a] && (c = Yr(c)), this.buf.push(" ", s, '="', vl(c), '"');
    }
    return this.buf.push(">"), true;
  }
  endElement(t) {
    let n = yl(t).toLowerCase();
    ml.hasOwnProperty(n) && !du.hasOwnProperty(n) && (this.buf.push("</"), this.buf.push(n), this.buf.push(">"));
  }
  chars(t) {
    this.buf.push(vl(t));
  }
};
function yp(e12, t) {
  return (e12.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_CONTAINED_BY) !== Node.DOCUMENT_POSITION_CONTAINED_BY;
}
function vp(e12) {
  let t = e12.nextSibling;
  if (t && e12 !== t.previousSibling)
    throw gu(t);
  return t;
}
function Ep(e12) {
  let t = e12.firstChild;
  if (t && yp(e12, t))
    throw gu(t);
  return t;
}
function yl(e12) {
  let t = e12.nodeName;
  return typeof t == "string" ? t : "FORM";
}
function gu(e12) {
  return new Error(`Failed to sanitize html because the element is clobbered: ${e12.outerHTML}`);
}
var Ip = /[\uD800-\uDBFF][\uDC00-\uDFFF]/g;
var Dp = /([^\#-~ |!])/g;
function vl(e12) {
  return e12.replace(/&/g, "&amp;").replace(Ip, function(t) {
    let n = t.charCodeAt(0), r = t.charCodeAt(1);
    return "&#" + ((n - 55296) * 1024 + (r - 56320) + 65536) + ";";
  }).replace(Dp, function(t) {
    return "&#" + t.charCodeAt(0) + ";";
  }).replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
var Mr;
function Kr(e12, t) {
  let n = null;
  try {
    Mr = Mr || ap(e12);
    let r = t ? String(t) : "";
    n = Mr.getInertBodyElement(r);
    let o = 5, i = r;
    do {
      if (o === 0)
        throw new Error("Failed to sanitize html because the input is unstable");
      o--, r = i, i = n.innerHTML, n = Mr.getInertBodyElement(r);
    } while (r !== i);
    let a = new ps().sanitizeChildren(El(n) || n);
    return Qr(a);
  } finally {
    if (n) {
      let r = El(n) || n;
      for (; r.firstChild; )
        r.firstChild.remove();
    }
  }
}
function El(e12) {
  return "content" in e12 && bp(e12) ? e12.content : null;
}
function bp(e12) {
  return e12.nodeType === Node.ELEMENT_NODE && e12.nodeName === "TEMPLATE";
}
function Cp(e12, t) {
  return e12.createText(t);
}
function wp(e12, t, n) {
  e12.setValue(t, n);
}
function mu(e12, t, n) {
  return e12.createElement(t, n);
}
function Fr(e12, t, n, r, o) {
  e12.insertBefore(t, n, r, o);
}
function yu(e12, t, n) {
  e12.appendChild(t, n);
}
function Il(e12, t, n, r, o) {
  r !== null ? Fr(e12, t, n, r, o) : yu(e12, t, n);
}
function vu(e12, t, n, r) {
  e12.removeChild(null, t, n, r);
}
function Tp(e12, t, n) {
  e12.setAttribute(t, "style", n);
}
function Mp(e12, t, n) {
  n === "" ? e12.removeAttribute(t, "class") : e12.setAttribute(t, "class", n);
}
function Eu(e12, t, n) {
  let { mergedAttrs: r, classes: o, styles: i } = n;
  r !== null && Ff(e12, t, r), o !== null && Mp(e12, t, o), i !== null && Tp(e12, t, i);
}
var ve = function(e12) {
  return e12[e12.NONE = 0] = "NONE", e12[e12.HTML = 1] = "HTML", e12[e12.STYLE = 2] = "STYLE", e12[e12.SCRIPT = 3] = "SCRIPT", e12[e12.URL = 4] = "URL", e12[e12.RESOURCE_URL = 5] = "RESOURCE_URL", e12;
}(ve || {});
function Ys(e12) {
  let t = _p();
  return t ? gl(t.sanitize(ve.HTML, e12) || "") : We(e12, "HTML") ? gl(xe(e12)) : Kr(ru(), gi(e12));
}
function _p() {
  let e12 = T();
  return e12 && e12[pe].sanitizer;
}
var Sp = "ng-template";
function Np(e12) {
  return e12.type === 4 && e12.value !== Sp;
}
function hs(e12) {
  return (e12 & 1) === 0;
}
function Dl(e12, t) {
  return e12 ? ":not(" + t.trim() + ")" : t;
}
function xp(e12) {
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
      o !== "" && !hs(s) && (t += Dl(i, o), o = ""), r = s, i = i || !hs(r);
    n++;
  }
  return o !== "" && (t += Dl(i, o)), t;
}
function Rp(e12) {
  return e12.map(xp).join(",");
}
function Ap(e12) {
  let t = [], n = [], r = 1, o = 2;
  for (; r < e12.length; ) {
    let i = e12[r];
    if (typeof i == "string")
      o === 2 ? i !== "" && t.push(i, e12[++r]) : o === 8 && n.push(i);
    else {
      if (!hs(o))
        break;
      o = i;
    }
    r++;
  }
  return n.length && t.push(1, ...n), t;
}
var Ae = {};
function Ks(e12, t, n, r, o, i, s, a, c, l, u) {
  let d = $ + r, p = d + o, f = Op(d, p), h = typeof l == "function" ? l() : l;
  return f[m] = { type: e12, blueprint: f, template: n, queries: null, viewQuery: a, declTNode: t, data: f.slice().fill(null, d), bindingStartIndex: d, expandoStartIndex: p, hostBindingOpCodes: null, firstCreatePass: true, firstUpdatePass: true, staticViewQueries: false, staticContentQueries: false, preOrderHooks: null, preOrderCheckHooks: null, contentHooks: null, contentCheckHooks: null, viewHooks: null, viewCheckHooks: null, destroyHooks: null, cleanup: null, contentQueries: null, components: null, directiveRegistry: typeof i == "function" ? i() : i, pipeRegistry: typeof s == "function" ? s() : s, firstChild: null, schemas: c, consts: h, incompleteFirstPass: false, ssrId: u };
}
function Op(e12, t) {
  let n = [];
  for (let r = 0; r < t; r++)
    n.push(r < e12 ? null : Ae);
  return n;
}
function kp(e12) {
  let t = e12.tView;
  return t === null || t.incompleteFirstPass ? e12.tView = Ks(1, null, e12.template, e12.decls, e12.vars, e12.directiveDefs, e12.pipeDefs, e12.viewQuery, e12.schemas, e12.consts, e12.id) : t;
}
function Js(e12, t, n, r, o, i, s, a, c, l, u) {
  let d = t.blueprint.slice();
  return d[ie] = o, d[y] = r | 4 | 128 | 8 | 64 | 1024, (l !== null || e12 && e12[y] & 2048) && (d[y] |= 2048), xi(d), d[k] = d[ot] = e12, d[N] = n, d[pe] = s || e12 && e12[pe], d[P] = a || e12 && e12[P], d[Ce] = c || e12 && e12[Ce] || null, d[te] = i, d[we] = Kf(), d[St] = u, d[Ti] = l, d[ne] = t.type == 2 ? e12[ne] : d, d;
}
function Pp(e12, t, n) {
  let r = ge(t, e12), o = kp(n), i = e12[pe].rendererFactory, s = Xs(e12, Js(e12, o, null, Iu(n), r, t, null, i.createRenderer(r, n), null, null, null));
  return e12[t.index] = s;
}
function Iu(e12) {
  let t = 16;
  return e12.signals ? t = 4096 : e12.onPush && (t = 64), t;
}
function Du(e12, t, n, r) {
  if (n === 0)
    return -1;
  let o = t.length;
  for (let i = 0; i < n; i++)
    t.push(r), e12.blueprint.push(r), e12.data.push(null);
  return o;
}
function Xs(e12, t) {
  return e12[xt] ? e12[wi][ee] = t : e12[xt] = t, e12[wi] = t, t;
}
function j(e12 = 1) {
  bu(Q(), T(), Ue() + e12, false);
}
function bu(e12, t, n, r) {
  if (!r)
    if ((t[y] & 3) === 3) {
      let i = e12.preOrderCheckHooks;
      i !== null && Sr(t, i, n);
    } else {
      let i = e12.preOrderHooks;
      i !== null && Nr(t, i, 0, n);
    }
  ze(n);
}
var Jr = function(e12) {
  return e12[e12.None = 0] = "None", e12[e12.SignalBased = 1] = "SignalBased", e12[e12.HasDecoratorInputTransform = 2] = "HasDecoratorInputTransform", e12;
}(Jr || {});
function gs(e12, t, n, r) {
  let o = g(null);
  try {
    let [i, s, a] = e12.inputs[n], c = null;
    (s & Jr.SignalBased) !== 0 && (c = t[i][K]), c !== null && c.transformFn !== void 0 ? r = c.transformFn(r) : a !== null && (r = a.call(t, r)), e12.setInput !== null ? e12.setInput(t, c, r, n, i) : Hl(t, c, i, r);
  } finally {
    g(o);
  }
}
var Ne = function(e12) {
  return e12[e12.Important = 1] = "Important", e12[e12.DashCase = 2] = "DashCase", e12;
}(Ne || {});
var Lp;
function ea(e12, t) {
  return Lp(e12, t);
}
var sI = typeof document < "u" && typeof document?.documentElement?.getAnimations == "function";
var ms = /* @__PURE__ */ new WeakMap();
var cn = /* @__PURE__ */ new WeakSet();
function Fp(e12, t) {
  let n = ms.get(e12);
  if (!n || n.length === 0)
    return;
  let r = t.parentNode, o = t.previousSibling;
  for (let i = n.length - 1; i >= 0; i--) {
    let s = n[i], a = s.parentNode;
    s === t ? (n.splice(i, 1), cn.add(s), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } }))) : (o && s === o || a && r && a !== r) && (n.splice(i, 1), s.dispatchEvent(new CustomEvent("animationend", { detail: { cancel: true } })), s.parentNode?.removeChild(s));
  }
}
function jp(e12, t) {
  let n = ms.get(e12);
  n ? n.includes(t) || n.push(t) : ms.set(e12, [t]);
}
var ft = /* @__PURE__ */ new Set();
var ta = function(e12) {
  return e12[e12.CHANGE_DETECTION = 0] = "CHANGE_DETECTION", e12[e12.AFTER_NEXT_RENDER = 1] = "AFTER_NEXT_RENDER", e12;
}(ta || {});
var Ut = new D("");
var bl = /* @__PURE__ */ new Set();
function gt(e12) {
  bl.has(e12) || (bl.add(e12), performance?.mark?.("mark_feature_usage", { detail: { feature: e12 } }));
}
var Cu = (() => {
  class e12 {
    impl = null;
    execute() {
      this.impl?.execute();
    }
    static \u0275prov = _({ token: e12, providedIn: "root", factory: () => new e12() });
  }
  return e12;
})();
var wu = new D("", { factory: () => ({ queue: /* @__PURE__ */ new Set(), isScheduled: false, scheduler: null, injector: E(J) }) });
function Tu(e12, t, n) {
  let r = e12.get(wu);
  if (Array.isArray(t))
    for (let o of t)
      r.queue.add(o), n?.detachedLeaveAnimationFns?.push(o);
  else
    r.queue.add(t), n?.detachedLeaveAnimationFns?.push(t);
  r.scheduler && r.scheduler(e12);
}
function Hp(e12, t) {
  let n = e12.get(wu);
  if (t.detachedLeaveAnimationFns) {
    for (let r of t.detachedLeaveAnimationFns)
      n.queue.delete(r);
    t.detachedLeaveAnimationFns = void 0;
  }
}
function Vp(e12, t) {
  for (let [n, r] of t)
    Tu(e12, r.animateFns);
}
function Cl(e12, t, n, r) {
  let o = e12?.[Ve]?.enter;
  t !== null && o && o.has(n.index) && Vp(r, o);
}
function Ft(e12, t, n, r, o, i, s, a) {
  if (o != null) {
    let c, l = false;
    se(o) ? c = o : $e(o) && (l = true, o = o[ie]);
    let u = re(o);
    e12 === 0 && r !== null ? (Cl(a, r, i, n), s == null ? yu(t, r, u) : Fr(t, r, u, s || null, true)) : e12 === 1 && r !== null ? (Cl(a, r, i, n), Fr(t, r, u, s || null, true), Fp(i, u)) : e12 === 2 ? (a?.[Ve]?.leave?.has(i.index) && jp(i, u), cn.delete(u), wl(a, i, n, (d) => {
      if (cn.has(u)) {
        cn.delete(u);
        return;
      }
      vu(t, u, l, d);
    })) : e12 === 3 && (cn.delete(u), wl(a, i, n, () => {
      t.destroyNode(u);
    })), c != null && Xp(t, e12, n, c, i, r, s);
  }
}
function Bp(e12, t) {
  Mu(e12, t), t[ie] = null, t[te] = null;
}
function $p(e12, t, n, r, o, i) {
  r[ie] = o, r[te] = t, eo(e12, r, n, 1, o, i);
}
function Mu(e12, t) {
  t[pe].changeDetectionScheduler?.notify(9), eo(e12, t, t[P], 2, null, null);
}
function Up(e12) {
  let t = e12[xt];
  if (!t)
    return Zi(e12[m], e12);
  for (; t; ) {
    let n = null;
    if ($e(t))
      n = t[xt];
    else {
      let r = t[S];
      r && (n = r);
    }
    if (!n) {
      for (; t && !t[ee] && t !== e12; )
        $e(t) && Zi(t[m], t), t = t[k];
      t === null && (t = e12), $e(t) && Zi(t[m], t), n = t && t[ee];
    }
    t = n;
  }
}
function na(e12, t) {
  let n = e12[st], r = n.indexOf(t);
  n.splice(r, 1);
}
function Xr(e12, t) {
  if (ct(t))
    return;
  let n = t[P];
  n.destroyNode && eo(e12, t, n, 3, null, null), Up(t);
}
function Zi(e12, t) {
  if (ct(t))
    return;
  let n = g(null);
  try {
    t[y] &= -129, t[y] |= 256, t[Z] && yt(t[Z]), Gp(e12, t), Wp(e12, t), t[m].type === 1 && t[P].destroy();
    let r = t[He];
    if (r !== null && se(t[k])) {
      r !== t[k] && na(r, t);
      let o = t[he];
      o !== null && o.detachView(e12);
    }
    rs(t);
  } finally {
    g(n);
  }
}
function wl(e12, t, n, r) {
  let o = e12?.[Ve];
  if (o == null || o.leave == null || !o.leave.has(t.index))
    return r(false);
  e12 && ft.add(e12[we]), Tu(n, () => {
    if (o.leave && o.leave.has(t.index)) {
      let s = o.leave.get(t.index), a = [];
      if (s) {
        for (let c = 0; c < s.animateFns.length; c++) {
          let l = s.animateFns[c], { promise: u } = l();
          a.push(u);
        }
        o.detachedLeaveAnimationFns = void 0;
      }
      o.running = Promise.allSettled(a), zp(e12, r);
    } else
      e12 && ft.delete(e12[we]), r(false);
  }, o);
}
function zp(e12, t) {
  let n = e12[Ve]?.running;
  if (n) {
    n.then(() => {
      e12[Ve].running = void 0, ft.delete(e12[we]), t(true);
    });
    return;
  }
  t(false);
}
function Wp(e12, t) {
  let n = e12.cleanup, r = t[Nt];
  if (n !== null)
    for (let s = 0; s < n.length - 1; s += 2)
      if (typeof n[s] == "string") {
        let a = n[s + 3];
        a >= 0 ? r[a]() : r[-a].unsubscribe(), s += 2;
      } else {
        let a = r[n[s + 1]];
        n[s].call(a);
      }
  r !== null && (t[Nt] = null);
  let o = t[De];
  if (o !== null) {
    t[De] = null;
    for (let s = 0; s < o.length; s++) {
      let a = o[s];
      a();
    }
  }
  let i = t[Le];
  if (i !== null) {
    t[Le] = null;
    for (let s of i)
      s.destroy();
  }
}
function Gp(e12, t) {
  let n;
  if (e12 != null && (n = e12.destroyHooks) != null)
    for (let r = 0; r < n.length; r += 2) {
      let o = t[n[r]];
      if (!(o instanceof dt)) {
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
function qp(e12, t, n) {
  return Zp(e12, t.parent, n);
}
function Zp(e12, t, n) {
  let r = t;
  for (; r !== null && r.type & 168; )
    t = r, r = t.parent;
  if (r === null)
    return n[ie];
  if (Rt(r)) {
    let { encapsulation: o } = e12.data[r.directiveStart + r.componentOffset];
    if (o === ce.None || o === ce.Emulated)
      return null;
  }
  return ge(r, n);
}
function Qp(e12, t, n) {
  return Kp(e12, t, n);
}
function Yp(e12, t, n) {
  return e12.type & 40 ? ge(e12, n) : null;
}
var Kp = Yp;
var Tl;
function ra(e12, t, n, r) {
  let o = qp(e12, r, t), i = t[P], s = r.parent || t[te], a = Qp(s, r, t);
  if (o != null)
    if (Array.isArray(n))
      for (let c = 0; c < n.length; c++)
        Il(i, o, n[c], a, false);
    else
      Il(i, o, n, a, false);
  Tl !== void 0 && Tl(i, r, t, n, o);
}
function ln(e12, t) {
  if (t !== null) {
    let n = t.type;
    if (n & 3)
      return ge(t, e12);
    if (n & 4)
      return ys(-1, e12[t.index]);
    if (n & 8) {
      let r = t.child;
      if (r !== null)
        return ln(e12, r);
      {
        let o = e12[t.index];
        return se(o) ? ys(-1, o) : re(o);
      }
    } else {
      if (n & 128)
        return ln(e12, t.next);
      if (n & 32)
        return ea(t, e12)() || re(e12[t.index]);
      {
        let r = _u(e12, t);
        if (r !== null) {
          if (Array.isArray(r))
            return r[0];
          let o = Fe(e12[ne]);
          return ln(o, r);
        } else
          return ln(e12, t.next);
      }
    }
  }
  return null;
}
function _u(e12, t) {
  if (t !== null) {
    let r = e12[ne][te], o = t.projection;
    return r.projection[o];
  }
  return null;
}
function ys(e12, t) {
  let n = S + e12 + 1;
  if (n < t.length) {
    let r = t[n], o = r[m].firstChild;
    if (o !== null)
      return ln(r, o);
  }
  return t[Be];
}
function oa(e12, t, n, r, o, i, s) {
  for (; n != null; ) {
    let a = r[Ce];
    if (n.type === 128) {
      n = n.next;
      continue;
    }
    let c = r[n.index], l = n.type;
    if (s && t === 0 && (c && Ht(re(c), r), n.flags |= 2), !zs(n))
      if (l & 8)
        oa(e12, t, n.child, r, o, i, false), Ft(t, e12, a, o, c, n, i, r);
      else if (l & 32) {
        let u = ea(n, r), d;
        for (; d = u(); )
          Ft(t, e12, a, o, d, n, i, r);
        Ft(t, e12, a, o, c, n, i, r);
      } else
        l & 16 ? Jp(e12, t, r, n, o, i) : Ft(t, e12, a, o, c, n, i, r);
    n = s ? n.projectionNext : n.next;
  }
}
function eo(e12, t, n, r, o, i) {
  oa(n, r, e12.firstChild, t, o, i, false);
}
function Jp(e12, t, n, r, o, i) {
  let s = n[ne], c = s[te].projection[r.projection];
  if (Array.isArray(c))
    for (let l = 0; l < c.length; l++) {
      let u = c[l];
      Ft(t, e12, n[Ce], o, u, r, i, n);
    }
  else {
    let l = c, u = s[k];
    Jl(r) && (l.flags |= 128), oa(e12, t, l, u, o, i, true);
  }
}
function Xp(e12, t, n, r, o, i, s) {
  let a = r[Be], c = re(r);
  a !== c && Ft(t, e12, n, i, a, o, s);
  for (let l = S; l < r.length; l++) {
    let u = r[l];
    eo(u[m], u, e12, t, i, a);
  }
}
function eh(e12, t, n, r, o) {
  if (t)
    o ? e12.addClass(n, r) : e12.removeClass(n, r);
  else {
    let i = r.indexOf("-") === -1 ? void 0 : Ne.DashCase;
    o == null ? e12.removeStyle(n, r, i) : (typeof o == "string" && o.endsWith("!important") && (o = o.slice(0, -10), i |= Ne.Important), e12.setStyle(n, r, o, i));
  }
}
function Su(e12, t, n, r, o) {
  let i = Ue(), s = r & 2;
  try {
    ze(-1), s && t.length > $ && bu(e12, t, $, false);
    let a = s ? C.TemplateUpdateStart : C.TemplateCreateStart;
    M(a, o, n), n(r, o);
  } finally {
    ze(i);
    let a = s ? C.TemplateUpdateEnd : C.TemplateCreateEnd;
    M(a, o, n);
  }
}
function th(e12, t, n) {
  sh(e12, t, n), (n.flags & 64) === 64 && ah(e12, t, n);
}
function Nu(e12, t, n = ge) {
  let r = t.localNames;
  if (r !== null) {
    let o = t.index + 1;
    for (let i = 0; i < r.length; i += 2) {
      let s = r[i + 1], a = s === -1 ? n(t, e12) : e12[s];
      e12[o++] = a;
    }
  }
}
function nh(e12, t, n, r) {
  let i = r.get(au, su) || n === ce.ShadowDom || n === ce.ExperimentalIsolatedShadowDom, s = e12.selectRootElement(t, i);
  return rh(s), s;
}
function rh(e12) {
  oh(e12);
}
var oh = () => null;
function ih(e12, t, n, r, o, i) {
  if (e12.type & 3) {
    let s = ge(e12, t);
    r = i != null ? i(r, e12.value || "", n) : r, o.setProperty(s, n, r);
  } else
    e12.type & 12;
}
function sh(e12, t, n) {
  let r = n.directiveStart, o = n.directiveEnd;
  Rt(n) && Pp(t, n, e12.data[r + n.componentOffset]), e12.firstCreatePass || Pr(n, t);
  let i = n.initialInputs;
  for (let s = r; s < o; s++) {
    let a = e12.data[s], c = dn(t, e12, s, n);
    if (Ht(c, t), i !== null && lh(t, s - r, c, a, n, i), at(a)) {
      let l = Te(n.index, t);
      l[N] = dn(t, e12, s, n);
    }
  }
}
function ah(e12, t, n) {
  let r = n.directiveStart, o = n.directiveEnd, i = n.index, s = Uc();
  try {
    ze(i);
    for (let a = r; a < o; a++) {
      let c = e12.data[a], l = t[a];
      gr(a), (c.hostBindings !== null || c.hostVars !== 0 || c.hostAttrs !== null) && ch(c, l);
    }
  } finally {
    ze(-1), gr(s);
  }
}
function ch(e12, t) {
  e12.hostBindings !== null && e12.hostBindings(1, t);
}
function lh(e12, t, n, r, o, i) {
  let s = i[t];
  if (s !== null)
    for (let a = 0; a < s.length; a += 2) {
      let c = s[a], l = s[a + 1];
      gs(r, n, c, l);
    }
}
function uh(e12, t, n, r, o) {
  let i = $ + n, s = t[m], a = o(s, t, e12, r, n);
  t[i] = a, kt(e12, true);
  let c = e12.type === 2;
  return c ? (Eu(t[P], a, e12), (Rc() === 0 || Si(e12)) && Ht(a, t), Ac()) : Ht(a, t), Er() && (!c || !zs(e12)) && ra(s, t, a, e12), e12;
}
function dh(e12) {
  let t = e12;
  return Li() ? jc() : (t = t.parent, kt(t, false)), t;
}
function fh(e12, t) {
  let n = e12[Ce];
  if (!n)
    return;
  let r;
  try {
    r = n.get(lt, null);
  } catch {
    r = null;
  }
  r?.(t);
}
function ph(e12, t, n, r, o) {
  let i = e12.inputs?.[r], s = e12.hostDirectiveInputs?.[r], a = false;
  if (s)
    for (let c = 0; c < s.length; c += 2) {
      let l = s[c], u = s[c + 1], d = t.data[l];
      gs(d, n[l], u, o), a = true;
    }
  if (i)
    for (let c of i) {
      let l = n[c], u = t.data[c];
      gs(u, l, r, o), a = true;
    }
  return a;
}
function hh(e12, t) {
  let n = Te(t, e12), r = n[m];
  gh(r, n);
  let o = n[ie];
  o !== null && n[St] === null && (n[St] = cu(o, n[Ce])), M(C.ComponentStart);
  try {
    ia(r, n, n[N]);
  } finally {
    M(C.ComponentEnd, n[N]);
  }
}
function gh(e12, t) {
  for (let n = t.length; n < e12.blueprint.length; n++)
    t.push(e12.blueprint[n]);
}
function ia(e12, t, n) {
  yr(t);
  try {
    let r = e12.viewQuery;
    r !== null && is(1, r, n);
    let o = e12.template;
    o !== null && Su(e12, t, o, 1, n), e12.firstCreatePass && (e12.firstCreatePass = false), t[he]?.finishViewCreation(e12), e12.staticContentQueries && lu(e12, t), e12.staticViewQueries && is(2, e12.viewQuery, n);
    let i = e12.components;
    i !== null && mh(t, i);
  } catch (r) {
    throw e12.firstCreatePass && (e12.incompleteFirstPass = true, e12.firstCreatePass = false), r;
  } finally {
    t[y] &= -5, vr();
  }
}
function mh(e12, t) {
  for (let n = 0; n < t.length; n++)
    hh(e12, t[n]);
}
function to(e12, t, n, r) {
  let o = g(null);
  try {
    let i = t.tView, a = e12[y] & 4096 ? 4096 : 16, c = Js(e12, i, n, a, null, t, null, null, r?.injector ?? null, r?.embeddedViewInjector ?? null, r?.dehydratedView ?? null), l = e12[t.index];
    c[He] = l;
    let u = e12[he];
    return u !== null && (c[he] = u.createEmbeddedView(i)), ia(i, c, n), c;
  } finally {
    g(o);
  }
}
function fn(e12, t) {
  return !t || t.firstChild === null || Jl(e12);
}
function pn(e12, t, n, r, o = false) {
  for (; n !== null; ) {
    if (n.type === 128) {
      n = o ? n.projectionNext : n.next;
      continue;
    }
    let i = t[n.index];
    i !== null && r.push(re(i)), se(i) && xu(i, r);
    let s = n.type;
    if (s & 8)
      pn(e12, t, n.child, r);
    else if (s & 32) {
      let a = ea(n, t), c;
      for (; c = a(); )
        r.push(c);
    } else if (s & 16) {
      let a = _u(t, n);
      if (Array.isArray(a))
        r.push(...a);
      else {
        let c = Fe(t[ne]);
        pn(c[m], c, a, r, true);
      }
    }
    n = o ? n.projectionNext : n.next;
  }
  return r;
}
function xu(e12, t) {
  for (let n = S; n < e12.length; n++) {
    let r = e12[n], o = r[m].firstChild;
    o !== null && pn(r[m], r, o, t);
  }
  e12[Be] !== e12[ie] && t.push(e12[Be]);
}
function Ru(e12) {
  if (e12[dr] !== null) {
    for (let t of e12[dr])
      t.impl.addSequence(t);
    e12[dr].length = 0;
  }
}
var Au = [];
function yh(e12) {
  return e12[Z] ?? vh(e12);
}
function vh(e12) {
  let t = Au.pop() ?? Object.create(Ih);
  return t.lView = e12, t;
}
function Eh(e12) {
  e12.lView[Z] !== e12 && (e12.lView = null, Au.push(e12));
}
var Ih = O(A({}, mt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e12) => {
  Ot(e12.lView);
}, consumerOnSignalRead() {
  this.lView[Z] = this;
} });
function Dh(e12) {
  let t = e12[Z] ?? Object.create(bh);
  return t.lView = e12, t;
}
var bh = O(A({}, mt), { consumerIsAlwaysLive: true, kind: "template", consumerMarkedDirty: (e12) => {
  let t = Fe(e12.lView);
  for (; t && !Ou(t[m]); )
    t = Fe(t);
  t && Ri(t);
}, consumerOnSignalRead() {
  this.lView[Z] = this;
} });
function Ou(e12) {
  return e12.type !== 2;
}
function ku(e12) {
  if (e12[Le] === null)
    return;
  let t = true;
  for (; t; ) {
    let n = false;
    for (let r of e12[Le])
      r.dirty && (n = true, r.zone === null || Zone.current === r.zone ? r.run() : r.zone.run(() => r.run()));
    t = n && !!(e12[y] & 8192);
  }
}
var Ch = 100;
function Pu(e12, t = 0) {
  let r = e12[pe].rendererFactory, o = false;
  o || r.begin?.();
  try {
    wh(e12, t);
  } finally {
    o || r.end?.();
  }
}
function wh(e12, t) {
  let n = Fi();
  try {
    Kt(true), vs(e12, t);
    let r = 0;
    for (; on(e12); ) {
      if (r === Ch)
        throw new v(103, false);
      r++, vs(e12, 1);
    }
  } finally {
    Kt(n);
  }
}
function Th(e12, t, n, r) {
  if (ct(t))
    return;
  let o = t[y], i = false, s = false;
  yr(t);
  let a = true, c = null, l = null;
  i || (Ou(e12) ? (l = yh(t), c = Gt(l)) : jn() === null ? (a = false, l = Dh(t), c = Gt(l)) : t[Z] && (yt(t[Z]), t[Z] = null));
  try {
    xi(t), Hc(e12.bindingStartIndex), n !== null && Su(e12, t, n, 2, r);
    let u = (o & 3) === 3;
    if (!i)
      if (u) {
        let f = e12.preOrderCheckHooks;
        f !== null && Sr(t, f, null);
      } else {
        let f = e12.preOrderHooks;
        f !== null && Nr(t, f, 0, null), Gi(t, 0);
      }
    if (s || Mh(t), ku(t), Lu(t, 0), e12.contentQueries !== null && lu(e12, t), !i)
      if (u) {
        let f = e12.contentCheckHooks;
        f !== null && Sr(t, f);
      } else {
        let f = e12.contentHooks;
        f !== null && Nr(t, f, 1), Gi(t, 1);
      }
    Sh(e12, t);
    let d = e12.components;
    d !== null && ju(t, d, 0);
    let p = e12.viewQuery;
    if (p !== null && is(2, p, r), !i)
      if (u) {
        let f = e12.viewCheckHooks;
        f !== null && Sr(t, f);
      } else {
        let f = e12.viewHooks;
        f !== null && Nr(t, f, 2), Gi(t, 2);
      }
    if (e12.firstUpdatePass === true && (e12.firstUpdatePass = false), t[ur]) {
      for (let f of t[ur])
        f();
      t[ur] = null;
    }
    i || (Ru(t), t[y] &= -73);
  } catch (u) {
    throw i || Ot(t), u;
  } finally {
    l !== null && (Hn(l, c), a && Eh(l)), vr();
  }
}
function Lu(e12, t) {
  for (let n = eu(e12); n !== null; n = tu(n))
    for (let r = S; r < n.length; r++) {
      let o = n[r];
      Fu(o, t);
    }
}
function Mh(e12) {
  for (let t = eu(e12); t !== null; t = tu(t)) {
    if (!(t[y] & 2))
      continue;
    let n = t[st];
    for (let r = 0; r < n.length; r++) {
      let o = n[r];
      Ri(o);
    }
  }
}
function _h(e12, t, n) {
  M(C.ComponentStart);
  let r = Te(t, e12);
  try {
    Fu(r, n);
  } finally {
    M(C.ComponentEnd, r[N]);
  }
}
function Fu(e12, t) {
  pr(e12) && vs(e12, t);
}
function vs(e12, t) {
  let r = e12[m], o = e12[y], i = e12[Z], s = !!(t === 0 && o & 16);
  if (s ||= !!(o & 64 && t === 0), s ||= !!(o & 1024), s ||= !!(i?.dirty && Vn(i)), s ||= false, i && (i.dirty = false), e12[y] &= -9217, s)
    Th(r, e12, r.template, e12[N]);
  else if (o & 8192) {
    let a = g(null);
    try {
      ku(e12), Lu(e12, 1);
      let c = r.components;
      c !== null && ju(e12, c, 1), Ru(e12);
    } finally {
      g(a);
    }
  }
}
function ju(e12, t, n) {
  for (let r = 0; r < t.length; r++)
    _h(e12, t[r], n);
}
function Sh(e12, t) {
  let n = e12.hostBindingOpCodes;
  if (n !== null)
    try {
      for (let r = 0; r < n.length; r++) {
        let o = n[r];
        if (o < 0)
          ze(~o);
        else {
          let i = o, s = n[++r], a = n[++r];
          $c(s, i);
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
      ze(-1);
    }
}
function sa(e12, t) {
  let n = Fi() ? 64 : 1088;
  for (e12[pe].changeDetectionScheduler?.notify(t); e12; ) {
    e12[y] |= n;
    let r = Fe(e12);
    if (At(e12) && !r)
      return e12;
    e12 = r;
  }
  return null;
}
function Hu(e12, t, n, r) {
  return [e12, true, 0, t, null, r, null, n, null, null];
}
function Vu(e12, t) {
  let n = S + t;
  if (n < e12.length)
    return e12[n];
}
function no(e12, t, n, r = true) {
  let o = t[m];
  if (Nh(o, t, e12, n), r) {
    let s = ys(n, e12), a = t[P], c = a.parentNode(e12[Be]);
    c !== null && $p(o, e12[te], a, t, c, s);
  }
  let i = t[St];
  i !== null && i.firstChild !== null && (i.firstChild = null);
}
function Bu(e12, t) {
  let n = hn(e12, t);
  return n !== void 0 && Xr(n[m], n), n;
}
function hn(e12, t) {
  if (e12.length <= S)
    return;
  let n = S + t, r = e12[n];
  if (r) {
    let o = r[He];
    o !== null && o !== e12 && na(o, r), t > 0 && (e12[n - 1][ee] = r[ee]);
    let i = en(e12, S + t);
    Bp(r[m], r);
    let s = i[he];
    s !== null && s.detachView(i[m]), r[k] = null, r[ee] = null, r[y] &= -129;
  }
  return r;
}
function Nh(e12, t, n, r) {
  let o = S + r, i = n.length;
  r > 0 && (n[o - 1][ee] = t), r < i - S ? (t[ee] = n[o], vi(n, S + r, t)) : (n.push(t), t[ee] = null), t[k] = n;
  let s = t[He];
  s !== null && n !== s && $u(s, t);
  let a = t[he];
  a !== null && a.insertView(e12), hr(t), t[y] |= 128;
}
function $u(e12, t) {
  let n = e12[st], r = t[k];
  if ($e(r))
    e12[y] |= 2;
  else {
    let o = r[k][ne];
    t[ne] !== o && (e12[y] |= 2);
  }
  n === null ? e12[st] = [t] : n.push(t);
}
var Vt = class {
  _lView;
  _cdRefInjectingView;
  _appRef = null;
  _attachedToViewContainer = false;
  exhaustive;
  get rootNodes() {
    let t = this._lView, n = t[m];
    return pn(n, t, n.firstChild, []);
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
    return ct(this._lView);
  }
  destroy() {
    if (this._appRef)
      this._appRef.detachView(this);
    else if (this._attachedToViewContainer) {
      let t = this._lView[k];
      if (se(t)) {
        let n = t[rn], r = n ? n.indexOf(this) : -1;
        r > -1 && (hn(t, r), en(n, r));
      }
      this._attachedToViewContainer = false;
    }
    Xr(this._lView[m], this._lView);
  }
  onDestroy(t) {
    Ai(this._lView, t);
  }
  markForCheck() {
    sa(this._cdRefInjectingView || this._lView, 4);
  }
  detach() {
    this._lView[y] &= -129;
  }
  reattach() {
    hr(this._lView), this._lView[y] |= 128;
  }
  detectChanges() {
    this._lView[y] |= 1024, Pu(this._lView);
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
    let t = At(this._lView), n = this._lView[He];
    n !== null && !t && na(n, this._lView), Mu(this._lView[m], this._lView);
  }
  attachToAppRef(t) {
    if (this._attachedToViewContainer)
      throw new v(902, false);
    this._appRef = t;
    let n = At(this._lView), r = this._lView[He];
    r !== null && !n && $u(r, this._lView), hr(this._lView);
  }
};
var gn = /* @__PURE__ */ (() => {
  class e12 {
    _declarationLView;
    _declarationTContainer;
    elementRef;
    static __NG_ELEMENT_ID__ = xh;
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
      let i = to(this._declarationLView, this._declarationTContainer, n, { embeddedViewInjector: r, dehydratedView: o });
      return new Vt(i);
    }
  }
  return e12;
})();
function xh() {
  return aa(ae(), T());
}
function aa(e12, t) {
  return e12.type & 4 ? new gn(t, e12, $t(e12, t)) : null;
}
function ro(e12, t, n, r, o) {
  let i = e12.data[t];
  if (i === null)
    i = Rh(e12, t, n, r, o), Bc() && (i.flags |= 32);
  else if (i.type & 64) {
    i.type = n, i.value = r, i.attrs = o;
    let s = Fc();
    i.injectorIndex = s === null ? -1 : s.injectorIndex;
  }
  return kt(i, true), i;
}
function Rh(e12, t, n, r, o) {
  let i = Pi(), s = Li(), a = s ? i : i && i.parent, c = e12.data[t] = Oh(e12, a, n, t, r, o);
  return Ah(e12, c, i, s), c;
}
function Ah(e12, t, n, r) {
  e12.firstChild === null && (e12.firstChild = t), n !== null && (r ? n.child == null && t.parent !== null && (n.child = t) : n.next === null && (n.next = t, t.prev = n));
}
function Oh(e12, t, n, r, o, i) {
  let s = t ? t.injectorIndex : -1, a = 0;
  return kc() && (a |= 128), { type: n, index: r, insertBeforeIndex: null, injectorIndex: s, directiveStart: -1, directiveEnd: -1, directiveStylingLast: -1, componentOffset: -1, controlDirectiveIndex: -1, customControlIndex: -1, propertyBindings: null, flags: a, providerIndexes: 0, value: o, attrs: i, mergedAttrs: null, localNames: null, initialInputs: null, inputs: null, hostDirectiveInputs: null, outputs: null, hostDirectiveOutputs: null, directiveToIndex: null, tView: null, next: null, prev: null, projectionNext: null, child: null, parent: t, projection: null, styles: null, stylesWithoutHost: null, residualStyles: void 0, classes: null, classesWithoutHost: null, residualClasses: void 0, classBindings: 0, styleBindings: 0 };
}
function kh(e12) {
  let t = e12[Mi] ?? [], r = e12[k][P], o = [];
  for (let i of t)
    i.data[iu] !== void 0 ? o.push(i) : Ph(i, r);
  e12[Mi] = o;
}
function Ph(e12, t) {
  let n = 0, r = e12.firstChild;
  if (r) {
    let o = e12.data[ou];
    for (; n < o; ) {
      let i = r.nextSibling;
      vu(t, r, false), r = i, n++;
    }
  }
}
var Lh = () => null;
var Fh = () => null;
function Es(e12, t) {
  return Lh(e12, t);
}
function Uu(e12, t, n) {
  return Fh(e12, t, n);
}
var zu = class {
};
var oo = class {
};
var Is = class {
  resolveComponentFactory(t) {
    throw new v(917, false);
  }
};
var io = class {
  static NULL = new Is();
};
var pt = class {
};
var Wu = (() => {
  class e12 {
    static \u0275prov = _({ token: e12, providedIn: "root", factory: () => null });
  }
  return e12;
})();
var Rr = {};
var Ds = class {
  injector;
  parentInjector;
  constructor(t, n) {
    this.injector = t, this.parentInjector = n;
  }
  get(t, n, r) {
    let o = this.injector.get(t, Rr, r);
    return o !== Rr || n === Rr ? o : this.parentInjector.get(t, n, r);
  }
};
function jr(e12, t, n) {
  let r = n ? e12.styles : null, o = n ? e12.classes : null, i = 0;
  if (t !== null)
    for (let s = 0; s < t.length; s++) {
      let a = t[s];
      if (typeof a == "number")
        i = a;
      else if (i == 1)
        o = ci(o, a);
      else if (i == 2) {
        let c = a, l = t[++s];
        r = ci(r, c + ": " + l + ";");
      }
    }
  n ? e12.styles = r : e12.stylesWithoutHost = r, n ? e12.classes = o : e12.classesWithoutHost = o;
}
function so(e12, t = 0) {
  let n = T();
  if (n === null)
    return b(e12, t);
  let r = ae();
  return Ql(r, n, B(e12), t);
}
function jh(e12, t, n, r, o) {
  let i = r === null ? null : { "": -1 }, s = o(e12, n);
  if (s !== null) {
    let a = s, c = null, l = null;
    for (let u of s)
      if (u.resolveHostDirectives !== null) {
        [a, c, l] = u.resolveHostDirectives(s);
        break;
      }
    Bh(e12, t, n, a, i, c, l);
  }
  i !== null && r !== null && Hh(n, r, i);
}
function Hh(e12, t, n) {
  let r = e12.localNames = [];
  for (let o = 0; o < t.length; o += 2) {
    let i = n[t[o + 1]];
    if (i == null)
      throw new v(-301, false);
    r.push(t[o], i);
  }
}
function Vh(e12, t, n) {
  t.componentOffset = n, (e12.components ??= []).push(t.index);
}
function Bh(e12, t, n, r, o, i, s) {
  let a = r.length, c = null;
  for (let p = 0; p < a; p++) {
    let f = r[p];
    c === null && at(f) && (c = f, Vh(e12, n, p)), ns(Pr(n, t), e12, f.type);
  }
  qh(n, e12.data.length, a), c?.viewProvidersResolver && c.viewProvidersResolver(c);
  for (let p = 0; p < a; p++) {
    let f = r[p];
    f.providersResolver && f.providersResolver(f);
  }
  let l = false, u = false, d = Du(e12, t, a, null);
  a > 0 && (n.directiveToIndex = /* @__PURE__ */ new Map());
  for (let p = 0; p < a; p++) {
    let f = r[p];
    if (n.mergedAttrs = Wr(n.mergedAttrs, f.hostAttrs), Uh(e12, n, t, d, f), Gh(d, f, o), s !== null && s.has(f)) {
      let [x, R] = s.get(f);
      n.directiveToIndex.set(f.type, [d, x + n.directiveStart, R + n.directiveStart]);
    } else
      (i === null || !i.has(f)) && n.directiveToIndex.set(f.type, d);
    f.contentQueries !== null && (n.flags |= 4), (f.hostBindings !== null || f.hostAttrs !== null || f.hostVars !== 0) && (n.flags |= 64);
    let h = f.type.prototype;
    !l && (h.ngOnChanges || h.ngOnInit || h.ngDoCheck) && ((e12.preOrderHooks ??= []).push(n.index), l = true), !u && (h.ngOnChanges || h.ngDoCheck) && ((e12.preOrderCheckHooks ??= []).push(n.index), u = true), d++;
  }
  $h(e12, n, i);
}
function $h(e12, t, n) {
  for (let r = t.directiveStart; r < t.directiveEnd; r++) {
    let o = e12.data[r];
    if (n === null || !n.has(o))
      Ml(0, t, o, r), Ml(1, t, o, r), Sl(t, r, false);
    else {
      let i = n.get(o);
      _l(0, t, i, r), _l(1, t, i, r), Sl(t, r, true);
    }
  }
}
function Ml(e12, t, n, r) {
  let o = e12 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s;
      e12 === 0 ? s = t.inputs ??= {} : s = t.outputs ??= {}, s[i] ??= [], s[i].push(r), Gu(t, i);
    }
}
function _l(e12, t, n, r) {
  let o = e12 === 0 ? n.inputs : n.outputs;
  for (let i in o)
    if (o.hasOwnProperty(i)) {
      let s = o[i], a;
      e12 === 0 ? a = t.hostDirectiveInputs ??= {} : a = t.hostDirectiveOutputs ??= {}, a[s] ??= [], a[s].push(r, i), Gu(t, s);
    }
}
function Gu(e12, t) {
  t === "class" ? e12.flags |= 8 : t === "style" && (e12.flags |= 16);
}
function Sl(e12, t, n) {
  let { attrs: r, inputs: o, hostDirectiveInputs: i } = e12;
  if (r === null || !n && o === null || n && i === null || Np(e12)) {
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
function Uh(e12, t, n, r, o) {
  e12.data[r] = o;
  let i = o.factory || (o.factory = Tt(o.type, true)), s = new dt(i, at(o), so, null);
  e12.blueprint[r] = s, n[r] = s, zh(e12, t, r, Du(e12, n, o.hostVars, Ae), o);
}
function zh(e12, t, n, r, o) {
  let i = o.hostBindings;
  if (i) {
    let s = e12.hostBindingOpCodes;
    s === null && (s = e12.hostBindingOpCodes = []);
    let a = ~t.index;
    Wh(s) != a && s.push(a), s.push(n, r, i);
  }
}
function Wh(e12) {
  let t = e12.length;
  for (; t > 0; ) {
    let n = e12[--t];
    if (typeof n == "number" && n < 0)
      return n;
  }
  return 0;
}
function Gh(e12, t, n) {
  if (n) {
    if (t.exportAs)
      for (let r = 0; r < t.exportAs.length; r++)
        n[t.exportAs[r]] = e12;
    at(t) && (n[""] = e12);
  }
}
function qh(e12, t, n) {
  e12.flags |= 1, e12.directiveStart = t, e12.directiveEnd = t + n, e12.providerIndexes = t;
}
function Zh(e12, t, n, r, o, i, s, a) {
  let c = t[m], l = c.consts, u = me(l, s), d = ro(c, e12, n, r, u);
  return i && jh(c, t, d, me(l, a), o), d.mergedAttrs = Wr(d.mergedAttrs, d.attrs), d.attrs !== null && jr(d, d.attrs, false), d.mergedAttrs !== null && jr(d, d.mergedAttrs, true), c.queries !== null && c.queries.elementStart(c, d), d;
}
function Qh(e12, t) {
  Pf(e12, t), _i(t) && e12.queries.elementEnd(t);
}
function Yh(e12, t, n, r, o, i) {
  let s = t.consts, a = me(s, o), c = ro(t, e12, n, r, a);
  if (c.mergedAttrs = Wr(c.mergedAttrs, c.attrs), i != null) {
    let l = me(s, i);
    c.localNames = [];
    for (let u = 0; u < l.length; u += 2)
      c.localNames.push(l[u], -1);
  }
  return c.attrs !== null && jr(c, c.attrs, false), c.mergedAttrs !== null && jr(c, c.mergedAttrs, true), t.queries !== null && t.queries.elementStart(t, c), c;
}
function bn(e12, t, n) {
  if (n === Ae)
    return false;
  let r = e12[t];
  return Object.is(r, n) ? false : (e12[t] = n, true);
}
function Kh(e12, t, n) {
  return function r(o) {
    let i = r.__ngNativeEl__;
    i !== void 0 && ep(o, i);
    let s = Rt(e12) ? Te(e12.index, t) : t;
    sa(s, 5);
    let a = t[N], c = Nl(t, a, n, o), l = r.__ngNextListenerFn__;
    for (; l; )
      c = Nl(t, a, l, o) && c, l = l.__ngNextListenerFn__;
    return c;
  };
}
function Nl(e12, t, n, r) {
  let o = g(null);
  try {
    return M(C.OutputStart, t, n), n(r) !== false;
  } catch (i) {
    return fh(e12, i), false;
  } finally {
    M(C.OutputEnd, t, n), g(o);
  }
}
function Jh(e12, t, n, r, o, i, s, a) {
  let c = Si(e12), l = false, u = null;
  if (!r && c && (u = eg(t, n, i, e12.index)), u !== null) {
    let d = u.__ngLastListenerFn__ || u;
    d.__ngNextListenerFn__ = s, u.__ngLastListenerFn__ = s, l = true;
  } else {
    let d = ge(e12, n), p = r ? r(d) : d;
    np(n, p, i, a), r || (a.__ngNativeEl__ = d);
    let f = o.listen(p, i, a);
    if (!Xh(i)) {
      let h = r ? (x) => r(re(x[e12.index])) : e12.index;
      tg(h, t, n, i, a, f, false);
    }
  }
  return l;
}
function Xh(e12) {
  return e12.startsWith("animation") || e12.startsWith("transition");
}
function eg(e12, t, n, r) {
  let o = e12.cleanup;
  if (o != null)
    for (let i = 0; i < o.length - 1; i += 2) {
      let s = o[i];
      if (s === n && o[i + 1] === r) {
        let a = t[Nt], c = o[i + 2];
        return a && a.length > c ? a[c] : null;
      }
      typeof s == "string" && (i += 2);
    }
  return null;
}
function tg(e12, t, n, r, o, i, s) {
  let a = t.firstCreatePass ? ki(t) : null, c = Oi(n), l = c.length;
  c.push(o, i), a && a.push(r, e12, l, (l + 1) * (s ? -1 : 1));
}
var bs = Symbol("BINDING");
function ng(e12) {
  return e12.debugInfo?.className || e12.type.name || null;
}
var Cs = class extends io {
  ngModule;
  constructor(t) {
    super(), this.ngModule = t;
  }
  resolveComponentFactory(t) {
    let n = tt(t);
    return new mn(n, this.ngModule);
  }
};
function rg(e12) {
  return Object.keys(e12).map((t) => {
    let [n, r, o] = e12[t], i = { propName: n, templateName: t, isSignal: (r & Jr.SignalBased) !== 0 };
    return o && (i.transform = o), i;
  });
}
function og(e12) {
  return Object.keys(e12).map((t) => ({ propName: e12[t], templateName: t }));
}
function ig(e12, t, n) {
  let r = t instanceof J ? t : t?.injector;
  return r && e12.getStandaloneInjector !== null && (r = e12.getStandaloneInjector(r) || r), r ? new Ds(n, r) : n;
}
function sg(e12) {
  let t = e12.get(pt, null);
  if (t === null)
    throw new v(407, false);
  let n = e12.get(Wu, null), r = e12.get(Xe, null), o = e12.get(Ut, null, { optional: true });
  return { rendererFactory: t, sanitizer: n, changeDetectionScheduler: r, ngReflect: false, tracingService: o };
}
function ag(e12, t) {
  let n = qu(e12);
  return mu(t, n, n === "svg" ? wc : n === "math" ? Tc : null);
}
function qu(e12) {
  return (e12.selectors[0][0] || "div").toLowerCase();
}
var mn = class extends oo {
  componentDef;
  ngModule;
  selector;
  componentType;
  ngContentSelectors;
  isBoundToModule;
  cachedInputs = null;
  cachedOutputs = null;
  get inputs() {
    return this.cachedInputs ??= rg(this.componentDef.inputs), this.cachedInputs;
  }
  get outputs() {
    return this.cachedOutputs ??= og(this.componentDef.outputs), this.cachedOutputs;
  }
  constructor(t, n) {
    super(), this.componentDef = t, this.ngModule = n, this.componentType = t.type, this.selector = Rp(t.selectors), this.ngContentSelectors = t.ngContentSelectors ?? [], this.isBoundToModule = !!n;
  }
  create(t, n, r, o, i, s) {
    M(C.DynamicComponentStart);
    let a = g(null);
    try {
      let c = this.componentDef, l = ig(c, o || this.ngModule, t), u = sg(l), d = u.tracingService;
      return d && d.componentCreate ? d.componentCreate(ng(c), () => this.createComponentRef(u, l, n, r, i, s)) : this.createComponentRef(u, l, n, r, i, s);
    } finally {
      g(a);
    }
  }
  createComponentRef(t, n, r, o, i, s) {
    let a = this.componentDef, c = cg(o, a, s, i), l = t.rendererFactory.createRenderer(null, a), u = o ? nh(l, o, a.encapsulation, n) : ag(a, l), d = s?.some(xl) || i?.some((h) => typeof h != "function" && h.bindings.some(xl)), p = Js(null, c, null, 512 | Iu(a), null, null, t, l, n, null, cu(u, n, true));
    p[$] = u, yr(p);
    let f = null;
    try {
      let h = Zh($, p, 2, "#host", () => c.directiveRegistry, true, 0);
      Eu(l, u, h), Ht(u, p), th(c, p, h), op(c, h, p), Qh(c, h), r !== void 0 && ug(h, this.ngContentSelectors, r), f = Te(h.index, p), p[N] = f[N], ia(c, p, null);
    } catch (h) {
      throw f !== null && rs(f), rs(p), h;
    } finally {
      M(C.DynamicComponentEnd), vr();
    }
    return new Hr(this.componentType, p, !!d);
  }
};
function cg(e12, t, n, r) {
  let o = e12 ? ["ng-version", "21.2.11"] : Ap(t.selectors[0]), i = null, s = null, a = 0;
  if (n)
    for (let u of n)
      a += u[bs].requiredVars, u.create && (u.targetIdx = 0, (i ??= []).push(u)), u.update && (u.targetIdx = 0, (s ??= []).push(u));
  if (r)
    for (let u = 0; u < r.length; u++) {
      let d = r[u];
      if (typeof d != "function")
        for (let p of d.bindings) {
          a += p[bs].requiredVars;
          let f = u + 1;
          p.create && (p.targetIdx = f, (i ??= []).push(p)), p.update && (p.targetIdx = f, (s ??= []).push(p));
        }
    }
  let c = [t];
  if (r)
    for (let u of r) {
      let d = typeof u == "function" ? u : u.type, p = pi(d);
      c.push(p);
    }
  return Ks(0, null, lg(i, s), 1, a, c, null, null, null, [o], null);
}
function lg(e12, t) {
  return !e12 && !t ? null : (n) => {
    if (n & 1 && e12)
      for (let r of e12)
        r.create();
    if (n & 2 && t)
      for (let r of t)
        r.update();
  };
}
function xl(e12) {
  let t = e12[bs].kind;
  return t === "input" || t === "twoWay";
}
var Hr = class extends zu {
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
    super(), this._rootLView = n, this._hasInputBindings = r, this._tNode = fr(n[m], $), this.location = $t(this._tNode, n), this.instance = Te(this._tNode.index, n)[N], this.hostView = this.changeDetectorRef = new Vt(n, void 0), this.componentType = t;
  }
  setInput(t, n) {
    this._hasInputBindings;
    let r = this._tNode;
    if (this.previousInputValues ??= /* @__PURE__ */ new Map(), this.previousInputValues.has(t) && Object.is(this.previousInputValues.get(t), n))
      return;
    let o = this._rootLView, i = ph(r, o[m], o, t, n);
    this.previousInputValues.set(t, n);
    let s = Te(r.index, o);
    sa(s, 1);
  }
  get injector() {
    return new ut(this._tNode, this._rootLView);
  }
  destroy() {
    this.hostView.destroy();
  }
  onDestroy(t) {
    this.hostView.onDestroy(t);
  }
};
function ug(e12, t, n) {
  let r = e12.projection = [];
  for (let o = 0; o < t.length; o++) {
    let i = n[o];
    r.push(i != null && i.length ? Array.from(i) : null);
  }
}
var ao = /* @__PURE__ */ (() => {
  class e12 {
    static __NG_ELEMENT_ID__ = dg;
  }
  return e12;
})();
function dg() {
  let e12 = ae();
  return Zu(e12, T());
}
var ws = class e4 extends ao {
  _lContainer;
  _hostTNode;
  _hostLView;
  constructor(t, n, r) {
    super(), this._lContainer = t, this._hostTNode = n, this._hostLView = r;
  }
  get element() {
    return $t(this._hostTNode, this._hostLView);
  }
  get injector() {
    return new ut(this._hostTNode, this._hostLView);
  }
  get parentInjector() {
    let t = Bs(this._hostTNode, this._hostLView);
    if (Ul(t)) {
      let n = kr(t, this._hostLView), r = Or(t), o = n[m].data[r + 8];
      return new ut(o, n);
    } else
      return new ut(null, this._hostLView);
  }
  clear() {
    for (; this.length > 0; )
      this.remove(this.length - 1);
  }
  get(t) {
    let n = Rl(this._lContainer);
    return n !== null && n[t] || null;
  }
  get length() {
    return this._lContainer.length - S;
  }
  createEmbeddedView(t, n, r) {
    let o, i;
    typeof r == "number" ? o = r : r != null && (o = r.index, i = r.injector);
    let s = Es(this._lContainer, t.ssrId), a = t.createEmbeddedViewImpl(n || {}, i, s);
    return this.insertImpl(a, o, fn(this._hostTNode, s)), a;
  }
  createComponent(t, n, r, o, i, s, a) {
    let c = t && !Nf(t), l;
    if (c)
      l = n;
    else {
      let R = n || {};
      l = R.index, r = R.injector, o = R.projectableNodes, i = R.environmentInjector || R.ngModuleRef, s = R.directives, a = R.bindings;
    }
    let u = c ? t : new mn(tt(t)), d = r || this.parentInjector;
    if (!i && u.ngModule == null) {
      let Y = (c ? d : this.parentInjector).get(J, null);
      Y && (i = Y);
    }
    let p = tt(u.componentType ?? {}), f = Es(this._lContainer, p?.id ?? null), h = f?.firstChild ?? null, x = u.create(d, o, h, i, s, a);
    return this.insertImpl(x.hostView, l, fn(this._hostTNode, f)), x;
  }
  insert(t, n) {
    return this.insertImpl(t, n, true);
  }
  insertImpl(t, n, r) {
    let o = t._lView;
    if (_c(o)) {
      let a = this.indexOf(t);
      if (a !== -1)
        this.detach(a);
      else {
        let c = o[k], l = new e4(c, c[te], c[k]);
        l.detach(l.indexOf(t));
      }
    }
    let i = this._adjustIndex(n), s = this._lContainer;
    return no(s, o, i, r), t.attachToViewContainerRef(), vi(Qi(s), i, t), t;
  }
  move(t, n) {
    return this.insert(t, n);
  }
  indexOf(t) {
    let n = Rl(this._lContainer);
    return n !== null ? n.indexOf(t) : -1;
  }
  remove(t) {
    let n = this._adjustIndex(t, -1), r = hn(this._lContainer, n);
    r && (en(Qi(this._lContainer), n), Xr(r[m], r));
  }
  detach(t) {
    let n = this._adjustIndex(t, -1), r = hn(this._lContainer, n);
    return r && en(Qi(this._lContainer), n) != null ? new Vt(r) : null;
  }
  _adjustIndex(t, n = 0) {
    return t ?? this.length + n;
  }
};
function Rl(e12) {
  return e12[rn];
}
function Qi(e12) {
  return e12[rn] || (e12[rn] = []);
}
function Zu(e12, t) {
  let n, r = t[e12.index];
  return se(r) ? n = r : (n = Hu(r, t, null, e12), t[e12.index] = n, Xs(t, n)), pg(n, t, e12, r), new ws(n, e12, t);
}
function fg(e12, t) {
  let n = e12[P], r = n.createComment(""), o = ge(t, e12), i = n.parentNode(o);
  return Fr(n, i, r, n.nextSibling(o), false), r;
}
var pg = mg;
var hg = () => false;
function gg(e12, t, n) {
  return hg(e12, t, n);
}
function mg(e12, t, n, r) {
  if (e12[Be])
    return;
  let o;
  n.type & 8 ? o = re(r) : o = fg(t, n), e12[Be] = o;
}
var Ts = class e5 {
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
var Ms = class e6 {
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
      ca(t, n).matches !== null && this.queries[n].setDirty();
  }
};
var _s = class {
  flags;
  read;
  predicate;
  constructor(t, n, r = null) {
    this.flags = n, this.read = r, typeof t == "string" ? this.predicate = wg(t) : this.predicate = t;
  }
};
var Ss = class e7 {
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
var Ns = class e8 {
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
        this.matchTNodeWithReadOption(t, n, yg(n, i)), this.matchTNodeWithReadOption(t, n, xr(n, t, i, false, false));
      }
    else
      r === gn ? n.type & 4 && this.matchTNodeWithReadOption(t, n, -1) : this.matchTNodeWithReadOption(t, n, xr(n, t, r, false, false));
  }
  matchTNodeWithReadOption(t, n, r) {
    if (r !== null) {
      let o = this.metadata.read;
      if (o !== null)
        if (o === En || o === ao || o === gn && n.type & 4)
          this.addMatch(n.index, -2);
        else {
          let i = xr(n, t, o, false, false);
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
function yg(e12, t) {
  let n = e12.localNames;
  if (n !== null) {
    for (let r = 0; r < n.length; r += 2)
      if (n[r] === t)
        return n[r + 1];
  }
  return null;
}
function vg(e12, t) {
  return e12.type & 11 ? $t(e12, t) : e12.type & 4 ? aa(e12, t) : null;
}
function Eg(e12, t, n, r) {
  return n === -1 ? vg(t, e12) : n === -2 ? Ig(e12, t, r) : dn(e12, e12[m], n, t);
}
function Ig(e12, t, n) {
  if (n === En)
    return $t(t, e12);
  if (n === gn)
    return aa(t, e12);
  if (n === ao)
    return Zu(t, e12);
}
function Qu(e12, t, n, r) {
  let o = t[he].queries[r];
  if (o.matches === null) {
    let i = e12.data, s = n.matches, a = [];
    for (let c = 0; s !== null && c < s.length; c += 2) {
      let l = s[c];
      if (l < 0)
        a.push(null);
      else {
        let u = i[l];
        a.push(Eg(t, u, s[c + 1], n.metadata.read));
      }
    }
    o.matches = a;
  }
  return o.matches;
}
function xs(e12, t, n, r) {
  let o = e12.queries.getByIndex(n), i = o.matches;
  if (i !== null) {
    let s = Qu(e12, t, o, n);
    for (let a = 0; a < i.length; a += 2) {
      let c = i[a];
      if (c > 0)
        r.push(s[a / 2]);
      else {
        let l = i[a + 1], u = t[-c];
        for (let d = S; d < u.length; d++) {
          let p = u[d];
          p[He] === p[k] && xs(p[m], p, l, r);
        }
        if (u[st] !== null) {
          let d = u[st];
          for (let p = 0; p < d.length; p++) {
            let f = d[p];
            xs(f[m], f, l, r);
          }
        }
      }
    }
  }
  return r;
}
function Dg(e12, t) {
  return e12[he].queries[t].queryList;
}
function bg(e12, t, n) {
  let r = new Lr((n & 4) === 4);
  return xc(e12, t, r, r.destroy), (t[he] ??= new Ms()).queries.push(new Ts(r)) - 1;
}
function Cg(e12, t, n) {
  let r = Q();
  return r.firstCreatePass && (Tg(r, new _s(e12, t, n), -1), (t & 2) === 2 && (r.staticViewQueries = true)), bg(r, T(), t);
}
function wg(e12) {
  return e12.split(",").map((t) => t.trim());
}
function Tg(e12, t, n) {
  e12.queries === null && (e12.queries = new Ss()), e12.queries.track(new Ns(t, n));
}
function ca(e12, t) {
  return e12.queries.getByIndex(t);
}
function Mg(e12, t) {
  let n = e12[m], r = ca(n, t);
  return r.crossesNgTemplate ? xs(n, e12, t, []) : Qu(n, e12, r, t);
}
var Vr = class {
};
var yn = class extends Vr {
  injector;
  componentFactoryResolver = new Cs(this);
  instance = null;
  constructor(t) {
    super();
    let n = new Je([...t.providers, { provide: Vr, useValue: this }, { provide: io, useValue: this.componentFactoryResolver }], t.parent || nn(), t.debugName, /* @__PURE__ */ new Set(["environment"]));
    this.injector = n, t.runEnvironmentInitializers && n.resolveInjectorInitializers();
  }
  destroy() {
    this.injector.destroy();
  }
  onDestroy(t) {
    this.injector.onDestroy(t);
  }
};
function Yu(e12, t, n = null) {
  return new yn({ providers: e12, parent: t, debugName: n, runEnvironmentInitializers: true }).injector;
}
var _g = (() => {
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
        let r = Di(false, n.type), o = r.length > 0 ? Yu([r], this._injector, "") : null;
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
    static \u0275prov = _({ token: e12, providedIn: "environment", factory: () => new e12(b(J)) });
  }
  return e12;
})();
function la(e12) {
  return jl(() => {
    let t = Rg(e12), n = O(A({}, t), { decls: e12.decls, vars: e12.vars, template: e12.template, consts: e12.consts || null, ngContentSelectors: e12.ngContentSelectors, onPush: e12.changeDetection === $s.OnPush, directiveDefs: null, pipeDefs: null, dependencies: t.standalone && e12.dependencies || null, getStandaloneInjector: t.standalone ? (o) => o.get(_g).getOrCreateStandaloneInjector(n) : null, getExternalStyles: null, signals: e12.signals ?? false, data: e12.data || {}, encapsulation: e12.encapsulation || ce.Emulated, styles: e12.styles || Pe, _: null, schemas: e12.schemas || null, tView: null, id: "" });
    t.standalone && gt("NgStandalone"), Ag(n);
    let r = e12.dependencies;
    return n.directiveDefs = Al(r, Sg), n.pipeDefs = Al(r, lc), n.id = Og(n), n;
  });
}
function Sg(e12) {
  return tt(e12) || pi(e12);
}
function Ng(e12, t) {
  if (e12 == null)
    return nt;
  let n = {};
  for (let r in e12)
    if (e12.hasOwnProperty(r)) {
      let o = e12[r], i, s, a, c;
      Array.isArray(o) ? (a = o[0], i = o[1], s = o[2] ?? i, c = o[3] || null) : (i = o, s = o, a = Jr.None, c = null), n[i] = [r, a, c], t[i] = s;
    }
  return n;
}
function xg(e12) {
  if (e12 == null)
    return nt;
  let t = {};
  for (let n in e12)
    e12.hasOwnProperty(n) && (t[e12[n]] = n);
  return t;
}
function Rg(e12) {
  let t = {};
  return { type: e12.type, providersResolver: null, viewProvidersResolver: null, factory: null, hostBindings: e12.hostBindings || null, hostVars: e12.hostVars || 0, hostAttrs: e12.hostAttrs || null, contentQueries: e12.contentQueries || null, declaredInputs: t, inputConfig: e12.inputs || nt, exportAs: e12.exportAs || null, standalone: e12.standalone ?? true, signals: e12.signals === true, selectors: e12.selectors || Pe, viewQuery: e12.viewQuery || null, features: e12.features || null, setInput: null, resolveHostDirectives: null, hostDirectives: null, controlDef: null, inputs: Ng(e12.inputs, t), outputs: xg(e12.outputs), debugInfo: null };
}
function Ag(e12) {
  e12.features?.forEach((t) => t(e12));
}
function Al(e12, t) {
  return e12 ? () => {
    let n = typeof e12 == "function" ? e12() : e12, r = [];
    for (let o of n) {
      let i = t(o);
      i !== null && r.push(i);
    }
    return r;
  } : null;
}
function Og(e12) {
  let t = 0, n = typeof e12.consts == "function" ? "" : e12.consts, r = [e12.selectors, e12.ngContentSelectors, e12.hostVars, e12.hostAttrs, n, e12.vars, e12.decls, e12.encapsulation, e12.standalone, e12.signals, e12.exportAs, JSON.stringify(e12.inputs), JSON.stringify(e12.outputs), Object.getOwnPropertyNames(e12.type.prototype), !!e12.contentQueries, !!e12.viewQuery];
  for (let i of r.join("|"))
    t = Math.imul(31, t) + i.charCodeAt(0) << 0;
  return t += 2147483648, "c" + t;
}
function kg(e12, t, n, r, o, i, s, a) {
  if (n.firstCreatePass) {
    e12.mergedAttrs = Wr(e12.mergedAttrs, e12.attrs);
    let u = e12.tView = Ks(2, e12, o, i, s, n.directiveRegistry, n.pipeRegistry, null, n.schemas, n.consts, null);
    n.queries !== null && (n.queries.template(n, e12), u.queries = n.queries.embeddedTView(e12));
  }
  a && (e12.flags |= a), kt(e12, false);
  let c = Pg(n, t, e12, r);
  Er() && ra(n, t, c, e12), Ht(c, t);
  let l = Hu(c, t, c, e12);
  t[r + $] = l, Xs(t, l), gg(l, e12, t);
}
function Br(e12, t, n, r, o, i, s, a, c, l, u) {
  let d = n + $, p;
  if (t.firstCreatePass) {
    if (p = ro(t, d, 4, s || null, a || null), l != null) {
      let f = me(t.consts, l);
      p.localNames = [];
      for (let h = 0; h < f.length; h += 2)
        p.localNames.push(f[h], -1);
    }
  } else
    p = t.data[d];
  return kg(p, e12, t, n, r, o, i, c), l != null && Nu(e12, p, u), p;
}
var Pg = Lg;
function Lg(e12, t, n, r) {
  return Ir(true), t[P].createComment("");
}
var ua = new D("");
function da(e12) {
  return !!e12 && typeof e12.then == "function";
}
function Ku(e12) {
  return !!e12 && typeof e12.subscribe == "function";
}
var Ju = new D("");
var fa = (() => {
  class e12 {
    resolve;
    reject;
    initialized = false;
    done = false;
    donePromise = new Promise((n, r) => {
      this.resolve = n, this.reject = r;
    });
    appInits = E(Ju, { optional: true }) ?? [];
    injector = E(fe);
    constructor() {
    }
    runInitializers() {
      if (this.initialized)
        return;
      let n = [];
      for (let o of this.appInits) {
        let i = lr(this.injector, o);
        if (da(i))
          n.push(i);
        else if (Ku(i)) {
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
var Xu = new D("");
function ed() {
  Po(() => {
    let e12 = "";
    throw new v(600, e12);
  });
}
function td(e12) {
  return e12.isBoundToModule;
}
var Fg = 10;
var Cn = (() => {
  class e12 {
    _runningTick = false;
    _destroyed = false;
    _destroyListeners = [];
    _views = [];
    internalErrorHandler = E(lt);
    afterRenderManager = E(Cu);
    zonelessEnabled = E(an);
    rootEffectScheduler = E(br);
    dirtyFlags = 0;
    tracingSnapshot = null;
    allTestViews = /* @__PURE__ */ new Set();
    autoDetectTestViews = /* @__PURE__ */ new Set();
    includeAllTestViews = false;
    afterTick = new Ee();
    get allViews() {
      return [...(this.includeAllTestViews ? this.allTestViews : this.autoDetectTestViews).keys(), ...this._views];
    }
    get destroyed() {
      return this._destroyed;
    }
    componentTypes = [];
    components = [];
    internalPendingTask = E(Lt);
    get isStable() {
      return this.internalPendingTask.hasPendingTasksObservable.pipe(qo((n) => !n));
    }
    constructor() {
      E(Ut, { optional: true });
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
    _injector = E(J);
    _rendererFactory = null;
    get injector() {
      return this._injector;
    }
    bootstrap(n, r) {
      return this.bootstrapImpl(n, r);
    }
    bootstrapImpl(n, r, o = fe.NULL) {
      return this._injector.get(X).run(() => {
        M(C.BootstrapComponentStart);
        let s = n instanceof oo;
        if (!this._injector.get(fa).done) {
          let h = "";
          throw new v(405, h);
        }
        let c;
        s ? c = n : c = this._injector.get(io).resolveComponentFactory(n), this.componentTypes.push(c.componentType);
        let l = td(c) ? void 0 : this._injector.get(Vr), u = r || c.selector, d = c.create(o, [], u, l), p = d.location.nativeElement, f = d.injector.get(ua, null);
        return f?.registerApplication(p), d.onDestroy(() => {
          this.detachView(d.hostView), un(this.components, d), f?.unregisterApplication(p);
        }), this._loadComponent(d), M(C.BootstrapComponentEnd, d), d;
      });
    }
    tick() {
      this.zonelessEnabled || (this.dirtyFlags |= 1), this._tick();
    }
    _tick() {
      M(C.ChangeDetectionStart), this.tracingSnapshot !== null ? this.tracingSnapshot.run(ta.CHANGE_DETECTION, this.tickImpl) : this.tickImpl();
    }
    tickImpl = () => {
      if (this._runningTick)
        throw M(C.ChangeDetectionEnd), new v(101, false);
      let n = g(null);
      try {
        this._runningTick = true, this.synchronize();
      } finally {
        this._runningTick = false, this.tracingSnapshot?.dispose(), this.tracingSnapshot = null, g(n), this.afterTick.next(), M(C.ChangeDetectionEnd);
      }
    };
    synchronize() {
      this._rendererFactory === null && !this._injector.destroyed && (this._rendererFactory = this._injector.get(pt, null, { optional: true }));
      let n = 0;
      for (; this.dirtyFlags !== 0 && n++ < Fg; ) {
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
          if (!r && !on(o))
            continue;
          let i = r && !this.zonelessEnabled ? 0 : 1;
          Pu(o, i), n = true;
        }
        if (this.dirtyFlags &= -5, this.syncDirtyFlagsWithViews(), this.dirtyFlags & 23)
          return;
      }
      n || (this._rendererFactory?.begin?.(), this._rendererFactory?.end?.()), this.dirtyFlags & 8 && (this.dirtyFlags &= -9, this.afterRenderManager.execute()), this.syncDirtyFlagsWithViews();
    }
    syncDirtyFlagsWithViews() {
      if (this.allViews.some(({ _lView: n }) => on(n))) {
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
      un(this._views, r), r.detachFromAppRef();
    }
    _loadComponent(n) {
      this.attachView(n.hostView);
      try {
        this.tick();
      } catch (o) {
        this.internalErrorHandler(o);
      }
      this.components.push(n), this._injector.get(Xu, []).forEach((o) => o(n));
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
      return this._destroyListeners.push(n), () => un(this._destroyListeners, n);
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
function un(e12, t) {
  let n = e12.indexOf(t);
  n > -1 && e12.splice(n, 1);
}
var Rs = class {
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
function Yi(e12, t, n, r, o) {
  return e12 === n && Object.is(t, r) ? 1 : Object.is(o(e12, t), o(n, r)) ? -1 : 0;
}
function jg(e12, t, n, r) {
  let o, i, s = 0, a = e12.length - 1, c = void 0;
  if (Array.isArray(t)) {
    g(r);
    let l = t.length - 1;
    for (g(null); s <= a && s <= l; ) {
      let u = e12.at(s), d = t[s], p = Yi(s, u, s, d, n);
      if (p !== 0) {
        p < 0 && e12.updateValue(s, d), s++;
        continue;
      }
      let f = e12.at(a), h = t[l], x = Yi(a, f, l, h, n);
      if (x !== 0) {
        x < 0 && e12.updateValue(a, h), a--, l--;
        continue;
      }
      let R = n(s, u), Y = n(a, f), Wt = n(s, d);
      if (Object.is(Wt, Y)) {
        let Co = n(l, h);
        Object.is(Co, R) ? (e12.swap(s, a), e12.updateValue(a, h), l--, a--) : e12.move(a, s), e12.updateValue(s, d), s++;
        continue;
      }
      if (o ??= new $r(), i ??= kl(e12, s, a, n), As(e12, o, s, Wt))
        e12.updateValue(s, d), s++, a++;
      else if (i.has(Wt))
        o.set(R, e12.detach(s)), a--;
      else {
        let Co = e12.create(s, t[s]);
        e12.attach(s, Co), s++, a++;
      }
    }
    for (; s <= l; )
      Ol(e12, o, n, s, t[s]), s++;
  } else if (t != null) {
    g(r);
    let l = t[Symbol.iterator]();
    g(null);
    let u = l.next();
    for (; !u.done && s <= a; ) {
      let d = e12.at(s), p = u.value, f = Yi(s, d, s, p, n);
      if (f !== 0)
        f < 0 && e12.updateValue(s, p), s++, u = l.next();
      else {
        o ??= new $r(), i ??= kl(e12, s, a, n);
        let h = n(s, p);
        if (As(e12, o, s, h))
          e12.updateValue(s, p), s++, a++, u = l.next();
        else if (!i.has(h))
          e12.attach(s, e12.create(s, p)), s++, a++, u = l.next();
        else {
          let x = n(s, d);
          o.set(x, e12.detach(s)), a--;
        }
      }
    }
    for (; !u.done; )
      Ol(e12, o, n, e12.length, u.value), u = l.next();
  }
  for (; s <= a; )
    e12.destroy(e12.detach(a--));
  o?.forEach((l) => {
    e12.destroy(l);
  });
}
function As(e12, t, n, r) {
  return t !== void 0 && t.has(r) ? (e12.attach(n, t.get(r)), t.delete(r), true) : false;
}
function Ol(e12, t, n, r, o) {
  if (As(e12, t, r, n(r, o)))
    e12.updateValue(r, o);
  else {
    let i = e12.create(r, o);
    e12.attach(r, i);
  }
}
function kl(e12, t, n, r) {
  let o = /* @__PURE__ */ new Set();
  for (let i = t; i <= n; i++)
    o.add(r(i, e12.at(i)));
  return o;
}
var $r = class {
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
function wn(e12, t, n, r, o, i, s, a) {
  gt("NgControlFlow");
  let c = T(), l = Q(), u = me(l.consts, i);
  return Br(c, l, e12, t, n, r, o, u, 256, s, a), pa;
}
function pa(e12, t, n, r, o, i, s, a) {
  gt("NgControlFlow");
  let c = T(), l = Q(), u = me(l.consts, i);
  return Br(c, l, e12, t, n, r, o, u, 512, s, a), pa;
}
function Tn(e12, t) {
  gt("NgControlFlow");
  let n = T(), r = sn(), o = n[r] !== Ae ? n[r] : -1, i = o !== -1 ? Ur(n, $ + o) : void 0, s = 0;
  if (bn(n, r, e12)) {
    let a = g(null);
    try {
      if (i !== void 0 && Bu(i, s), e12 !== -1) {
        let c = $ + e12, l = Ur(n, c), u = Ls(n[m], c), d = Uu(l, u, n), p = to(n, u, t, { dehydratedView: d });
        no(l, p, s, fn(u, d));
      }
    } finally {
      g(a);
    }
  } else if (i !== void 0) {
    let a = Vu(i, s);
    a !== void 0 && (a[N] = t);
  }
}
var Os = class {
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
function co(e12, t) {
  return t;
}
var ks = class {
  hasEmptyBlock;
  trackByFn;
  liveCollection;
  constructor(t, n, r) {
    this.hasEmptyBlock = t, this.trackByFn = n, this.liveCollection = r;
  }
};
function lo(e12, t, n, r, o, i, s, a, c, l, u, d, p) {
  gt("NgControlFlow");
  let f = T(), h = Q(), x = c !== void 0, R = T(), Y = a ? s.bind(R[ne][N]) : s, Wt = new ks(x, Y);
  R[$ + e12] = Wt, Br(f, h, e12 + 1, t, n, r, o, me(h.consts, i), 256), x && Br(f, h, e12 + 2, c, l, u, d, me(h.consts, p), 512);
}
var Ps = class extends Rs {
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
    let r = n[St];
    this.needsIndexUpdate ||= t !== this.length, no(this.lContainer, n, t, fn(this.templateTNode, r)), Hg(this.lContainer, t);
  }
  detach(t) {
    return this.needsIndexUpdate ||= t !== this.length - 1, Vg(this.lContainer, t), Bg(this.lContainer, t);
  }
  create(t, n) {
    let r = Es(this.lContainer, this.templateTNode.tView.ssrId);
    return to(this.hostLView, this.templateTNode, new Os(this.lContainer, n, t), { dehydratedView: r });
  }
  destroy(t) {
    Xr(t[m], t);
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
    return $g(this.lContainer, t);
  }
};
function uo(e12) {
  let t = g(null), n = Ue();
  try {
    let r = T(), o = r[m], i = r[n], s = n + 1, a = Ur(r, s);
    if (i.liveCollection === void 0) {
      let l = Ls(o, s);
      i.liveCollection = new Ps(a, r, l);
    } else
      i.liveCollection.reset();
    let c = i.liveCollection;
    if (jg(c, e12, i.trackByFn, t), c.updateIndexes(), i.hasEmptyBlock) {
      let l = sn(), u = c.length === 0;
      if (bn(r, l, u)) {
        let d = n + 2, p = Ur(r, d);
        if (u) {
          let f = Ls(o, d), h = Uu(p, f, r), x = to(r, f, void 0, { dehydratedView: h });
          no(p, x, 0, fn(f, h));
        } else
          o.firstUpdatePass && kh(p), Bu(p, 0);
      }
    }
  } finally {
    g(t);
  }
}
function Ur(e12, t) {
  return e12[t];
}
function Hg(e12, t) {
  if (e12.length <= S)
    return;
  let n = S + t, r = e12[n], o = r ? r[Ve] : void 0;
  if (r && o && o.detachedLeaveAnimationFns && o.detachedLeaveAnimationFns.length > 0) {
    let i = r[Ce];
    Hp(i, o), ft.delete(r[we]), o.detachedLeaveAnimationFns = void 0;
  }
}
function Vg(e12, t) {
  if (e12.length <= S)
    return;
  let n = S + t, r = e12[n], o = r ? r[Ve] : void 0;
  o && o.leave && o.leave.size > 0 && (o.detachedLeaveAnimationFns = []);
}
function Bg(e12, t) {
  return hn(e12, t);
}
function $g(e12, t) {
  return Vu(e12, t);
}
function Ls(e12, t) {
  return fr(e12, t);
}
function L(e12, t, n, r) {
  let o = T(), i = o[m], s = e12 + $, a = i.firstCreatePass ? Yh(s, i, 2, t, n, r) : i.data[s];
  return uh(a, o, e12, t, Ug), r != null && Nu(o, a), L;
}
function F() {
  let e12 = ae(), t = dh(e12);
  return Pc(t) && Lc(), Oc(), F;
}
function fo(e12, t, n, r) {
  return L(e12, t, n, r), F(), fo;
}
var Ug = (e12, t, n, r, o) => (Ir(true), mu(t[P], r, Yc()));
function po() {
  return T();
}
function le(e12, t, n) {
  let r = T(), o = sn();
  if (bn(r, o, t)) {
    let i = Q(), s = Qc();
    ih(s, r, e12, t, r[P], n);
  }
  return le;
}
var Mn = "en-US";
var zg = Mn;
function nd(e12) {
  typeof e12 == "string" && (zg = e12.toLowerCase().replace(/_/g, "-"));
}
function Oe(e12, t, n) {
  let r = T(), o = Q(), i = ae();
  return (i.type & 3 || n) && Jh(i, o, r, n, r[P], e12, t, Kh(i, r, t)), Oe;
}
function ue(e12 = 1) {
  return Zc(e12);
}
function ho(e12, t, n) {
  return Cg(e12, t, n), ho;
}
function ha(e12) {
  let t = T(), n = Q(), r = ji();
  mr(r + 1);
  let o = ca(n, r);
  if (e12.dirty && Mc(t) === ((o.metadata.flags & 2) === 2)) {
    if (o.matches === null)
      e12.reset([]);
    else {
      let i = Mg(t, r);
      e12.reset(i, Zf), e12.notifyOnChanges();
    }
    return true;
  }
  return false;
}
function ga() {
  return Dg(T(), ji());
}
function _r(e12, t) {
  return e12 << 17 | t << 2;
}
function ht(e12) {
  return e12 >> 17 & 32767;
}
function Wg(e12) {
  return (e12 & 2) == 2;
}
function Gg(e12, t) {
  return e12 & 131071 | t << 17;
}
function Fs(e12) {
  return e12 | 2;
}
function Bt(e12) {
  return (e12 & 131068) >> 2;
}
function Ki(e12, t) {
  return e12 & -131069 | t << 2;
}
function qg(e12) {
  return (e12 & 1) === 1;
}
function js(e12) {
  return e12 | 1;
}
function Zg(e12, t, n, r, o, i) {
  let s = i ? t.classBindings : t.styleBindings, a = ht(s), c = Bt(s);
  e12[r] = n;
  let l = false, u;
  if (Array.isArray(n)) {
    let d = n;
    u = d[1], (u === null || Mt(d, u) > 0) && (l = true);
  } else
    u = n;
  if (o)
    if (c !== 0) {
      let p = ht(e12[a + 1]);
      e12[r + 1] = _r(p, a), p !== 0 && (e12[p + 1] = Ki(e12[p + 1], r)), e12[a + 1] = Gg(e12[a + 1], r);
    } else
      e12[r + 1] = _r(a, 0), a !== 0 && (e12[a + 1] = Ki(e12[a + 1], r)), a = r;
  else
    e12[r + 1] = _r(c, 0), a === 0 ? a = r : e12[c + 1] = Ki(e12[c + 1], r), c = r;
  l && (e12[r + 1] = Fs(e12[r + 1])), Pl(e12, u, r, true), Pl(e12, u, r, false), Qg(t, u, e12, r, i), s = _r(a, c), i ? t.classBindings = s : t.styleBindings = s;
}
function Qg(e12, t, n, r, o) {
  let i = o ? e12.residualClasses : e12.residualStyles;
  i != null && typeof t == "string" && Mt(i, t) >= 0 && (n[r + 1] = js(n[r + 1]));
}
function Pl(e12, t, n, r) {
  let o = e12[n + 1], i = t === null, s = r ? ht(o) : Bt(o), a = false;
  for (; s !== 0 && (a === false || i); ) {
    let c = e12[s], l = e12[s + 1];
    Yg(c, t) && (a = true, e12[s + 1] = r ? js(l) : Fs(l)), s = r ? ht(l) : Bt(l);
  }
  a && (e12[n + 1] = r ? Fs(o) : js(o));
}
function Yg(e12, t) {
  return e12 === null || t == null || (Array.isArray(e12) ? e12[1] : e12) === t ? true : Array.isArray(e12) && typeof t == "string" ? Mt(e12, t) >= 0 : false;
}
function go(e12, t) {
  return Kg(e12, t, null, true), go;
}
function Kg(e12, t, n, r) {
  let o = T(), i = Q(), s = Vc(2);
  if (i.firstUpdatePass && Xg(i, e12, s, r), t !== Ae && bn(o, s, t)) {
    let a = i.data[Ue()];
    om(i, a, o, o[P], e12, o[s + 1] = im(t, n), r, s);
  }
}
function Jg(e12, t) {
  return t >= e12.expandoStartIndex;
}
function Xg(e12, t, n, r) {
  let o = e12.data;
  if (o[n + 1] === null) {
    let i = o[Ue()], s = Jg(e12, n);
    sm(i, r) && t === null && !s && (t = false), t = em(o, i, t, r), Zg(o, i, t, n, s, r);
  }
}
function em(e12, t, n, r) {
  let o = zc(e12), i = r ? t.residualClasses : t.residualStyles;
  if (o === null)
    (r ? t.classBindings : t.styleBindings) === 0 && (n = Ji(null, e12, t, n, r), n = vn(n, t.attrs, r), i = null);
  else {
    let s = t.directiveStylingLast;
    if (s === -1 || e12[s] !== o)
      if (n = Ji(o, e12, t, n, r), i === null) {
        let c = tm(e12, t, r);
        c !== void 0 && Array.isArray(c) && (c = Ji(null, e12, t, c[1], r), c = vn(c, t.attrs, r), nm(e12, t, r, c));
      } else
        i = rm(e12, t, r);
  }
  return i !== void 0 && (r ? t.residualClasses = i : t.residualStyles = i), n;
}
function tm(e12, t, n) {
  let r = n ? t.classBindings : t.styleBindings;
  if (Bt(r) !== 0)
    return e12[ht(r)];
}
function nm(e12, t, n, r) {
  let o = n ? t.classBindings : t.styleBindings;
  e12[ht(o)] = r;
}
function rm(e12, t, n) {
  let r, o = t.directiveEnd;
  for (let i = 1 + t.directiveStylingLast; i < o; i++) {
    let s = e12[i].hostAttrs;
    r = vn(r, s, n);
  }
  return vn(r, t.attrs, n);
}
function Ji(e12, t, n, r, o) {
  let i = null, s = n.directiveEnd, a = n.directiveStylingLast;
  for (a === -1 ? a = n.directiveStart : a++; a < s && (i = t[a], r = vn(r, i.hostAttrs, o), i !== e12); )
    a++;
  return e12 !== null && (n.directiveStylingLast = a), r;
}
function vn(e12, t, n) {
  let r = n ? 1 : 2, o = -1;
  if (t !== null)
    for (let i = 0; i < t.length; i++) {
      let s = t[i];
      typeof s == "number" ? o = s : o === r && (Array.isArray(e12) || (e12 = e12 === void 0 ? [] : ["", e12]), mc(e12, s, n ? true : t[++i]));
    }
  return e12 === void 0 ? null : e12;
}
function om(e12, t, n, r, o, i, s, a) {
  if (!(t.type & 3))
    return;
  let c = e12.data, l = c[a + 1], u = qg(l) ? Ll(c, t, n, o, Bt(l), s) : void 0;
  if (!zr(u)) {
    zr(i) || Wg(l) && (i = Ll(c, null, n, o, a, s));
    let d = Ni(Ue(), n);
    eh(r, s, d, o, i);
  }
}
function Ll(e12, t, n, r, o, i) {
  let s = t === null, a;
  for (; o > 0; ) {
    let c = e12[o], l = Array.isArray(c), u = l ? c[1] : c, d = u === null, p = n[o + 1];
    p === Ae && (p = d ? Pe : void 0);
    let f = d ? cr(p, r) : u === r ? p : void 0;
    if (l && !zr(f) && (f = cr(c, r)), zr(f) && (a = f, s))
      return a;
    let h = e12[o + 1];
    o = s ? ht(h) : Bt(h);
  }
  if (t !== null) {
    let c = i ? t.residualClasses : t.residualStyles;
    c != null && (a = cr(c, r));
  }
  return a;
}
function zr(e12) {
  return e12 !== void 0;
}
function im(e12, t) {
  return e12 == null || e12 === "" || (typeof t == "string" ? e12 = e12 + t : typeof e12 == "object" && (e12 = nr(xe(e12)))), e12;
}
function sm(e12, t) {
  return (e12.flags & (t ? 8 : 16)) !== 0;
}
function G(e12, t = "") {
  let n = T(), r = Q(), o = e12 + $, i = r.firstCreatePass ? ro(r, o, 1, t, null) : r.data[o], s = am(r, n, i, t);
  n[o] = s, Er() && ra(r, n, s, i), kt(i, false);
}
var am = (e12, t, n, r) => (Ir(true), Cp(t[P], r));
function cm(e12, t, n, r = "") {
  return bn(e12, sn(), n) ? t + gi(n) + r : Ae;
}
function ke(e12) {
  return ma("", e12), ke;
}
function ma(e12, t, n) {
  let r = T(), o = cm(r, e12, t, n);
  return o !== Ae && lm(r, Ue(), o), ma;
}
function lm(e12, t, n) {
  let r = Ni(t, e12);
  wp(e12[P], r, n);
}
function Fl(e12, t, n) {
  let r = Q();
  r.firstCreatePass && rd(t, r.data, r.blueprint, at(e12), n);
}
function rd(e12, t, n, r, o) {
  if (e12 = B(e12), Array.isArray(e12))
    for (let i = 0; i < e12.length; i++)
      rd(e12[i], t, n, r, o);
  else {
    let i = Q(), s = T(), a = ae(), c = Ke(e12) ? e12 : B(e12.provide), l = Ci(e12), u = a.providerIndexes & 1048575, d = a.directiveStart, p = a.providerIndexes >> 20;
    if (Ke(e12) || !e12.multi) {
      let f = new dt(l, o, so, null), h = es(c, t, o ? u : u + p, d);
      h === -1 ? (ns(Pr(a, s), i, c), Xi(i, e12, t.length), t.push(c), a.directiveStart++, a.directiveEnd++, o && (a.providerIndexes += 1048576), n.push(f), s.push(f)) : (n[h] = f, s[h] = f);
    } else {
      let f = es(c, t, u + p, d), h = es(c, t, u, u + p), x = f >= 0 && n[f], R = h >= 0 && n[h];
      if (o && !R || !o && !x) {
        ns(Pr(a, s), i, c);
        let Y = fm(o ? dm : um, n.length, o, r, l, e12);
        !o && R && (n[h].providerFactory = Y), Xi(i, e12, t.length, 0), t.push(c), a.directiveStart++, a.directiveEnd++, o && (a.providerIndexes += 1048576), n.push(Y), s.push(Y);
      } else {
        let Y = od(n[o ? h : f], l, !o && r);
        Xi(i, e12, f > -1 ? f : h, Y);
      }
      !o && r && R && n[h].componentProviders++;
    }
  }
}
function Xi(e12, t, n, r) {
  let o = Ke(t), i = Dc(t);
  if (o || i) {
    let c = (i ? B(t.useClass) : t).prototype.ngOnDestroy;
    if (c) {
      let l = e12.destroyHooks || (e12.destroyHooks = []);
      if (!o && t.multi) {
        let u = l.indexOf(n);
        u === -1 ? l.push(n, [r, c]) : l[u + 1].push(r, c);
      } else
        l.push(n, c);
    }
  }
}
function od(e12, t, n) {
  return n && e12.componentProviders++, e12.multi.push(t) - 1;
}
function es(e12, t, n, r) {
  for (let o = n; o < r; o++)
    if (t[o] === e12)
      return o;
  return -1;
}
function um(e12, t, n, r, o) {
  return Hs(this.multi, []);
}
function dm(e12, t, n, r, o) {
  let i = this.multi, s;
  if (this.providerFactory) {
    let a = this.providerFactory.componentProviders, c = dn(r, r[m], this.providerFactory.index, o);
    s = c.slice(0, a), Hs(i, s);
    for (let l = a; l < c.length; l++)
      s.push(c[l]);
  } else
    s = [], Hs(i, s);
  return s;
}
function Hs(e12, t) {
  for (let n = 0; n < e12.length; n++) {
    let r = e12[n];
    t.push(r());
  }
  return t;
}
function fm(e12, t, n, r, o, i) {
  let s = new dt(e12, n, so, null);
  return s.multi = [], s.index = t, s.componentProviders = 0, od(s, o, r && !n), s;
}
function ya(e12, t) {
  return (n) => {
    n.providersResolver = (r, o) => Fl(r, o ? o(e12) : e12, false), t && (n.viewProvidersResolver = (r, o) => Fl(r, o ? o(t) : t, true));
  };
}
var id = (() => {
  class e12 {
    applicationErrorHandler = E(lt);
    appRef = E(Cn);
    taskService = E(Lt);
    ngZone = E(X);
    zonelessEnabled = E(an);
    tracing = E(Ut, { optional: true });
    zoneIsDefined = typeof Zone < "u" && !!Zone.root.run;
    schedulerTickApplyArgs = [{ data: { __scheduler_tick__: true } }];
    subscriptions = new U();
    angularZoneId = this.zoneIsDefined ? this.ngZone._inner?.get(Jt) : null;
    scheduleInRootZone = !this.zonelessEnabled && this.zoneIsDefined && (E(Wi, { optional: true }) ?? false);
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
      let r = this.useMicrotaskScheduler ? tl : Bi;
      this.pendingRenderTaskId = this.taskService.add(), this.scheduleInRootZone ? this.cancelScheduledCallback = Zone.root.run(() => r(() => this.tick())) : this.cancelScheduledCallback = this.ngZone.runOutsideAngular(() => r(() => this.tick()));
    }
    shouldScheduleTick() {
      return !(this.appRef.destroyed || this.pendingRenderTaskId !== null || this.runningTick || this.appRef._runningTick || !this.zonelessEnabled && this.zoneIsDefined && Zone.current.get(Jt + this.angularZoneId));
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
function va() {
  return gt("NgZoneless"), _t([...Ea(), []]);
}
function Ea() {
  return [{ provide: Xe, useExisting: id }, { provide: X, useClass: Xt }, { provide: an, useValue: true }];
}
function pm() {
  return typeof $localize < "u" && $localize.locale || Mn;
}
var Ia = new D("", { factory: () => E(Ia, { optional: true, skipSelf: true }) || pm() });
function Ge(e12, t) {
  return Bn(e12, t?.equal);
}
var Da = new D("");
var Cm = new D("");
function _n(e12) {
  return !e12.moduleRef;
}
function wm(e12) {
  let t = _n(e12) ? e12.r3Injector : e12.moduleRef.injector, n = t.get(X);
  return n.run(() => {
    _n(e12) ? e12.r3Injector.resolveInjectorInitializers() : e12.moduleRef.resolveInjectorInitializers();
    let r = t.get(lt), o;
    if (n.runOutsideAngular(() => {
      o = n.onError.subscribe({ next: r });
    }), _n(e12)) {
      let i = () => t.destroy(), s = e12.platformInjector.get(Da);
      s.add(i), t.onDestroy(() => {
        o.unsubscribe(), s.delete(i);
      });
    } else {
      let i = () => e12.moduleRef.destroy(), s = e12.platformInjector.get(Da);
      s.add(i), e12.moduleRef.onDestroy(() => {
        un(e12.allPlatformModules, e12.moduleRef), o.unsubscribe(), s.delete(i);
      });
    }
    return Mm(r, n, () => {
      let i = t.get(Lt), s = i.add(), a = t.get(fa);
      return a.runInitializers(), a.donePromise.then(() => {
        let c = t.get(Ia, Mn);
        if (nd(c || Mn), !t.get(Cm, true))
          return _n(e12) ? t.get(Cn) : (e12.allPlatformModules.push(e12.moduleRef), e12.moduleRef);
        if (_n(e12)) {
          let u = t.get(Cn);
          return e12.rootComponent !== void 0 && u.bootstrap(e12.rootComponent), u;
        } else
          return Tm?.(e12.moduleRef, e12.allPlatformModules), e12.moduleRef;
      }).finally(() => {
        i.remove(s);
      });
    });
  });
}
var Tm;
function Mm(e12, t, n) {
  try {
    let r = n();
    return da(r) ? r.catch((o) => {
      throw t.runOutsideAngular(() => e12(o)), o;
    }) : r;
  } catch (r) {
    throw t.runOutsideAngular(() => e12(r)), r;
  }
}
var mo = null;
function _m(e12 = [], t) {
  return fe.create({ name: t, providers: [{ provide: tn, useValue: "platform" }, { provide: Da, useValue: /* @__PURE__ */ new Set([() => mo = null]) }, ...e12] });
}
function Sm(e12 = []) {
  if (mo)
    return mo;
  let t = _m(e12);
  return mo = t, ed(), Nm(t), t;
}
function Nm(e12) {
  let t = e12.get(qr, null);
  lr(e12, () => {
    t?.forEach((n) => n());
  });
}
var xm = 1e4;
var e_ = xm - 1e3;
function ad(e12) {
  let { rootComponent: t, appProviders: n, platformProviders: r, platformRef: o } = e12;
  M(C.BootstrapApplicationStart);
  try {
    let i = o?.injector ?? Sm(r), s = [Ea(), rl, ...n || []], a = new yn({ providers: s, parent: i, debugName: "", runEnvironmentInitializers: false });
    return wm({ r3Injector: a.injector, platformInjector: i, rootComponent: t });
  } catch (i) {
    return Promise.reject(i);
  } finally {
    M(C.BootstrapApplicationEnd);
  }
}
var cd = null;
function zt() {
  return cd;
}
function ba(e12) {
  cd ??= e12;
}
var Nn = class {
};
function Ca(e12, t) {
  t = encodeURIComponent(t);
  for (let n of e12.split(";")) {
    let r = n.indexOf("="), [o, i] = r == -1 ? [n, ""] : [n.slice(0, r), n.slice(r + 1)];
    if (o.trim() === t)
      return decodeURIComponent(i);
  }
  return null;
}
var xn = class {
};
var ld = "browser";
var Rn = class {
  _doc;
  constructor(t) {
    this._doc = t;
  }
  manager;
};
var yo = (() => {
  class e12 extends Rn {
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
      return new (r || e12)(b(W));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var Io = new D("");
var _a = (() => {
  class e12 {
    _zone;
    _plugins;
    _eventNameToPlugin = /* @__PURE__ */ new Map();
    constructor(n, r) {
      this._zone = r, n.forEach((s) => {
        s.manager = this;
      });
      let o = n.filter((s) => !(s instanceof yo));
      this._plugins = o.slice().reverse();
      let i = n.find((s) => s instanceof yo);
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
      return new (r || e12)(b(Io), b(X));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var wa = "ng-app-id";
function ud(e12) {
  for (let t of e12)
    t.remove();
}
function dd(e12, t) {
  let n = t.createElement("style");
  return n.textContent = e12, n;
}
function Rm(e12, t, n, r) {
  let o = e12.head?.querySelectorAll(`style[${wa}="${t}"],link[${wa}="${t}"]`);
  if (o)
    for (let i of o)
      i.removeAttribute(wa), i instanceof HTMLLinkElement ? r.set(i.href.slice(i.href.lastIndexOf("/") + 1), { usage: 0, elements: [i] }) : i.textContent && n.set(i.textContent, { usage: 0, elements: [i] });
}
function Ma(e12, t) {
  let n = t.createElement("link");
  return n.setAttribute("rel", "stylesheet"), n.setAttribute("href", e12), n;
}
var Sa = (() => {
  class e12 {
    doc;
    appId;
    nonce;
    inline = /* @__PURE__ */ new Map();
    external = /* @__PURE__ */ new Map();
    hosts = /* @__PURE__ */ new Set();
    constructor(n, r, o, i = {}) {
      this.doc = n, this.appId = r, this.nonce = o, Rm(n, r, this.inline, this.external), this.hosts.add(n.head);
    }
    addStyles(n, r) {
      for (let o of n)
        this.addUsage(o, this.inline, dd);
      r?.forEach((o) => this.addUsage(o, this.external, Ma));
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
      o && (o.usage--, o.usage <= 0 && (ud(o.elements), r.delete(n)));
    }
    ngOnDestroy() {
      for (let [, { elements: n }] of [...this.inline, ...this.external])
        ud(n);
      this.hosts.clear();
    }
    addHost(n) {
      this.hosts.add(n);
      for (let [r, { elements: o }] of this.inline)
        o.push(this.addElement(n, dd(r, this.doc)));
      for (let [r, { elements: o }] of this.external)
        o.push(this.addElement(n, Ma(r, this.doc)));
    }
    removeHost(n) {
      this.hosts.delete(n);
    }
    addElement(n, r) {
      return this.nonce && r.setAttribute("nonce", this.nonce), n.appendChild(r);
    }
    static \u0275fac = function(r) {
      return new (r || e12)(b(W), b(Gr), b(Zr, 8), b(In));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var Ta = { svg: "http://www.w3.org/2000/svg", xhtml: "http://www.w3.org/1999/xhtml", xlink: "http://www.w3.org/1999/xlink", xml: "http://www.w3.org/XML/1998/namespace", xmlns: "http://www.w3.org/2000/xmlns/", math: "http://www.w3.org/1998/Math/MathML" };
var Na = /%COMP%/g;
var pd = "%COMP%";
var Am = `_nghost-${pd}`;
var Om = `_ngcontent-${pd}`;
var km = true;
var Pm = new D("", { factory: () => km });
function Lm(e12) {
  return Om.replace(Na, e12);
}
function Fm(e12) {
  return Am.replace(Na, e12);
}
function hd(e12, t) {
  return t.map((n) => n.replace(Na, e12));
}
var xa = (() => {
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
      this.eventManager = n, this.sharedStylesHost = r, this.appId = o, this.removeStylesOnCompDestroy = i, this.doc = s, this.ngZone = a, this.nonce = c, this.tracingService = l, this.defaultRenderer = new An(n, s, a, this.tracingService);
    }
    createRenderer(n, r) {
      if (!n || !r)
        return this.defaultRenderer;
      let o = this.getOrCreateRenderer(n, r);
      return o instanceof Eo ? o.applyToHost(n) : o instanceof On && o.applyStyles(), o;
    }
    getOrCreateRenderer(n, r) {
      let o = this.rendererByCompId, i = o.get(r.id);
      if (!i) {
        let s = this.doc, a = this.ngZone, c = this.eventManager, l = this.sharedStylesHost, u = this.removeStylesOnCompDestroy, d = this.tracingService;
        switch (r.encapsulation) {
          case ce.Emulated:
            i = new Eo(c, l, r, this.appId, u, s, a, d);
            break;
          case ce.ShadowDom:
            return new vo(c, n, r, s, a, this.nonce, d, l);
          case ce.ExperimentalIsolatedShadowDom:
            return new vo(c, n, r, s, a, this.nonce, d);
          default:
            i = new On(c, l, r, u, s, a, d);
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
      return new (r || e12)(b(_a), b(Sa), b(Gr), b(Pm), b(W), b(X), b(Zr), b(Ut, 8));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
var An = class {
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
    return n ? this.doc.createElementNS(Ta[n] || n, t) : this.doc.createElement(t);
  }
  createComment(t) {
    return this.doc.createComment(t);
  }
  createText(t) {
    return this.doc.createTextNode(t);
  }
  appendChild(t, n) {
    (fd(t) ? t.content : t).appendChild(n);
  }
  insertBefore(t, n, r) {
    t && (fd(t) ? t.content : t).insertBefore(n, r);
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
      let i = Ta[o];
      i ? t.setAttributeNS(i, n, r) : t.setAttribute(n, r);
    } else
      t.setAttribute(n, r);
  }
  removeAttribute(t, n, r) {
    if (r) {
      let o = Ta[r];
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
    o & (Ne.DashCase | Ne.Important) ? t.style.setProperty(n, r, o & Ne.Important ? "important" : "") : t.style[n] = r;
  }
  removeStyle(t, n, r) {
    r & Ne.DashCase ? t.style.removeProperty(n) : t.style[n] = "";
  }
  setProperty(t, n, r) {
    t != null && (t[n] = r);
  }
  setValue(t, n) {
    t.nodeValue = n;
  }
  listen(t, n, r, o) {
    if (typeof t == "string" && (t = zt().getGlobalEventTarget(this.doc, t), !t))
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
function fd(e12) {
  return e12.tagName === "TEMPLATE" && e12.content !== void 0;
}
var vo = class extends An {
  hostEl;
  sharedStylesHost;
  shadowRoot;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, o, i, a), this.hostEl = n, this.sharedStylesHost = c, this.shadowRoot = n.attachShadow({ mode: "open" }), this.sharedStylesHost && this.sharedStylesHost.addHost(this.shadowRoot);
    let l = r.styles;
    l = hd(r.id, l);
    for (let d of l) {
      let p = document.createElement("style");
      s && p.setAttribute("nonce", s), p.textContent = d, this.shadowRoot.appendChild(p);
    }
    let u = r.getExternalStyles?.();
    if (u)
      for (let d of u) {
        let p = Ma(d, o);
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
var On = class extends An {
  sharedStylesHost;
  removeStylesOnCompDestroy;
  styles;
  styleUrls;
  constructor(t, n, r, o, i, s, a, c) {
    super(t, i, s, a), this.sharedStylesHost = n, this.removeStylesOnCompDestroy = o;
    let l = r.styles;
    this.styles = c ? hd(c, l) : l, this.styleUrls = r.getExternalStyles?.(c);
  }
  applyStyles() {
    this.sharedStylesHost.addStyles(this.styles, this.styleUrls);
  }
  destroy() {
    this.removeStylesOnCompDestroy && ft.size === 0 && this.sharedStylesHost.removeStyles(this.styles, this.styleUrls);
  }
};
var Eo = class extends On {
  contentAttr;
  hostAttr;
  constructor(t, n, r, o, i, s, a, c) {
    let l = o + "-" + r.id;
    super(t, n, r, i, s, a, c, l), this.contentAttr = Lm(l), this.hostAttr = Fm(l);
  }
  applyToHost(t) {
    this.applyStyles(), this.setAttribute(t, this.hostAttr, "");
  }
  createElement(t, n) {
    let r = super.createElement(t, n);
    return super.setAttribute(r, this.contentAttr, ""), r;
  }
};
var Do = class e9 extends Nn {
  supportsDOMEvents = true;
  static makeCurrent() {
    ba(new e9());
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
    let n = jm();
    return n == null ? null : Hm(n);
  }
  resetBaseElement() {
    kn = null;
  }
  getUserAgent() {
    return window.navigator.userAgent;
  }
  getCookie(t) {
    return Ca(document.cookie, t);
  }
};
var kn = null;
function jm() {
  return kn = kn || document.head.querySelector("base"), kn ? kn.getAttribute("href") : null;
}
function Hm(e12) {
  return new URL(e12, document.baseURI).pathname;
}
var Vm = (() => {
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
var gd = ["alt", "control", "meta", "shift"];
var Bm = { "\b": "Backspace", "	": "Tab", "\x7F": "Delete", "\x1B": "Escape", Del: "Delete", Esc: "Escape", Left: "ArrowLeft", Right: "ArrowRight", Up: "ArrowUp", Down: "ArrowDown", Menu: "ContextMenu", Scroll: "ScrollLock", Win: "OS" };
var $m = { alt: (e12) => e12.altKey, control: (e12) => e12.ctrlKey, meta: (e12) => e12.metaKey, shift: (e12) => e12.shiftKey };
var md = (() => {
  class e12 extends Rn {
    constructor(n) {
      super(n);
    }
    supports(n) {
      return e12.parseEventName(n) != null;
    }
    addEventListener(n, r, o, i) {
      let s = e12.parseEventName(r), a = e12.eventCallback(s.fullKey, o, this.manager.getZone());
      return this.manager.getZone().runOutsideAngular(() => zt().onAndCancel(n, s.domEventName, a, i));
    }
    static parseEventName(n) {
      let r = n.toLowerCase().split("."), o = r.shift();
      if (r.length === 0 || !(o === "keydown" || o === "keyup"))
        return null;
      let i = e12._normalizeKey(r.pop()), s = "", a = r.indexOf("code");
      if (a > -1 && (r.splice(a, 1), s = "code."), gd.forEach((l) => {
        let u = r.indexOf(l);
        u > -1 && (r.splice(u, 1), s += l + ".");
      }), s += i, r.length != 0 || i.length === 0)
        return null;
      let c = {};
      return c.domEventName = o, c.fullKey = s, c;
    }
    static matchEventFullKeyCode(n, r) {
      let o = Bm[n.key] || n.key, i = "";
      return r.indexOf("code.") > -1 && (o = n.code, i = "code."), o == null || !o ? false : (o = o.toLowerCase(), o === " " ? o = "space" : o === "." && (o = "dot"), gd.forEach((s) => {
        if (s !== o) {
          let a = $m[s];
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
      return new (r || e12)(b(W));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac });
  }
  return e12;
})();
async function Ra(e12, t) {
  return ad(Um(e12, t));
}
function Um(e12, t) {
  return { platformRef: t?.platformRef, appProviders: [...Zm, ...e12?.providers ?? []], platformProviders: qm };
}
function zm() {
  Do.makeCurrent();
}
function Wm() {
  return new be();
}
function Gm() {
  return Us(document), document;
}
var qm = [{ provide: In, useValue: ld }, { provide: qr, useValue: zm, multi: true }, { provide: W, useFactory: Gm }];
var Zm = [{ provide: tn, useValue: "root" }, { provide: be, useFactory: Wm }, { provide: Io, useClass: yo, multi: true }, { provide: Io, useClass: md, multi: true }, xa, Sa, _a, { provide: pt, useExisting: xa }, { provide: xn, useClass: Vm }, []];
var Aa = (() => {
  class e12 {
    static \u0275fac = function(r) {
      return new (r || e12)();
    };
    static \u0275prov = _({ token: e12, factory: function(r) {
      let o = null;
      return r ? o = new (r || e12)() : o = b(Qm), o;
    }, providedIn: "root" });
  }
  return e12;
})();
var Qm = (() => {
  class e12 extends Aa {
    _doc;
    constructor(n) {
      super(), this._doc = n;
    }
    sanitize(n, r) {
      if (r == null)
        return null;
      switch (n) {
        case ve.NONE:
          return r;
        case ve.HTML:
          return We(r, "HTML") ? xe(r) : Kr(this._doc, String(r)).toString();
        case ve.STYLE:
          return We(r, "Style") ? xe(r) : r;
        case ve.SCRIPT:
          if (We(r, "Script"))
            return xe(r);
          throw new v(5200, false);
        case ve.URL:
          return We(r, "URL") ? xe(r) : Yr(String(r));
        case ve.RESOURCE_URL:
          if (We(r, "ResourceURL"))
            return xe(r);
          throw new v(5201, false);
        default:
          throw new v(5202, false);
      }
    }
    bypassSecurityTrustHtml(n) {
      return Ws(n);
    }
    bypassSecurityTrustStyle(n) {
      return Gs(n);
    }
    bypassSecurityTrustScript(n) {
      return qs(n);
    }
    bypassSecurityTrustUrl(n) {
      return Zs(n);
    }
    bypassSecurityTrustResourceUrl(n) {
      return Qs(n);
    }
    static \u0275fac = function(r) {
      return new (r || e12)(b(W));
    };
    static \u0275prov = _({ token: e12, factory: e12.\u0275fac, providedIn: "root" });
  }
  return e12;
})();
var Pn = class e10 {
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
  page = H(0);
  pageSize = H(10);
  maxColumns = H(0);
  rowCount = H(null);
  tableHtml = H("");
  sortContext = H([]);
  orderableColumns = H([]);
  errorMessage = H(null);
  startExecution = H(false);
  isDeferredMode = H(false);
  dryRunInfo = H("");
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
  static \u0275prov = _({ token: e10, factory: e10.\u0275fac });
};
var Ym = ["tableContainer"];
var Km = ["app-root", ""];
function Jm(e12, t) {
  if (e12 & 1 && (L(0, "div", 2), G(1), F()), e12 & 2) {
    let n = ue();
    j(), ke(n.errorMessage());
  }
}
function Xm(e12, t) {
  e12 & 1 && (fo(0, "span", 7), G(1, " Run Query "));
}
function ey(e12, t) {
  e12 & 1 && G(0, " Run Query ");
}
function ty(e12, t) {
  if (e12 & 1) {
    let n = po();
    L(0, "div", 3)(1, "div", 4)(2, "p", 5), G(3), F(), L(4, "button", 6), Oe("click", function() {
      Me(n);
      let o = ue();
      return _e(o.handleRunQuery());
    }), wn(5, Xm, 2, 0)(6, ey, 1, 0), F()()();
  }
  if (e12 & 2) {
    let n = ue();
    j(3), ke(n.dryRunInfo()), j(), le("disabled", n.isLoading()), j(), Tn(n.isLoading() ? 5 : 6);
  }
}
function ny(e12, t) {
  if (e12 & 1 && (L(0, "option", 18), G(1), F()), e12 & 2) {
    let n = t.$implicit;
    le("value", n), j(), ke(n === 0 ? "All" : n);
  }
}
function ry(e12, t) {
  if (e12 & 1 && (L(0, "option", 18), G(1), F()), e12 & 2) {
    let n = t.$implicit;
    le("value", n), j(), ke(n);
  }
}
function oy(e12, t) {
  if (e12 & 1) {
    let n = po();
    L(0, "div", 8, 0), Oe("click", function(o) {
      Me(n);
      let i = ue();
      return _e(i.handleTableClick(o));
    }), F(), L(2, "footer", 9)(3, "span", 10), G(4), F(), L(5, "div", 11)(6, "button", 12), Oe("click", function() {
      Me(n);
      let o = ue();
      return _e(o.handlePageChange(-1));
    }), G(7, "<"), F(), L(8, "span", 13), G(9), F(), L(10, "button", 12), Oe("click", function() {
      Me(n);
      let o = ue();
      return _e(o.handlePageChange(1));
    }), G(11, ">"), F()(), L(12, "div", 14)(13, "div", 15)(14, "label", 16), G(15, "Max columns:"), F(), L(16, "select", 17), Oe("change", function(o) {
      Me(n);
      let i = ue();
      return _e(i.handleMaxColumnsChange(o));
    }), lo(17, ny, 2, 2, "option", 18, co), F()(), L(19, "div", 19)(20, "label", 20), G(21, "Page size:"), F(), L(22, "select", 21), Oe("change", function(o) {
      Me(n);
      let i = ue();
      return _e(i.handlePageSizeChange(o));
    }), lo(23, ry, 2, 2, "option", 18, co), F()()()();
  }
  if (e12 & 2) {
    let n = ue();
    le("innerHTML", n.sanitizedHtml(), Ys), j(4), ke(n.rowCountText()), j(2), le("disabled", n.prevPageDisabled()), j(3), ke(n.pageIndicatorText()), j(), le("disabled", n.nextPageDisabled()), j(6), le("value", n.maxColumns()), j(), uo(n.maxColumnOptions), j(5), le("value", n.pageSize()), j(), uo(n.pageSizeOptions);
  }
}
var bo = class e11 {
  state = E(Pn);
  sanitizer = E(Aa);
  maxColumnOptions = [5, 10, 15, 20, 0];
  pageSizeOptions = [10, 25, 50, 100];
  errorMessage = this.state.errorMessage;
  maxColumns = this.state.maxColumns;
  pageSize = this.state.pageSize;
  page = this.state.page;
  rowCount = this.state.rowCount;
  isDeferredMode = this.state.isDeferredMode;
  dryRunInfo = this.state.dryRunInfo;
  isLoading = H(false);
  sanitizedHtml = Ge(() => this.sanitizer.bypassSecurityTrustHtml(this.state.tableHtml()));
  totalPages = Ge(() => {
    let t = this.rowCount(), n = this.pageSize();
    return t !== null && n > 0 ? Math.ceil(t / n) : null;
  });
  pageIndicatorText = Ge(() => {
    let t = this.page(), n = this.rowCount(), r = this.totalPages(), o = (t + 1).toLocaleString(), i = (r ?? 1).toLocaleString();
    return `Page ${o} of ${i}`;
  });
  rowCountText = Ge(() => {
    let t = this.rowCount();
    return t === null ? "Total rows unknown" : t === 0 ? "0 total rows" : `${t.toLocaleString()} total rows`;
  });
  prevPageDisabled = Ge(() => this.page() === 0);
  nextPageDisabled = Ge(() => {
    let t = this.page(), n = this.rowCount(), r = this.totalPages();
    return n === null ? false : n === 0 ? true : r !== null && t >= r - 1;
  });
  isDarkMode = H(false);
  themeObserver = null;
  tableContainerRef;
  isHeightInitialized = false;
  constructor() {
    Cr(() => {
      let t = this.state.tableHtml(), n = this.state.sortContext(), r = this.state.orderableColumns();
      this.isHeightInitialized = false, setTimeout(() => {
        this.applySortIndicators(), this.lockInitialHeight();
      }, 0);
    }), Cr(() => {
      this.state.startExecution() || this.isLoading.set(false);
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
    t.shiftKey ? c !== -1 ? l[c].ascending ? l[c] = O(A({}, l[c]), { ascending: false }) : l.splice(c, 1) : l.push({ column: i, ascending: true }) : c !== -1 && l.length === 1 ? l[c].ascending ? l[c] = O(A({}, l[c]), { ascending: false }) : l = [] : l = [{ column: i, ascending: true }], this.state.setSortContext(l);
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
  static \u0275cmp = la({ type: e11, selectors: [["", "app-root", ""]], viewQuery: function(n, r) {
    if (n & 1 && ho(Ym, 5), n & 2) {
      let o;
      ha(o = ga()) && (r.tableContainerRef = o.first);
    }
  }, features: [ya([Pn])], attrs: Km, decls: 4, vars: 4, consts: [["tableContainer", ""], [1, "bigframes-widget"], [1, "bigframes-error-message"], [1, "deferred-container"], [1, "deferred-card"], [1, "deferred-estimate"], [1, "run-query-button", 3, "click", "disabled"], [1, "spinner"], [1, "table-container", 3, "click", "innerHTML"], [1, "footer"], [1, "row-count"], [1, "pagination"], [3, "click", "disabled"], [1, "page-indicator"], [1, "settings"], [1, "max-columns"], ["for", "max-cols-select"], ["id", "max-cols-select", 3, "change", "value"], [3, "value"], [1, "page-size"], ["for", "page-size-select"], ["id", "page-size-select", 3, "change", "value"]], template: function(n, r) {
    n & 1 && (L(0, "div", 1), wn(1, Jm, 2, 1, "div", 2), wn(2, ty, 7, 3, "div", 3)(3, oy, 25, 7), F()), n & 2 && (go("bigframes-dark-mode", r.isDarkMode()), j(), Tn(r.errorMessage() ? 1 : -1), j(), Tn(r.isDeferredMode() ? 2 : 3));
  }, styles: [".bigframes-widget.bigframes-widget[_ngcontent-%COMP%]{--bf-bg: white;--bf-border-color: #ccc;--bf-error-bg: #fbe;--bf-error-border: red;--bf-error-fg: black;--bf-fg: black;--bf-header-bg: #f5f5f5;--bf-null-fg: gray;--bf-row-even-bg: #f5f5f5;--bf-row-odd-bg: white;background-color:var(--bf-bg);box-sizing:border-box;color:var(--bf-fg);display:flex;flex-direction:column;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;margin:0;padding:0;width:100%}.bigframes-widget[_ngcontent-%COMP%]   *[_ngcontent-%COMP%]{box-sizing:border-box}@media(prefers-color-scheme:dark){.bigframes-widget.bigframes-widget[_ngcontent-%COMP%]{--bf-bg: var(--vscode-editor-background, #202124);--bf-border-color: #444;--bf-error-bg: #511;--bf-error-border: #f88;--bf-error-fg: #fcc;--bf-fg: white;--bf-header-bg: var(--vscode-editor-background, black);--bf-null-fg: #aaa;--bf-row-even-bg: #202124;--bf-row-odd-bg: #383838}}.bigframes-widget.bigframes-dark-mode.bigframes-dark-mode[_ngcontent-%COMP%]{--bf-bg: var(--vscode-editor-background, #202124);--bf-border-color: #444;--bf-error-bg: #511;--bf-error-border: #f88;--bf-error-fg: #fcc;--bf-fg: white;--bf-header-bg: var(--vscode-editor-background, black);--bf-null-fg: #aaa;--bf-row-even-bg: #202124;--bf-row-odd-bg: #383838}.bigframes-widget[_ngcontent-%COMP%]   .table-container[_ngcontent-%COMP%]{background-color:var(--bf-bg);margin:0;overflow:auto;padding:0}.bigframes-widget[_ngcontent-%COMP%]   .footer[_ngcontent-%COMP%]{align-items:center;background-color:var(--bf-bg);color:var(--bf-fg);display:flex;font-size:.8rem;justify-content:space-between;padding:8px}.bigframes-widget[_ngcontent-%COMP%]   .footer[_ngcontent-%COMP%] > *[_ngcontent-%COMP%]{flex:1}.bigframes-widget[_ngcontent-%COMP%]   .pagination[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:4px;justify-content:center;padding:4px}.bigframes-widget[_ngcontent-%COMP%]   .page-indicator[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .row-count[_ngcontent-%COMP%]{margin:0 8px}.bigframes-widget[_ngcontent-%COMP%]   .settings[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:16px;justify-content:end}.bigframes-widget[_ngcontent-%COMP%]   .page-size[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .max-columns[_ngcontent-%COMP%]{align-items:center;display:flex;flex-direction:row;gap:4px}.bigframes-widget[_ngcontent-%COMP%]   .page-size[_ngcontent-%COMP%]   label[_ngcontent-%COMP%], .bigframes-widget[_ngcontent-%COMP%]   .max-columns[_ngcontent-%COMP%]   label[_ngcontent-%COMP%]{margin-right:8px}.bigframes-widget[_ngcontent-%COMP%]     table.bigframes-widget-table, .bigframes-widget[_ngcontent-%COMP%]     table.dataframe{background-color:var(--bf-bg);border:1px solid var(--bf-border-color);border-collapse:collapse;border-spacing:0;box-shadow:none;color:var(--bf-fg);margin:0;outline:none;text-align:left;width:auto}.bigframes-widget[_ngcontent-%COMP%]     tr{border:none}.bigframes-widget[_ngcontent-%COMP%]     th{background-color:var(--bf-header-bg);border:1px solid var(--bf-border-color);color:var(--bf-fg);padding:0;position:sticky;text-align:left;top:0;z-index:1}.bigframes-widget[_ngcontent-%COMP%]     td{border:1px solid var(--bf-border-color);color:var(--bf-fg);padding:.5em}.bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(odd), .bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(odd) td{background-color:var(--bf-row-odd-bg)}.bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(2n), .bigframes-widget[_ngcontent-%COMP%]     table tbody tr:nth-child(2n) td{background-color:var(--bf-row-even-bg)}.bigframes-widget[_ngcontent-%COMP%]     .bf-header-content{box-sizing:border-box;height:100%;overflow:auto;padding:.5em;resize:horizontal;width:100%}.bigframes-widget[_ngcontent-%COMP%]     th .sort-indicator{padding-left:4px;visibility:hidden}.bigframes-widget[_ngcontent-%COMP%]     th:hover .sort-indicator{visibility:visible}.bigframes-widget[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]{background-color:transparent;border:1px solid currentColor;border-radius:4px;color:inherit;cursor:pointer;display:inline-block;padding:2px 8px;text-align:center;text-decoration:none;-webkit-user-select:none;user-select:none;vertical-align:middle}.bigframes-widget[_ngcontent-%COMP%]   button[_ngcontent-%COMP%]:disabled{opacity:.65;pointer-events:none}.bigframes-widget[_ngcontent-%COMP%]   .bigframes-error-message[_ngcontent-%COMP%]{background-color:var(--bf-error-bg);border:1px solid var(--bf-error-border);border-radius:4px;color:var(--bf-error-fg);font-size:14px;margin-bottom:8px;padding:8px}.bigframes-widget[_ngcontent-%COMP%]     .cell-align-right{text-align:right}.bigframes-widget[_ngcontent-%COMP%]     .cell-align-left{text-align:left}.bigframes-widget[_ngcontent-%COMP%]     .null-value{color:var(--bf-null-fg)}.bigframes-widget[_ngcontent-%COMP%]     .debug-info{border-top:1px solid var(--bf-border-color)}.bigframes-widget[_ngcontent-%COMP%]   .deferred-container[_ngcontent-%COMP%]{align-items:center;display:flex;justify-content:center;min-height:220px;padding:24px;width:100%}.bigframes-widget[_ngcontent-%COMP%]   .deferred-card[_ngcontent-%COMP%]{background:linear-gradient(135deg,#fff9,#ffffff4d);border:1px solid rgba(255,255,255,.4);border-radius:16px;box-shadow:0 8px 32px #1f268712;display:flex;flex-direction:column;gap:16px;max-width:500px;padding:32px;text-align:center;transition:all .3s ease-in-out}.bigframes-widget.bigframes-dark-mode[_ngcontent-%COMP%]   .deferred-card[_ngcontent-%COMP%]{background:linear-gradient(135deg,#20212499,#2021244d);border:1px solid rgba(255,255,255,.1);box-shadow:0 8px 32px #0000004d}@media(prefers-color-scheme:dark){.bigframes-widget[_ngcontent-%COMP%]   .deferred-card[_ngcontent-%COMP%]{background:linear-gradient(135deg,#20212499,#2021244d);border:1px solid rgba(255,255,255,.1);box-shadow:0 8px 32px #0000004d}}.bigframes-widget[_ngcontent-%COMP%]   .deferred-title[_ngcontent-%COMP%]{font-size:1.1rem;font-weight:600;margin:0}.bigframes-widget[_ngcontent-%COMP%]   .deferred-estimate[_ngcontent-%COMP%]{color:var(--bf-null-fg);font-size:.9rem;margin:0}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]{align-items:center;background-color:var(--bf-fg);border:1px solid var(--bf-fg);border-radius:8px;color:var(--bf-bg);cursor:pointer;display:inline-flex;font-size:14px;font-weight:600;gap:8px;justify-content:center;padding:10px 20px;transition:transform .2s ease,opacity .2s ease}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]:hover{opacity:.9;transform:translateY(-1px)}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]:active{transform:translateY(0)}.bigframes-widget[_ngcontent-%COMP%]   .run-query-button[_ngcontent-%COMP%]:disabled{cursor:not-allowed;opacity:.6}.bigframes-widget[_ngcontent-%COMP%]   .spinner[_ngcontent-%COMP%]{animation:_ngcontent-%COMP%_spin 1s linear infinite;border:2px solid currentColor;border-radius:50%;border-top-color:transparent;display:inline-block;height:12px;width:12px}@keyframes _ngcontent-%COMP%_spin{to{transform:rotate(360deg)}}"] });
};
function iy({ model: e12, el: t }) {
  let n = document.createElement("div");
  n.setAttribute("app-root", ""), t.appendChild(n);
  let r = { providers: [zi(), va(), { provide: "ANYWIDGET_MODEL", useValue: e12 }] };
  Ra(r).then((o) => {
    o.bootstrap(bo, n), n.removeAttribute("app-root");
  }).catch((o) => console.error(o));
}
var gS = { render: iy };
export {
  gS as default
};
