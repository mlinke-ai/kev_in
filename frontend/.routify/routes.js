
/**
 * @roxi/routify 2.18.11
 * File generated Wed Mar 08 2023 15:36:54 GMT+0100 (Mitteleuropäische Normalzeit)
 */

export const __version = "2.18.11"
export const __timestamp = "2023-03-08T14:36:54.991Z"

//buildRoutes
import { buildClientTree } from "@roxi/routify/runtime/buildRoutes"

//imports
import __fallback from '../src/pages/_fallback.svelte'
import _admin_add_user from '../src/pages/admin/add_user.svelte'
import _admin_index from '../src/pages/admin/index.svelte'
import _admin_view_exercises from '../src/pages/admin/view_exercises.svelte'
import _admin_view_solutions from '../src/pages/admin/view_solutions.svelte'
import _admin_view_users from '../src/pages/admin/view_users.svelte'
import _admin__reset from '../src/pages/admin/_reset.svelte'
import _exercises__exerciseID from '../src/pages/exercises/[exerciseID].svelte'
import _exercises_create_parsonspuzzle from '../src/pages/exercises/create/parsonspuzzle.svelte'
import _exercises_create_programming from '../src/pages/exercises/create/programming.svelte'
import _exercises_create__reset from '../src/pages/exercises/create/_reset.svelte'
import _exercises__reset from '../src/pages/exercises/_reset.svelte'
import _index from '../src/pages/index.svelte'
import _user_index from '../src/pages/user/index.svelte'
import _user_my_solutions from '../src/pages/user/my_solutions.svelte'
import _user_profile from '../src/pages/user/profile.svelte'
import _user__reset from '../src/pages/user/_reset.svelte'
import __layout from '../src/pages/_layout.svelte'

//options
export const options = {}

//tree
export const _tree = {
  "root": true,
  "children": [
    {
      "isFallback": true,
      "path": "/_fallback",
      "component": () => __fallback
    },
    {
      "isDir": true,
      "children": [
        {
          "isPage": true,
          "path": "/admin/add_user",
          "id": "_admin_add_user",
          "component": () => _admin_add_user
        },
        {
          "isIndex": true,
          "isPage": true,
          "path": "/admin/index",
          "id": "_admin_index",
          "component": () => _admin_index
        },
        {
          "isPage": true,
          "path": "/admin/view_exercises",
          "id": "_admin_view_exercises",
          "component": () => _admin_view_exercises
        },
        {
          "isPage": true,
          "path": "/admin/view_solutions",
          "id": "_admin_view_solutions",
          "component": () => _admin_view_solutions
        },
        {
          "isPage": true,
          "path": "/admin/view_users",
          "id": "_admin_view_users",
          "component": () => _admin_view_users
        }
      ],
      "isLayout": true,
      "isReset": true,
      "path": "/admin",
      "id": "_admin__reset",
      "component": () => _admin__reset
    },
    {
      "isDir": true,
      "children": [
        {
          "isPage": true,
          "path": "/exercises/:exerciseID",
          "id": "_exercises__exerciseID",
          "component": () => _exercises__exerciseID
        },
        {
          "isDir": true,
          "children": [
            {
              "isPage": true,
              "path": "/exercises/create/parsonspuzzle",
              "id": "_exercises_create_parsonspuzzle",
              "component": () => _exercises_create_parsonspuzzle
            },
            {
              "isPage": true,
              "path": "/exercises/create/programming",
              "id": "_exercises_create_programming",
              "component": () => _exercises_create_programming
            }
          ],
          "isLayout": true,
          "isReset": true,
          "path": "/exercises/create",
          "id": "_exercises_create__reset",
          "component": () => _exercises_create__reset
        }
      ],
      "isLayout": true,
      "isReset": true,
      "path": "/exercises",
      "id": "_exercises__reset",
      "component": () => _exercises__reset
    },
    {
      "isIndex": true,
      "isPage": true,
      "path": "/index",
      "id": "_index",
      "component": () => _index
    },
    {
      "isDir": true,
      "children": [
        {
          "isIndex": true,
          "isPage": true,
          "path": "/user/index",
          "id": "_user_index",
          "component": () => _user_index
        },
        {
          "isPage": true,
          "path": "/user/my_solutions",
          "id": "_user_my_solutions",
          "component": () => _user_my_solutions
        },
        {
          "isPage": true,
          "path": "/user/profile",
          "id": "_user_profile",
          "component": () => _user_profile
        }
      ],
      "isLayout": true,
      "isReset": true,
      "path": "/user",
      "id": "_user__reset",
      "component": () => _user__reset
    }
  ],
  "isLayout": true,
  "path": "/",
  "id": "__layout",
  "component": () => __layout
}


export const {tree, routes} = buildClientTree(_tree)
