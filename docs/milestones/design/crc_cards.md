# CRC Cards

| Attribute | Value |
|---|---|
| Class name | Database |
| Superclass |  |
| Responsibilities | create, read, update, delete exercise data; create, read, update, delete user data |
| Collaborators | AbstractExercise; User |

| Attribute | Value |
|---|---|
| Class name | Server |
| Superclass |  |
| Responsibilities | serve webpages and related files; provide API interface; translate API requests into SQL queries |
| Collaborators | Database |

| Attribute | Value |
|---|---|
| Class name | AbstractUser |
| Superclass |  |
| Responsibilities | reflect database structure; provide database interface; define API route |
| Collaborators | Database; Server |

| Attribute | Value |
|---|---|
| Class name | User |
| Superclass | AbstractUser |
| Responsibilities | solve exercises |
| Collaborators | AbstractExercise |

| Attribute | Value |
|---|---|
| Class name | Administrator |
| Superclass | AbstractUser |
| Responsibilities | manipulate exercise data; evaluate solutions; evaluate users |
| Collaborators | Database; ExerciseCreator; AbstractExercise; User; LearningProgress |

| Attribute | Value |
|---|---|
| Class name | AbstractExercise |
| Superclass |  |
| Responsibilities | reflect database structure; provide database interface; define API route |
| Collaborators | Database; Server |

| Attribute | Value |
|---|---|
| Class name | GapTextExercise |
| Superclass | AbstractExercise |
| Responsibilities |  |
| Collaborators |  |

| Attribute | Value |
|---|---|
| Class name | SyntaxExercise |
| Superclass | AbstractExercise |
| Responsibilities |  |
| Collaborators |  |

| Attribute | Value |
|---|---|
| Class name | ParsonsPuzzleExercise |
| Superclass | AbstractExercise |
| Responsibilities |  |
| Collaborators |  |

| Attribute | Value |
|---|---|
| Class name | FindTheBugExercise |
| Superclass | AbstractExercise |
| Responsibilities |  |
| Collaborators |  |

| Attribute | Value |
|---|---|
| Class name | DocumentationExercise |
| Superclass | AbstractExercise |
| Responsibilities |  |
| Collaborators |  |

| Attribute | Value |
|---|---|
| Class name | OutputExercise |
| Superclass | AbstractExercise |
| Responsibilities |  |
| Collaborators |  |

| Attribute | Value |
|---|---|
| Class name | ProgrammingExercise |
| Superclass | AbstractExercise |
| Responsibilities |  |
| Collaborators |  |

| Attribute | Value |
|---|---|
| Class name | ExerciseTracker |
| Superclass |  |
| Responsibilities | track solving time |
| Collaborators | Exercise |

| Attribute | Value |
|---|---|
| Class name | AbstractEvaluator |
| Superclass |  |
| Responsibilities | evaluate solution; store solution attempt and solving time |
| Collaborators | AbstractExercise; ExerciseTracker; Database; Administrator |

| Attribute | Value |
|---|---|
| Class name | SourceCodeEvaluator |
| Superclass | AbstractEvaluator |
| Responsibilities | parse user code; execute user code in sandbox |
| Collaborators | CodeSandbox |

| Attribute | Value |
|---|---|
| Class name | CodeSandbox |
| Superclass |  |
| Responsibilities | encapsulate user code |
| Collaborators |  |

| Attribute | Value |
|---|---|
| Class name | LearningProgress |
| Superclass |  |
| Responsibilities | assemble learning progress; create graphical representation |
| Collaborators | Database; User; AbstractExercise |

| Attribute | Value |
|---|---|
| Class name | ExerciseCreator |
| Superclass |  |
| Responsibilities | create exercise with hints and solution |
| Collaborators | Database; AbstractExercise |

| Attribute | Value |
|---|---|
| Class name | HomePage |
| Superclass |  |
| Responsibilities | provide login |
| Collaborators | User; LoginArea |

| Attribute | Value |
|---|---|
| Class name | LoginArea |
| Superclass |  |
| Responsibilities | display components |
| Collaborators | TextField; LoginButton; SignUpButton; ForgotPasswordButton |

| Attribute | Value |
|---|---|
| Class name | TextField |
| Superclass |  |
| Responsibilities | accept user input; obfuscate password input |
| Collaborators |  |

| Attribute | Value |
|---|---|
| Class name | LoginButton |
| Superclass |  |
| Responsibilities | trigger login process |
| Collaborators | Server |

| Attribute | Value |
|---|---|
| Class name | SignUpButton |
| Superclass |  |
| Responsibilities | trigger user creation process |
| Collaborators | Server |

| Attribute | Value |
|---|---|
| Class name | ForgotPasswordButton |
| Superclass |  |
| Responsibilities | trigger password reset process |
| Collaborators | Server |
