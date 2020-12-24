<template>
  <div id="tableInfo">
    <a-row type="flex" justify="start">
      <a-col :span="8">
        <a-spin :spinning="new_table_spinning">
          <a-descriptions
            :bordered="true"
            title="表结构"
            size="small"
            layout="vertical"
            :column="5"
          >
            <a-descriptions-item label="主机">
              {{ new_table_info.db_host }}
            </a-descriptions-item>
            <a-descriptions-item label="类型">
              {{ new_table_info.db_type }}
            </a-descriptions-item>
            <a-descriptions-item label="库名">
              {{ new_table_info.db_name }}
            </a-descriptions-item>
            <a-descriptions-item label="表名">
              {{ new_table_info.table_name }}
            </a-descriptions-item>
            <a-descriptions-item label="更新时间" :span="2">
              {{ new_table_info.update_time }}
            </a-descriptions-item>
          </a-descriptions>
          <br />
          <p style="white-space: pre-wrap;">{{ new_table_info.data }}</p>
        </a-spin>
      </a-col>

      <a-col :span="8">
        <a-spin :spinning="table_column_spinning">
          <a-timeline mode="alternate">
            <div v-for="line in table_column_data" :key="line.batch_md5">
              <a-timeline-item>
                <template #dot>
                  <ClockCircleOutlined style="font-size: 16px;" />
                </template>
                Update Time {{ line.update_time }}
              </a-timeline-item>
              <a-timeline-item
                color="green"
                v-if="check_data(line.add_column_data) === true"
              >
                <a-row
                  v-for="item in line.add_column_data"
                  :key="item.batch_md5"
                >
                  <a-col :span="24" id="add-column-type">
                    {{ item.COLUMN_NAME }}
                    {{ item.COLUMN_TYPE }}
                    COMMENT '{{ item.COLUMN_COMMENT }}'
                  </a-col>
                </a-row>
              </a-timeline-item>

              <a-timeline-item
                color="blue"
                v-if="check_data(line.up_column_data) === true"
              >
                <a-row
                  v-for="item in line.up_column_data"
                  :key="item.batch_md5"
                >
                  <a-col :span="24" id="up-column-type">
                    {{ item.COLUMN_NAME }}
                    {{ item.COLUMN_TYPE }}
                    COMMENT '{{ item.COLUMN_COMMENT }}'
                  </a-col>
                </a-row>
              </a-timeline-item>

              <a-timeline-item
                color="red"
                v-if="check_data(line.del_column_data) === true"
              >
                <a-row
                  v-for="item in line.del_column_data"
                  :key="item.batch_md5"
                >
                  <a-col :span="24" id="del-column-type">
                    {{ item.COLUMN_NAME }}
                    {{ item.COLUMN_TYPE }}
                    COMMENT '{{ item.COLUMN_COMMENT }}'
                  </a-col>
                </a-row>
              </a-timeline-item>
            </div>
          </a-timeline>
        </a-spin>
      </a-col>

      <a-col :span="8"><CommentList></CommentList></a-col>
    </a-row>
  </div>
</template>
<script>
import { tableColumnApi, getTableApi } from "../../api/search";
import { ClockCircleOutlined } from "@ant-design/icons-vue";
import CommentList from "../comment/CommentList";

export default {
  name: "tableInfo",
  components: {
    ClockCircleOutlined,
    CommentList,
  },
  data() {
    return {
      table_input: this.$route.query,
      table_column_data: "",
      new_table_info: {},
      new_table_spinning: false,
      table_column_spinning: false,
    };
  },
  created() {
    this.tableColumnData();
    this.getTableData();
  },
  updated() {},
  methods: {
    check_data(data) {
      if (data === "[]" || data.length === 0) {
        return false;
      }
      return true;
    },
    getTableData() {
      this.new_table_spinning = true;
      getTableApi(this.table_input)
        .then((res) => this.newTableSuccess(res))
        .catch((err) => this.newTableFailed(err))
        .finally(() => {});
    },
    newTableSuccess(res) {
      this.new_table_info = res;
      this.new_table_spinning = false;
    },
    newTableFailed() {
      this.new_table_spinning = false;
    },
    tableColumnData() {
      this.table_column_spinning = true;
      tableColumnApi(this.table_input)
        .then((res) => this.tableColumnSuccess(res))
        .catch((err) => this.tableColumnFailed(err))
        .finally(() => {});
    },
    tableColumnSuccess(res) {
      this.table_column_data = res.data;
      this.table_column_spinning = false;
    },
    tableColumnFailed() {
      this.table_column_spinning = false;
    },
  },
};
</script>

<style>
.ant-descriptions-bordered .ant-descriptions-item-label {
  background-color: #eedbdb;
}
.ant-descriptions-bordered .ant-descriptions-row {
  border-bottom: 1px solid #ccb1b1;
}
.ant-descriptions-bordered .ant-descriptions-view {
  border: 1px solid #e8e0e0;
}
.ant-descriptions-bordered.ant-descriptions-small .ant-descriptions-item-label,
.ant-descriptions-bordered.ant-descriptions-small
  .ant-descriptions-item-content {
  padding: 5px 5px;
}

#add-column-type {
  background: #cdffd8;
  border: 0.5px solid rgb(251, 251, 251);
}

#up-column-type {
  background: #dbedff;
  border: 0.5px solid rgb(251, 251, 251);
}

#del-column-type {
  background: #ffdce0;
  border: 0.5px solid rgb(251, 251, 251);
}
</style>
