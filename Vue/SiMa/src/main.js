import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import {
    Button,
    Row,
    Col,
    Table,
    Form,
    Input,
    Tabs,
    Layout,
    Breadcrumb,
    Menu,
    Avatar,
    Dropdown,
    Drawer,
    Statistic,
    Tag,
    Popconfirm,
    Modal,
    Select,
    Spin,
    Radio,
    Space,
    Descriptions,
    List,
    Collapse,
    Timeline,
    Tooltip,
    Comment,
    Switch,
} from 'ant-design-vue';

import { message,notification } from 'ant-design-vue'


const app = createApp(App);
app.use(router);
app.use(store);

// ant
app.use(Button);
app.use(Row);
app.use(Col);
app.use(Table);
app.use(Form);
app.use(Input);
app.use(Tabs);
app.use(Layout);
app.use(Breadcrumb);
app.use(Menu);
app.use(Avatar);
app.use(Dropdown);
app.use(Drawer);
app.use(Statistic);
app.use(Tag);
app.use(Popconfirm);
app.use(Modal);
app.use(Select);
app.use(Spin);
app.use(Radio);
app.use(Space);
app.use(Descriptions);
app.use(List);
app.use(Collapse);
app.use(Timeline);
app.use(Tooltip);
app.use(Comment);
app.use(Switch);

app.config.globalProperties.$message = message;
app.config.globalProperties.$notification = notification;

app.mount("#app");

app.config.productionTip = false
