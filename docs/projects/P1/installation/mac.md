# Installing NodeBB on MacOS

## Required Software

First, install the following programs:

-   <http://nodejs.org/>
-   <http://brew.sh/>

Verify installation of Node.js and npm. You should have version LTS of Node.js installed, and version 10 of npm installed:

```console
% node -v     # this should output "20.17.0" or similar
% npm -v      # this should output "10.8.2" or similar
```

There might be issues later if you are using an older Node version (<20).


### Installing Redis

Install redis with homebrew:

```console
% brew install redis
```

Start the redis server:

```console
% redis-server
```

## Installing NodeBB

You should have already forked the [class-specific repository](https://github.com/CMU-17313Q/NodeBB). Clone your forked repository onto your local machine.

Enter the directory where you have cloned the repository:

```console
% cd NodeBB
```

Run the interactive installation command:

```console
% ./nodebb setup
```

You will then be presented with a series of setup questions.

For each of the questions — **except for "Which database to use (mongo)"**, which you should answer with "redis" — you may accept the default answer by pressing ++enter++

```console
URL used to access this NodeBB (http://127.0.0.1:4567)
Please enter a NodeBB secret (ee18b7c3-1d23-41c9-800f-78d74acc0861)
Would you like to submit anonymous plugin usage to nbbpm? (yes)
Which database to use (mongo) redis

Now configuring redis database:
Host IP or address of your Redis instance (127.0.0.1)
Host port of your Redis instance (6379)
Password of your Redis database
Which database to use (0..n) (0)
```

The first time you run the `setup` command, you will also be asked to configure a forum administrator. When prompted, enter the desired information for the admin account. You can choose any admin username and password. Unfortunately (or fortunately), NodeBB won't accept weak passwords like `1234` :) so you need to come up with a slightly stronger password like `admin1234!`.

Once everything has finished installing, a configuration file `config.json` will be created. This file can be modified if you need to make changes to the above settings, such as the database location or credentials used to access the database.

After the installation, start the NodeBB server:

```console
% ./nodebb start
```

You can now visit your forum at [`http://localhost:4567/`](http://localhost:4567/).
