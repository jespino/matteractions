MatterActions
=============

MatterActions is a small service to use in combination with the
https://github.com/jespino/mattermost-post-actions-plugin plugin for
mattermost.

It provides a small set of configurable post actions and can be used as an skel
for your own mattermost action implementation, or simply to provide actions to
your post using the already implemented ones.

Build with docker
-----------------

```sh
docker build -t matteractions .
```

If you want, you can modify the Dockerfile to embed your configfile directly in
the container.

Run with docker
---------------

You can configure it using the environment variables following the pattern
`MMACTIONS_<SECTION>_<KEY>` for each entry in the config.example.ini file.

If I want to have Matteractions running my translate action enabled, you can run

```sh
docker run -e MMACTIONS_TRANSLATE_ENABLED=true \
           -e MMACTIONS_TRANSLATE_KEY=a-secret-key \
           -e MMACTIONS_TRANSLATE_CREDENTIALS_FILE=/usr/src/app/google_translate_credentials_file.json \
           -v my-crendentials-file.json:google_translate_credentials_file.json \
           --rm --name matteractions jespino/matteractions
```

Installation
------------

If you want install it in your machine without using docker, you can.

You need to clone the repository:

```
git clone github.com/jespino/matteractions.git
cd matteractions
```

Create your own virtualenv, for example:

```
mkvirtualenv matteractions
```

Install the requirements

```
pip install -r requirements.txt
```

Copy and modify `config.example.ini` to `config.ini`.

and run the application:

```
python ./main.py
```

How to Contribute?
------------------

Just open an issue or PR ;)

License
-------

Matteractions is licensed under BSD (2-Clause) license.
