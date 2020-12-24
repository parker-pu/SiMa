<template>
  <div id="search">
    <a-row type="flex" justify="start">
      <a-col :span="12">
        <!-- <NewTable></NewTable> -->
        <NewTable :new_search_data="new_search_data"></NewTable>
      </a-col>
      <a-col :span="12"> </a-col>
    </a-row>
  </div>
</template>
<script>
import NewTable from "../search/NewTable";

export default {
  name: "search",
  data() {
    return {
      new_search_data: this.$route.query.search,
    };
  },
  components: {
    NewTable,
  },
  created() {},
  updated() {
    this.new_search_data = this.$route.query.search;
  },
  methods: {},
};
</script>
<style></style>
