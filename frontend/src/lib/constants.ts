export enum accessLevels {
    undefined = -1,
    default = 0,
    user = 1,
    admin = 2,
    sadmin = 3
};

export enum messages {
    neutral = 0,
    success = 1,
    warning = 2,
    error = 3
}

export enum exercises {
    gapText = 1,
    syntax = 2,
    parsonsPuzzle = "ParsonsPuzzleExercise",
    findTheBug = 4,
    documentation = 5,
    output = 6,
    programming = "ProgrammingExercise"
}

export enum languages {
    python = "Python",
    java = "Java"
}

export const passwordLength = 8;

export const dashboardPage = "/admin-dashboard"