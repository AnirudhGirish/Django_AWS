
# AWS EC2 CENTRALISED

The current AWS infrastructure lacks a unified mechanism to comprehensively aggregate EC2 instance data across geographically distributed regions and organization accounts.

This necessitates manual intervention to gather and consolidate instance information from disparate sources, hindering visibility and control over resources.

This Django web-application developed is a centralized solution that addresses this challenge. The solution will bridge the gap by establishing a unified platform for retrieving and presenting EC2 instance data from multiple regions and accounts. This will provide a holistic view of the entire EC2 infrastructure, empowering users with improved resource management capabilities.


## About the application

* This tool offers a comprehensive solution for efficient multi-account and multi-region instance management.
* It gathers detailed information from instances across various regions and accounts, presenting it on a single, user-friendly interface. 
* Users can easily filter instances based on specific attributes and export the data in `CSV format`. 
* By providing a centralized and streamlined approach, this tool significantly enhances the user experience and simplifies instance management across different environments.


## Environment Variables

To run this project, you will need to add the following environment variables to your `.env file`. However, everything is included in `requirments.txt`

`Django`
`boto3`
`cryptography`
`sqlparse`
`python-dateutil`
`botocore`
`jmespath`
`asgiref`
`cffi`
`pycparser`
`s3transfer`
`six`
`urllib3`


## Run Django Locally

Clone the project

```bash
  git clone https://github.com/AnirudhGirish/Django_AWS
```

Go to the project directory

```bash
  cd myproject
```

Create Virtual Environment

```bash
  python3 -m venv .env
```

Activate Virtual Environment

```bash
  source .env/bin/activate
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Setting up the DB and Models

```bash
  python3 manage.py makemigrations
```

```bash
  python3 manage.py migrate
```

Start the server

```bash
  python3 manage.py runserver
```


## Tech Stack

**Frontend:** `HTML, CSS, JavaScript`

**Backend:** `Django`

**Database:** `SQLite3`

## Acknowledgements

This project uses several open-source packages and libraries. We are grateful to the developers and maintainers of these projects:

- [Django](https://www.djangoproject.com/) - The web framework used for the application.
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK for Python to interact with AWS services.
- [cryptography](https://cryptography.io/en/latest/) - Provides cryptographic recipes and primitives.
- [sqlparse](https://sqlparse.readthedocs.io/en/latest/) - A non-validating SQL parser.
- [python-dateutil](https://dateutil.readthedocs.io/en/stable/) - Extensions to the standard Python datetime module.
- [botocore](https://botocore.amazonaws.com/v1/documentation/api/latest/index.html) - The low-level, data-driven core of boto3.
- [jmespath](https://jmespath.org/) - JSON Matching Expressions.
- [asgiref](https://asgiref.readthedocs.io/en/latest/) - ASGI utilities and reference implementation.
- [cffi](https://cffi.readthedocs.io/en/latest/) - Foreign Function Interface for Python calling C code.
- [pycparser](https://github.com/eliben/pycparser) - A complete C99 parser in pure Python.
- [s3transfer](https://github.com/boto/s3transfer) - A library for managing Amazon S3 transfers.
- [six](https://six.readthedocs.io/) - Python 2 and 3 compatibility utilities.
- [urllib3](https://urllib3.readthedocs.io/en/latest/) - A powerful, user-friendly HTTP client for Python.

By incorporating these tools, we can provide robust, secure, and efficient functionality in our application. Thank you to all the developers and maintainers of these packages!

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.


## Support

For support, email anirudhgirish08@gmail.com.

