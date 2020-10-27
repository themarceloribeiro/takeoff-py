# Takeoff
A Python toolset to launch full stack, web and mobile projects

[![<ORG_NAME>](https://circleci.com/github/themarceloribeiro/takeoff-py.svg?style=svg)](<LINK>)

```
pip install takeoff-py
```

Once installed you can use the generator to start building

## Web: Django Support

Start by creating a new project. You will be asked for django admin credentials.

```
takeoff-generate web:project blog
```

For model generation:

```
takeoff-generate web:model blog category name:string summary:text
```

```
takeoff-generate web:model blog post category:belongs_to title:string summary:text contents:text drafted_at:datetime published:boolean 
```

After your model exists, you can create the web resource (standard index/show/create/edit functions)

```
takeoff-generate web:resource blog category
```

```
takeoff-generate web:resource blog post
```