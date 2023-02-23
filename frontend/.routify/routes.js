
/**
 * @roxi/routify 2.18.11
 * File generated Thu Feb 23 2023 14:20:52 GMT+0100 (Mitteleuropäische Normalzeit)
 */

export const __version = "2.18.11"
export const __timestamp = "2023-02-23T13:20:52.618Z"

//buildRoutes
import { buildClientTree } from "@roxi/routify/runtime/buildRoutes"

//imports


//options
export const options = {}

//tree
export const _tree = {
  "root": true,
  "children": [
    {
      "isFallback": true,
      "path": "/_fallback",
      "component": () => import('../src/pages/_fallback.svelte').then(m => m.default)
    },
    {
      "isDir": true,
      "children": [
        {
          "isPage": true,
          "path": "/admin/Exercises",
          "id": "_admin_Exercises",
          "component": () => import('../src/pages/admin/Exercises.svelte').then(m => m.default)
        },
        {
          "isIndex": true,
          "isPage": true,
          "path": "/admin/index",
          "id": "_admin_index",
          "component": () => import('../src/pages/admin/index.svelte').then(m => m.default)
        },
        {
          "isPage": true,
          "path": "/admin/Solutions",
          "id": "_admin_Solutions",
          "component": () => import('../src/pages/admin/Solutions.svelte').then(m => m.default)
        },
        {
          "isPage": true,
          "path": "/admin/Users",
          "id": "_admin_Users",
          "component": () => import('../src/pages/admin/Users.svelte').then(m => m.default)
        }
      ],
      "isLayout": true,
      "isReset": true,
      "path": "/admin",
      "id": "_admin__reset",
      "component": () => import('../src/pages/admin/_reset.svelte').then(m => m.default)
    },
    {
      "isDir": true,
      "children": [
        {
          "isPage": true,
          "path": "/exercises/:exerciseID",
          "id": "_exercises__exerciseID",
          "component": () => import('../src/pages/exercises/[exerciseID].svelte').then(m => m.default)
        },
        {
          "isDir": true,
          "children": [
            {
              "isPage": true,
              "path": "/exercises/create/ParsonsPuzzleExerciseCreate",
              "id": "_exercises_create_ParsonsPuzzleExerciseCreate",
              "component": () => import('../src/pages/exercises/create/ParsonsPuzzleExerciseCreate.svelte').then(m => m.default)
            }
          ],
          "isLayout": true,
          "isReset": true,
          "path": "/exercises/create",
          "id": "_exercises_create__reset",
          "component": () => import('../src/pages/exercises/create/_reset.svelte').then(m => m.default)
        }
      ],
      "isLayout": true,
      "isReset": true,
      "path": "/exercises",
      "id": "_exercises__reset",
      "component": () => import('../src/pages/exercises/_reset.svelte').then(m => m.default)
    },
    {
      "isIndex": true,
      "isPage": true,
      "path": "/index",
      "id": "_index",
      "component": () => import('../src/pages/index.svelte').then(m => m.default)
    },
    {
      "isDir": true,
      "children": [
        {
          "isIndex": true,
          "isPage": true,
          "path": "/user/index",
          "id": "_user_index",
          "component": () => import('../src/pages/user/index.svelte').then(m => m.default)
        }
      ],
      "isLayout": true,
      "isReset": true,
      "path": "/user",
      "id": "_user__reset",
      "component": () => import('../src/pages/user/_reset.svelte').then(m => m.default)
    }
  ],
  "isLayout": true,
  "path": "/",
  "id": "__layout",
  "component": () => import('../src/pages/_layout.svelte').then(m => m.default)
}


export const {tree, routes} = buildClientTree(_tree)

