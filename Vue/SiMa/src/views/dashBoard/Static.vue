<template>
  <div style="background: #ECECEC; padding: 30px">
    <a-row :gutter="16">
      <a-col :span="12">
        <a-card>
          <a-statistic
            title="数据库"
            :value="static_data.scan_conn_db_setting.total_nums"
            style="margin-right: 50px"
          >
            <template #prefix>
              <DatabaseOutlined />
            </template>
          </a-statistic>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card>
          <a-statistic
            title="扫描的表"
            :value="static_data.new_table.total_nums"
            class="demo-class"
            :value-style="{ color: 'rgb(26, 193, 139)' }"
          >
            <template #prefix>
              <TableOutlined />
            </template>
          </a-statistic>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>
<script>
import { getStatisApi } from "../../api/dashBoard";
import { TableOutlined, DatabaseOutlined } from "@ant-design/icons-vue";

export default {
  name: "static",
  components: {
    TableOutlined,
    DatabaseOutlined
  },
  created() {
    this.getSattic();
  },
  data() {
    return {
      static_data: {
        scan_conn_db_setting: {},
        new_table: {}
      }
    };
  },
  methods: {
    getSattic() {
      getStatisApi()
        .then(rsp => {
          this.static_data = rsp;
        })
        .catch(() => {});
    }
  }
};
</script>
<style></style>
