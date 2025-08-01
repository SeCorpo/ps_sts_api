# ps_sts_api
Primary School Student Tracking System - API

---
### General Rules

1. Models-classes don't directly interact with get_db
2. Always send the minimum and only if used personal data to client
3. never end on return True
4. Routers do not use db directly
5. Services perform query's to db
6. Every service / provider function has an explanatory description
7. Service modules manipulate database objects and are focussed on internal processes, 
they receive a database session from a router endpoint
8. Provider modules are service modules, with a more specified purpose
9. All directories are Python Packages (they include __init__)
10. Categorial directories and db tables have plural naming, files and objects have singular names
11. All models use BaseModel from core/base
12. When creating an object, return the created object to the client
13. Every database table has its own file and class (no two classes in one file)
14. Redis (sub) service functions use session_base_crud for crud operations

---
### Service functions
#### Naming conventions
- `get_"object"_by_"variable"`
- `update_"object"`
- `update_"object"_"variable"`
- `create_"object"`
- `delete_"object"`
- `toggle_"object"` : create / delete (standard: add: bool = True)

#### Rules
- Service create functions take a created_by_user_id from the current user
- Service functions (excluding base_crud and (some) in common) receive AND RETURN Pydantic schemas 
- Association models are managed within the (dominant) Model service module
- Service functions get a get_db() database session from the router calling them

---
### Schema's
#### Schema structure
- `"Object""Identifing variable"Schema(BaseSchema)` : eg PersonEmailSchema
- `"Object"Schema("Object""Identifing variable"Schema)` : with all required fields mandatory
- `"Object"UpdateSchema("Object""Identifing variable"Schema)` : with all fields optional
- `"Object""Variable/ Scenario"Schema("Object""Identifing variable"Schema)` : custom scenarios, eg PersonNameSchema

#### Rules
- All schemas use BaseSchema from core/base_schema
- Schemas use the same value naming as there Models, if possible (unless it's for added functionality)

---