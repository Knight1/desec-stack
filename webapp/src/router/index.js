import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import DomainList from "../views/Console/DomainList/index";
import {HTTP, logout} from "../utils";
import Login from "../views/Login";
import store from '../store';
import CrudDomainList from "../views/CrudDomainList";
import CrudDomain from "../views/Domain/CrudDomain";
import Domain from "../views/Domain";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/signup/:email?',
    name: 'signup',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "signup" */ '../views/SignUp.vue')
  },
  {
    path: '/custom-setup/:domain',
    name: 'customSetup',
    component: () => import(/* webpackChunkName: "signup" */ '../views/CustomSetup.vue')
  },
  {
    path: '/dyn-setup/:domain',
    alias: '/dynsetup/:domain',
    name: 'dynSetup',
    component: () => import(/* webpackChunkName: "signup" */ '../views/DynSetup.vue')
  },
  {
    path: '/welcome/:domain?',
    name: 'welcome',
    component: () => import(/* webpackChunkName: "signup" */ '../views/Welcome.vue')
  },
  {
    path: '//desec.readthedocs.io/',
    name: 'docs',
    beforeEnter(to) { location.href = to.path },
  },
  {
    path: '//talk.desec.io/',
    name: 'talk',
    beforeEnter(to) { location.href = to.path },
  },
  {
    path: '/confirm/:action/:code',
    name: 'confirmation',
    component: () => import(/* webpackChunkName: "signup" */ '../views/Confirmation.vue')
  },
  {
    path: '/reset-password/:email?',
    name: 'reset-password',
    component: () => import(/* webpackChunkName: "signup" */ '../views/ResetPassword.vue')
  },
  {
    path: '/donate/',
    name: 'donate',
    component: () => import('../views/Donate.vue')
  },
  {
    path: '/impressum/',
    name: 'impressum',
    component: () => import('../views/Impressum.vue')
  },
  {
    path: '/privacy-policy/',
    name: 'privacy-policy',
    component: () => import('../views/PrivacyPolicy.vue')
  },
  {
    path: '/terms/',
    name: 'terms',
    component: () => import('../views/Terms.vue')
  },
  {
    path: '/about/',
    name: 'about',
    component: () => import('../views/About.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
  },

  /* "manual" table implementation */
  {
    path: '/domains-homebrew',
    name: 'domains-homebrew',
    component: DomainList,
    meta: {guest: false},
  },
  {
    path: '/domains-homebrew/:name',
    name: 'Domain',
    component: Domain,
    meta: {guest: false},
  },

  /* generic table implementation */
  {
    path: '/domains-crud',
    name: 'domains-crud',
    component: CrudDomainList,
    meta: {guest: false},
  },
  {
    path: '/domain-crud/:name',
    name: 'CrudDomain',
    component: CrudDomain,
    meta: {guest: false},
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  scrollBehavior (to, from) {
    // Skip if destination full path has query parameters and differs in no other way from previous
    if (from && Object.keys(to.query).length) {
      if (to.fullPath.split('?')[0] == from.fullPath.split('?')[0]) return;
    }
    return { x: 0, y: 0 }
  },
  routes
})

router.beforeEach((to, from, next) => {
  // see if there are credentials in the session store that we don't know of
  let recovered = false;
  if (sessionStorage.getItem('token') && !store.state.authenticated){
    HTTP.defaults.headers.common['Authorization'] = 'Token ' + sessionStorage.getItem('token');
    store.commit('login', sessionStorage.getItem('token'));
    recovered = true
  }

  if (to.matched.some(record => 'guest' in record.meta && record.meta.guest === false)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (!store.state.authenticated) {
      next({
        name: 'login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    if (store.state.authenticated) {
      // Log in state was present, but not needed for the current page
      if (recovered) {
        // user restored a previous session
        // redirect her to the home page for authorized users
        next({
          name: 'DomainList'
        })
      } else {
        // user navigated to a page that doesn't require auth
        // from within the current session (without session restore)
        // to bias on the safe side we log out
        logout()
      }
    }
    next() // make sure to always call next()!
  }
});

export default router
