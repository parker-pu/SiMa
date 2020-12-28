<template>
  <div id="">
    <a-button type="primary" shape="round" size="small" @click="addComment">
      <template #icon><PlusCircleTwoTone />增加评论</template>
    </a-button>

    <!-- 评论 -->
    <a-spin :spinning="spinning">
      <a-list
        class="comment-list"
        header=""
        item-layout="horizontal"
        :data-source="comment_data"
      >
        <template #renderItem="{ item, }">
          <a-list-item>
            <a-comment
              :author="item.comment_main.author"
              :avatar="item.comment_main.avatar"
            >
              <template #actions>
                <span v-for="action in item.comment_main.actions" :key="action">
                  {{ action }}
                </span>
                <a-popconfirm
                  title="确定删除?"
                  ok-text="是"
                  cancel-text="否"
                  @confirm="delComment(item)"
                  @cancel="cancel"
                >
                  <a href="#">删除</a>
                </a-popconfirm>
              </template>
              <template #content>
                <p>
                  {{ item.comment_main.content }}
                </p>
              </template>

              <template #datetime>
                <a-tooltip :title="item.update_time">
                  <span>{{ item.update_time }}</span>
                </a-tooltip>
              </template>
            </a-comment>
          </a-list-item>
        </template>
      </a-list>
    </a-spin>

    <!-- 用户数据 -->
    <a-modal v-model:visible="visible" :title="edidTitle" @ok="handleOk">
      <template #footer>
        <a-button key="back" @click="handleCancel">
          取消
        </a-button>
        <a-button key="back" @click="resetCancel">
          重置
        </a-button>
        <a-button
          key="submit"
          type="primary"
          :loading="loading"
          @click="handleOk"
        >
          提交
        </a-button>
      </template>
      <a-form
        :model="addCommForm"
        :label-col="labelCol"
        :wrapper-col="wrapperCol"
        layout="vertical"
      >
        <a-form-item label="评论" name="content">
          <a-textarea v-model:value="addCommForm.content" />
          <!-- <a-input v-model:value="addCommForm.content"></a-input> -->
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>
<script>
import { getCommentApi, putCommentApi, delCommentApi } from "../../api/comment";
import moment from "moment";
import { PlusCircleTwoTone } from "@ant-design/icons-vue";

export default {
  name: "commentList",
  components: {
    PlusCircleTwoTone
  },
  data() {
    return {
      action: null,
      moment,
      visible: false,
      addDBForm: {},
      confirmLoading: false,
      edidTitle: "增加评论",
      labelCol: { span: 4 },
      wrapperCol: { span: 24 },
      loading: false,
      addCommForm: {
        content: null
      },
      table_input: this.$route.query,
      spinning: false,
      comment_data: []
    };
  },
  created() {
    this.table_input = this.$route.query;
    this.getCommentList();
  },
  updated() {
    this.table_input = this.$route.query;
  },
  methods: {
    addComment() {
      this.visible = true;
    },

    handleCancel() {
      this.visible = false;
    },
    resetCancel() {
      this.addCommForm = {};
    },
    handleOk() {
      this.loading = true;
      putCommentApi(this.addCommForm, this.table_input)
        .then(res => this.addSuccess(res))
        .catch(err => this.addFailed(err))
        .finally(() => {});
    },
    addSuccess() {
      this.$notification.success({
        message: "成功",
        description: "添加成功"
      });

      // off
      this.loading = false;
      this.visible = false;

      this.getCommentList();
    },
    addFailed() {
      // off
      this.loading = false;
      this.visible = false;
    },

    // list comment
    getCommentList() {
      this.spinning = true;
      setTimeout(() => {
        getCommentApi(this.table_input)
          .then(res => this.getCommentSuccess(res))
          .catch(() => (this.spinning = false))
          .finally(() => {});
      }, 1000);
    },
    getCommentSuccess(res) {
      this.comment_data = res.data;
      // off
      this.spinning = false;
    },

    delComment(line) {
      console.log(line);
      delCommentApi(line)
        .then(res => this.getCommentList(res))
        .catch()
        .finally(() => {});
    },

    cancel() {}
  }
};
</script>

<style></style>
