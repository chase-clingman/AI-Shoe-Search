<template>
  <q-layout view="hhh lpR fFf">
    <q-header elevated class="bg-white text-black q-pb-md">
      <q-toolbar class="aligned-toolbar">
        <q-toolbar-title style="max-width: 1600px" class="center text-h5">
          <a class="logo-container" href="/">
            <q-img src="logo2.png" style="width: 160px" class="q-ml-xl" />
          </a>
        </q-toolbar-title>

        <!-- Add a q-space to separate title and buttons -->
        <q-space />

        <div class="">
          <!-- Add the home, search property, and broker assistant buttons -->
          <q-btn flat label="Home" to="/" class="q-mx-sm" no-caps />
          <q-btn
            flat
            label="Subscriptions"
            to="/"
            no-caps
            class="q-mx-sm"
          />
          <q-btn
            flat
            label="Contact Us"
            to="/"
            class="q-mx-sm"
            no-caps
          />
        </div>

        <!-- Add a q-space to separate buttons and account icon -->
        <q-space />

        <!-- Add the account icon button -->
        <div class="">
          Log In
          <q-btn flat round dense icon="o_account_circle" no-caps />
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
<script>
import { ref } from "vue";

export default {
  //name: "BookSummaryPage",
  data() {
    return {};
  },
};
</script>
<style>
@import url("https://fonts.googleapis.com/css2?family=Inter&family=Nunito:wght@700&display=swap");
body {
  font-family: "Inter";
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 19px;
}
.center {
  margin: 0 auto;
}
.aligned-toolbar {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}
.logo-container {
  display: flex;
  align-items: flex-end;
  margin-bottom: 8px;
}

</style>
