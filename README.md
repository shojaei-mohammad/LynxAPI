# LynxAPI

LynxAPI is a comprehensive API service for managing devices, offering secure admin authorization capabilities. This API is designed to be lightweight and easy to deploy on various platforms, providing a suite of tools for device management, network configuration, and system resource monitoring.

## Features

- Device information retrieval
- Network configuration management
- System resource monitoring
- Secure admin authorization
- Easy to install and run

## Quick Start

To install LynxAPI on your system, run the following command:

```bash
sudo bash -c "$(curl -sL https://github.com/shojaei-mohammad/LynxAPI-Scripts/raw/main/lynxapi.sh)"
```

This command will download and execute the lynxapi.sh installation script from the project's repository.
## Documentation

The LynxAPI project is documented with in-code docstrings. To generate and view the complete documentation, you can use tools like Sphinx, pdoc, or Doxygen. Each endpoint is described with detailed request and response examples, making it easy to understand and integrate into your systems.

For developers, LynxAPI provides Swagger UI for an interactive documentation experience. To enable or disable the Swagger documentation, you can adjust the `DOCS` variable in the `.env` file:

- To enable Swagger UI, set DOCS=yes.
- To disable it, set DOCS=no.

To access the Swagger UI:

Ensure the Swagger documentation is enabled by setting the `DOCS=true` in the `.env` file.
After starting the LynxAPI service, navigate to `http://<host>:<port>/docs` in your web browser, where `<host>` is the address where your server is running (by default this is 0.0.0.0), and `<port>` is the port specified in the `.env` file (default is 8081).

For example, if you're running the server locally and haven't changed the default port, you can access the Swagger UI at:

```url

http://localhost:8080/docs
http://localhost:8080/redoc
```

This will bring up the interactive Swagger UI where you can read about the API's endpoints, try out requests, and see the responses directly in your browser.

This allows you to control the visibility of your API documentation in production or development environments.
## Usage

After installation, LynxAPI can be accessed through its RESTful endpoints. You can use any HTTP client to interact with the API. The API is self-descriptive, with each endpoint providing a summary and description in its docstring.
## Support

If you encounter any issues or require support, please file an issue on the project's GitHub issue tracker.
## Contributing

We welcome contributions to the LynxAPI project. Please read the CONTRIBUTING.md file for guidelines on how to make a contribution.
## License

LynxAPI is released under the MIT License. Please see the LICENSE file for more details.

Enjoy using LynxAPI for your device management needs!

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@shojaei-mohammd](https://github.com/shojaei-mohammad)


## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


