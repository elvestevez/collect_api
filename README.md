# Data collect API REST
Microservice to get datasets.

- Select [endpoint](./doc/doc-data.json).
- Get JSON response:

    - data
    - metadata

You can get dimensions, facts tables, period available for data.

Datasets are collected and stored by [collect load](https://github.com/elvestevez/collect_load).

It's available web app [collect streamlit](https://github.com/elvestevez/collect_streamlit) to get data more friendly. Web app get data connecto to this microservice.

### **Technology stack**
Python, SQL, Pandas, JSON, flask.

### **Configuration**
Get project from GitHub and create a python environment with these additional libraries:
- flask
- sqlalchemy
- pandas

> Review requirements.txt file.

The application is deployed in heroku.

### **Usage**
You can use at url [data-collect-api](https://data-collect-api.herokuapp.com) heroku and enjoy!.

- Call [endpoint](https://data-collect-api.herokuapp.com/documentation).
- Get JSON.

### **Folder structure**

```
└── project
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    ├── runtime.txt
    ├── Procfile
    ├── datatype.properties
    ├── wsgi.py
    ├── db
    ├── doc
    └── modules
        ├── api
        └── get
```

---

### **Next steps**
- Other technologies on cloud (Azure, AWS...).
- Add new endpoints.
- Improve endpoints documentation with swagger.
- Add new datasets (if they are availabe by collect load).
