## 用途
定义如何通过 .relationship.json 如何记录 design 文件之前的关系

## 格式
```json
"{namespace}.{filename}": {
    type: class | method,
    parent: {namespace}.{filename} | None,
    codePath: "{相对于 work-space 的目标代码文件路径}" | None,
    fields: [{"{fieldname}": {usedBy: ["{namespace}.{filename}.{method}"] | []}} ... ],
    methods: [{"{methodname}": {paras: "{paras}", invoke:["{namespace}.{filename}.{method}({parames})"] | [], invokeBy: ["{namespace}.{filename}({parames})"] | []}  } ... ]
}
```

`codePath`：该设计文档对应的目标源代码文件路径。由 `make` 工作流首次生成代码（Designed→Created）时推导/确认后写入；后续 `make`（Changed→Updated）与 `validation` 直接读取该字段，不重新推导。设计文档仍为 Designing/Designed 状态、尚未生成代码时为 `None`。

`fields` 仅用于 `type: class`：记录该类的成员变量，以及哪些方法（本类或跨类）读取/依赖了该成员变量（`usedBy`）。用于成员变量变更时的影响分析。

当 `make` 工作流处理设计文档中被删除的方法时，`record_relationship.py` 需将 `methods` 数组中对应的方法记录同步移除，避免后续 `change-design` 影响分析读取到已不存在的方法。

## 示例
``` json
{"com.zt.xx": {
    "type": "class", 
    "parent":  "None",
    "codePath": "src/com/zt/xx.py",
    "fields": [{"secretKey": {"usedBy": ["com.zt.xx.encrypt"]}}],
    "methods": [{"encrypt": {"paras": "string username, string pwd", "invoke": [] , "invokeBy":  ["com.zt.yy.login(username, pwd)"]}   },
    {"encrypt": {"paras": "string pwd", "invoke":[] , "invokeBy":  ["com.zt.yy.login(username,pwd)"]}   }]
},
"com.zt.yy": {
    "type": "class", 
    "parent":  "None",
    "codePath": "src/com/zt/yy.py",
    "fields": [],
    "methods": [{"login": {"paras": "string username, string pwd", "invoke":["com.zt.xx.encrypt(username,pwd)","com.zt.xx.encrypt(pwd)"] , "invokeBy":  []}}]
},
"com.zt.zz": {
    "type": "method", 
    "parent":  "None",
    "codePath": "src/com/zt/zz.py",
    "methods": [{"zip": {"paras": "string content","invoke": [] , "invokeBy":[]}}]
}
}
```

## 更新方式：
调用脚本 `record_relationship.py`