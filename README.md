![TakeOff](logo-small.png)

# Takeoff
A Python toolset to launch full stack, web and mobile projects

[![CircleCI](https://circleci.com/gh/themarceloribeiro/takeoff-py.svg?style=svg)](https://app.circleci.com/pipelines/github/themarceloribeiro/takeoff-py)

```
pip install takeoff-py
```

Once installed you can use the generator to start building

## Web: Django Support

### New Project

Start by creating a new project. You will be asked for django admin credentials.

```
takeoff-generate web:project blog
```

### Generate models

For model generation:

```
takeoff-generate web:model blog category name:string summary:text
```

```
takeoff-generate web:model blog post category:belongs_to title:string summary:text contents:text drafted_at:datetime published:boolean 
```

### Generate web resources

After your model exists, you can create the web resource (standard index/show/create/edit functions)

```
takeoff-generate web:resource blog category
```

```
takeoff-generate web:resource blog post
```

### Generate user authentication

User authentication is also supported by a generator

```
takeoff-generate web:authentication blog
```

## API: Django REST Framework Support

### New Project

Start by creating a new project. You will be asked for django admin credentials.

```
takeoff-generate api:project blog
```

### Generate models

For model generation:

```
takeoff-generate api:model blog category name:string summary:text
```

```
takeoff-generate api:model blog post category:belongs_to title:string summary:text contents:text drafted_at:datetime published:boolean 
```

### Generate api resources

After your model exists, you can create the api resource (standard REST routes)

```
takeoff-generate api:resource blog category
```

```
takeoff-generate api:resource blog post
```

### Generate user authentication

User JWT authentication is also supported by a generator

```
takeoff-generate api:authentication blog
```

After authentication is generated, you can use the following routes for new tokens, refresh tokens:

```
curl -X POST -d "username=user&password=pass" http://localhost:8000/tokens/
```

```
curl -X POST -d "token=TOKEN" http://localhost:8000/tokens/refresh/
```

## Mobile: Android Support

### New Project

Start by creating a new project.

```
takeoff-generate android:project blog
```

### Generate rest entities

You can generate rest entities that answer to a json schema from an API:

```
takeoff-generate android:entity blog title published:boolean published_at:datetime read_count:integer
```


### Generate user authentication

User authentication is also supported by a generator

```
takeoff-generate android:authentication blog
```

And you can also ask for built-in facebook login:

```
takeoff-generate android:authentication blog facebook_auth=true facebook_app_id=XXXXXXXX facebook_scheme=fbXXXXXXXX
```

## Extra

### Android Facebook Login

Generating the key hash for facebook:

```
keytool -exportcert -alias androiddebugkey -keystore ~/.android/debug.keystore | openssl sha1 -binary | openssl base64
```