# Marrs

Marrs is a Python package for Android Java apps researchers, built on top of tools like [frida](https://frida.re) and
[adb](https://developer.android.com/studio/command-line/adb).  
Using Marrs you can write Python code that modifies fields' value, calls methods, creates instances, hooks methods and
more.

## Getting started

### Prerequisites

1. Python >= 3.7
2. Connected device with USB Debugging enabled (or an Android emulator).
3. Features involving frida require rooted device (`su` is required).

### Installation

Using pip:

    pip install marrs

Or from source:

    git clone https://github.com/oran1248/marrs.git
    cd marrs
    python setup.py install

## Documentation

For full documentation, please see [here](https://oran1248.github.io/marrs/).

## Usage example

***NOTE***: This code demonstrates the use of some of the features (there are many more)

    import marrs

    # Get connected device
    device = marrs.get_device()

    # Install app
    app = device.install_app("testapp.apk")

    # Attach frida agent to app (ROOT is required).
    # If needed, will do some magic tricks in order to run frida server on the device and then will start the app.
    agent = app.attach_frida_agent()

    # Get class object
    cls = agent.get_class("com.example.testapp.MyClass")

    # Increment static field of type int by 1
    cls.set_field(cls.get_field("intField") + 1)

    # Create new instance of type MyClass
    instance = cls.new(['someString', 2, 3])
    
    # Get instance field value (can be primitive type or reference type)
    fieldValue = instance.get("someField") 
    
    # Call an instance method
    retVal = instance.call("someInstanceMethod", params = [cls.new(), fieldValue])

    # Hook a method - first create your hook implementation function
    def my_hook(params, orig_retval):
        return 1337

    # Create the hook
    agent.hooks.add("com.example.testapp.MyClass", "someIntFunc", hook_impl=my_hook)

    # num's value will be 1337
    num = instance.call("someIntFunc", [1, 2])

For more examples, please refer to the [docs](https://oran1248.github.io/marrs/) or see the [tests](tests).

## Caveat

Marrs wasn't tested on all the platforms and devices.  
If you run into a bug, you can [open an issue](issues), or even better than that - fix it and create a PR. create a PR
with the fix.

## Running Tests

Steps for running the tests:

1. Install `pytest` package:

`pip install pytest`

2. Build `test-app` app - it's a simple android app used for testing Marrs:

`cd test-app`

`gradlew build`

3. Install test-app's APK on a connected rooted device
4. Run the tests:

`cd misc`

`run_tests.bat`

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the terms of GNU General Public License v3.0.









