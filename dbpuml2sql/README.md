# README

The goal is to use a [PlantUML class diagram](http://plantuml.com/) in a [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) process to generate an _acceptable_ SQL script, via _class diagrams_ and a `physical data model`. Code below came from [here](https://github.com/freezed/ocp6/tree/master/src-puml).

## Code stucture

### `*.iuml` files contains project sources

 _(syntax uses [PlantUML's macro pre-processor](http://plantuml.com/preprocessing) feature)_

#### Classes

    class address
    class client
    class composition <<assoc>>
    (…)

#### Relations

    rel(address,1,--,1,restaurant)
    rel(address,1,--,*,employee)
    rel(client,1,--,1..2,phone)
    (…)

#### Attributes

    class address {
        att(label,String,VARCHAR(30) NOT NULL)
        att(name,String,VARCHAR(30) NOT NULL)
        att(line1,String,VARCHAR(30) NOT NULL)
        att(line2,String [0..1],VARCHAR(20))
        att(zip,String,VARCHAR(5) NOT NULL)
        att(city,String,VARCHAR(20) NOT NULL)
    }
    class client {
        att(1st_name,String,VARCHAR(30) NOT NULL)
        att(name,String,VARCHAR(30) NOT NULL)
        att(mail,String,VARCHAR(40) NOT NULL)
        att(login,String,VARCHAR(30) NOT NULL)
        att(password_sha2bin,String,BINARY(32) NOT NULL)
    }
    class composition {
        att(quantity,Integer,TINYINT NOT NULL UNSIGNED)
    }

#### Keys (primary and/or foreign)

    class address {
        pyk(id)
    }
    class client {
        pyk(id)
        fnk(delivery_address_id,address.id)
        fnk(billing_address_id,address.id)
        fnk(phone_id,phone.id)
    }
    class composition {
        pfk(pizza_id,pizza.id,TINYINT UNSIGNED NOT NULL)
        pfk(ingredient_id,ingredient.id,TINYINT UNSIGNED NOT NULL)
    }

#### Associatons classes

    rel(pizza,1..*,-,1..*,ingredient)
    rea(pizza,ingredient,..,composition)
    rel(ingredient,1..*,--,1..*,restaurant)
    rea(ingredient,restaurant,..,stock)
    (…)

### `*.puml` files contains includes and diagrams specific informations

#### Class diagram simplyfied

    @startuml
    title Functional domain description\n <i>(simplyfied)</i>
    /' = = = = = = = STYLE = = = = = = = '/
    skinparam monochrome true
    hide empty methods
    hide <<assoc>> circle
    skinparam class {
        BackgroundColor<<assoc>> lightblue
    }
    /' = = = = = = = MACRO = = = = = = = '/
    !define rel(a,b,c,d,e) a c e
    !define rea(a,b,c,d) (a, b) c d
    /' = = = = = = = CLASSE = = = = = = = '/
    !includeurl https://raw.githubusercontent.com/freezed/ocp6/master/src-puml/classes.iuml
    /' = = = = = = = ASSOCIATION = = = = = = = '/
    !includeurl https://raw.githubusercontent.com/freezed/ocp6/master/src-puml/associations.iuml
    @enduml

#### Class diagram

    @startuml
    title Functional domain description
    /' = = = = = = = STYLE = = = = = = = '/
    hide empty methods
    hide <<assoc>> circle
    skinparam class {
        BackgroundColor<<assoc>> lightblue
    }
    /' = = = = = = = MACRO = = = = = = = '/
    !define rel(a,b,c,d,e) a "b" c "d" e
    !define rea(a,b,c,d) (a, b) c d
    !define att(n,u,s) n : u
    /' = = = = = = = CLASSE = = = = = = = '/
    !includeurl https://raw.githubusercontent.com/freezed/ocp6/master/src-puml/classes.iuml
    /' = = = = = = = ATTRIBUTE = = = = = = = '/
    !includeurl https://raw.githubusercontent.com/freezed/ocp6/master/src-puml/attributes.iuml
    /' = = = = = = = ASSOCIATION = = = = = = = '/
    !includeurl https://raw.githubusercontent.com/freezed/ocp6/master/src-puml/associations.iuml
    @enduml

### Physical data model

    @startuml
    title Physical data model
    /' = = = = = = = STYLE = = = = = = = '/
    hide empty methods
    hide circle
    skinparam class {
        BackgroundColor<<assoc>> lightblue
    }
    /' = = = = = = = MACRO = = = = = = = '/
    !define rel(a,b,c,d,e) a c e
    !define rea(a,b,c,d) (a, b) c d
    !define pyk(n,t="MEDIUMINT NOT NULL UNSIGNED") <font color="red">PK:<b>n</b> <size:09>[t]</size></font>
    !define fnk(n,r,t="MEDIUMINT NOT NULL UNSIGNED") <font color="blue">FK:<b>n</b> <size:09>[t]</size></font>
    !define pfk(n,r,t="MEDIUMINT NOT NULL UNSIGNED") <font color="orangered">PFK:<b>n</b> <size:09>[t]</size></font>
    !define att(n,u,s) {field} <b>n</b> [s]
    /' = = = = = = = CLASSE = = = = = = = '/
    !includeurl https://raw.githubusercontent.com/freezed/ocp6/master/src-puml/classes.iuml
    /' = = = = = = = KEY = = = = = = = '/
    !includeurl https://raw.githubusercontent.com/freezed/ocp6/master/src-puml/keys.iuml
    /' = = = = = = = ATTRIBUTE = = = = = = = '/
    !includeurl https://raw.githubusercontent.com/freezed/ocp6/master/src-puml/attributes.iuml
    /' = = = = = = = ASSOCIATION = = = = = = = '/
    rel(pizza,.,-,.,composition)
    rel(composition,.,-,.,ingredient)
    rel(ingredient,.,--,.,stock)
    rel(stock,.,--,.,restaurant)
    @enduml

## Diagrams

![Simple functional domain description](https://raw.githubusercontent.com/freezed/py-puml-tools/master/dbpuml2sql/readme-diagrams/functional_model_simplyfied.png "Simple functional domain description")
___

![Functional domain description](https://raw.githubusercontent.com/freezed/py-puml-tools/master/dbpuml2sql/readme-diagrams/functional_model.png "Functional domain description")
___

![Physical data model](https://raw.githubusercontent.com/freezed/py-puml-tools/master/dbpuml2sql/readme-diagrams/physical_data_model.png "Physical data model")


## Roadmap

- [x] adds a bit verbosity when processing
- [ ] scrapes attributes
- [x] scrapes primary key
- [x] scrapes foreign key
- [x] scrapes primary foreign key
- use some preprocessing feature
    - [ ] `!includeurl`
- [ ] keep comments
- respect UML syntax in [PlantUML] file & extrapole SQL statement
    - [ ] use [UML primitive type](https://www.uml-diagrams.org/data-type.html#primitive-type)
    - [ ] define default parameters's types (VARCHAR, DECIMAL, DATETIME)
- [ ] MySQL/MariaDB SQL Syntax
- [ ] nest data in a nice dict like this:

```
    d = {
        "table1" : {
            "attr" : [
                {
                    "name" : "id"
                    "isPrimary" : true
                    "isForeign" : false
                    "type" : "String"
                },

            ]
        }
    }
```
