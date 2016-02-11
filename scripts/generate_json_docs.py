import argparse
import json

from parinx.parser import parse_docstring
import pdoc


class Module(object):
    def __init__(self, module_id, name, description=None, methods=None):
        self.module_id = module_id
        self.name = name
        self.description = description
        self.methods = methods or []

    @classmethod
    def from_module_name(cls, name):
        module = pdoc.Module(pdoc.import_module(name), allsubmodules=True)

        methods = module.functions() + module.variables()
        methods.extend(module.classes())
        for c in module.classes():
            methods.extend(c.doc.values())

        return cls(module_id=name,
                name=name.split('.')[-1].title(),
                description=module.docstring,
                methods=[Method.from_pdoc(m) for m in methods])

    def to_dict(self):
        return {'id': self.module_id, 'name': self.name,
                'description': self.description,
                'methods': [m.to_dict() for m in self.methods]}


class Method(object):

    def __init__(self, method_id, name, is_class, examples=None, metadata=None,
            params=None, exceptions=None, returns=None):
        self.method_id = method_id
        self.name = name
        self.examples = examples or []
        self.params = params or []
        self.exceptions = exceptions or []
        self.returns = returns or []

        if is_class:
            self.type = 'constructor'
        else:
            self.type = 'instance'

    def add_param(self, param):
        self.params.append(param)

    def add_example(self, example):
        self.examples.append({'code': example})

    def set_returns(self, param_type, description):
        self.returns = [{'types': [param_type], 'description': description}]

    def to_dict(self):
        return {'id': self.method_id, 'name': self.name,
                'examples': self.examples,
                'params': [p.to_dict() for p in self.params],
                'exceptions': self.exceptions, 'returns': self.returns}

    @classmethod
    def from_pdoc(cls, element):
        is_class = isinstance(element, pdoc.Class)
        method = cls(element.refname, element.name, is_class)

        if element.docstring:
            if not isinstance(element, pdoc.Class) and element.cls:
                cls = element.cls.cls
            else:
                cls = None

            method_info = parse_docstring(element.docstring, cls)

            for name, data in method_info['arguments'].items():
                param = Param.from_docstring_section(name, data)
                method.add_param(param)

            if method_info.get('example'):
                method.add_example(method_info['example'])

            #if 'return' in method_info:
            if method_info.get('return'):
                if len(method_info['return']['type_name']) > 1:
                    method.set_returns(method_info['return']['type_name'],
                                       method_info['return']['description'])

        return method


class Param(object):

    def __init__(self, name, description=None, types=None, optional=None,
            nullable=None):
        self.name = name
        self.description = description
        self.types = types or []
        self.optional = optional
        self.nullable = nullable

    def to_dict(self):
        return {'name': self.name, 'description': self.description,
                'types': self.types, 'optional': self.optional,
                'nullable': self.nullable}

    @classmethod
    def from_docstring_section(cls, name, data):
        return cls(name=name, description=data['description'],
                types=[data['type_name']])


def main():
    parser = argparse.ArgumentParser(description='Document Python modules.')
    parser.add_argument('module', help='The module name (ie, requests.api)')
    args = parser.parse_args()

    module = Module.from_module_name(args.module)
    print json.dumps(module.to_dict(), indent=2)


if __name__ == '__main__':
    main()
