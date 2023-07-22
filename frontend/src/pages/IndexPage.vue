<template>
  <!-- Main container with flex and center alignment -->
  <q-page class="row items-start justify-center top-content" padding>
    <div class="column" style="width: 100%; max-width: 1200px">
      <!-- Add this wrapper div -->
      <!-- Display the text search mode message -->
      <div class="text-center">
        <q-img src="logo.png" style="width: 300px" class="q-ml-xl" />
      </div>
      <div class="hero q-mt-md">
        Take A Step Ahead in Style, Find Your Sole Mate.
      </div>
      <!-- Display the image search mode message -->
      <!-- <div v-if="model === 'image'" class="hero q-ma-lg">
        Find Your Home
      </div> -->
      <!-- <div class="heroSub q-my-md">
        We'd love to hear what you're on the lookout for!
      </div> -->
      <!-- Toggle button for switching between text and image search modes -->
      <div class="text-center q-mt-lg">
        <q-btn
          flat
          class="my-custom-button"
          :class="{ active: model === 'text' }"
          color="transparent"
          text-color="black"
          @click="model = 'text'"
        >
          ENTER TEXT CRITERIA
        </q-btn>
        <q-btn
          flat
          class="my-custom-button"
          :class="{ active: model === 'image' }"
          color="transparent"
          text-color="black"
          @click="model = 'image'"
        >
          UPLOAD INSPIRATION IMAGE
        </q-btn>
      </div>

      <!-- Conditionally render the text search component -->
      <text-search v-if="model === 'text'" :search-text="searchText" />
      <!-- Conditionally render the image uploader component -->
      <image-uploader v-if="model === 'image'" />
    </div>
  </q-page>
</template>

<script>
// Import the required components
import ImageUploader from "components/ImageUploader.vue";
import TextSearch from "components/TextSearch.vue";

export default {
  // Initialize the data properties
  data() {
    return {
      model: "text",
      showContent: true,

      searchText: "", // Add this line
    };
  },
  // Register the imported components
  components: {
    ImageUploader,
    TextSearch,
  },
};
</script>
<style>
/* Import the Roboto font from Google Fonts */
@import url("https://fonts.googleapis.com/css2?family=Inter&family=Nunito:wght@700&display=swap");
body {
  /* gradient from grey to black top to bottom - This comment suggests that a gradient should be applied to the body, but the actual gradient CSS code is missing */
}
/* Define styles for the hero text */
.top-content {
  margin-top: 2em;
}
.hero {
  /*
  position: absolute;
  width: 991px;
  height: 49px;
  left: 242px;
  top: 142px;

  font-family: 'Avenir';
  font-style: normal;
  font-weight: 800;
  font-size: 36px;
  line-height: 49px;
  display: flex;
  align-items: center;


  color: #343A40;

  CHANGE FONT FAMILY
*/
  font-family: "Inter", sans-serif;
  font-style: normal;
  font-weight: 800;
  font-size: 36px;
  line-height: 49.18px;

  align-items: center;
  text-align: center;

  color: #343a40;
}
.heroSub {
  font-family: "Lato";
  font-style: normal;
  font-weight: 400;
  font-size: 24px;
  line-height: 29px;
  /* identical to box height */

  display: flex;
  align-items: center;

  /* Text Gray 2 */

  color: #6c757d;
}

.my-custom-button {
  margin-top: 2em;
  padding: 5px 40px; /* Adjust this value according to your needs */
  text-transform: none;
  color: black;
  border: none;
  background-color: transparent;
  font-family: "Lato";
  font-style: normal;
  font-weight: 700;
  font-size: 14px;
  line-height: 17px;

  color: #6c757d;
}

.my-custom-button.active {
  border-bottom: 3px solid #f04845b2;
}

.expansion {
  font-family: "Inter", sans-serif;
  font-style: normal;
  font-weight: 500;
  font-size: 24px;
  line-height: 33px;
  /* identical to box height */
  align-items: center;

  /* Text Gray 1 */

  color: #343a40;
}
.rotate-180 {
  transform: rotate(180deg);
}

.expansionArrow {
  color: #6c757d;
}
.expansionSep {
  border-bottom: 0.5px solid #6c757d;
  margin-bottom: 30px;
}
.expansionCard {
  width: 311px;
  height: 260px;
  background: #f8f9fa;
  border-radius: 3px;
  padding: 10px;
  padding-top: 0;
  cursor: pointer;
  transition: all 0.5s;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0); /* Add initial state of box-shadow */
}

.expansionCard:hover {
  transform: scale(1.02); /* slightly scale up the card */
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); /* Add a subtle shadow */
}

.cardIcon {
  /* Gray3 */
  margin-bottom: 20px;
  color: #adb5bd;

  align-items: center;
  text-align: center;
}
.cardTitle {
  /* Feature Based */
  font-family: "Inter", sans-serif;
  font-style: normal;
  font-weight: 500;
  font-size: 21px;
  line-height: 29px;
  /* identical to box height */

  align-items: center;
  text-align: center;
  /* Text Gray 1 */

  color: #343a40;
  margin-bottom: 10px;
}
.cardExample {
  font-family: "Lato";
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 19px;
  display: flex;
  align-items: center;
  text-align: center;

  /* Text Gray 2 */

  color: #6c757d;
}
.cardArrow {
  /* Gray3 */
  margin-bottom: 20px;
  color: #adb5bd;

  align-items: center;
  text-align: center;
}
.cards-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
