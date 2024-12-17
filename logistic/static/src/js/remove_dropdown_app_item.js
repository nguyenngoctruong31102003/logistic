/** @odoo-module **/
import { NavBar } from "@web/webclient/navbar/navbar";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { onWillStart, useState, onMounted } from "@odoo/owl";

const systrayRegistry = registry.category("systray");
patch(NavBar.prototype, {
  setup() {
    super.setup();
    this.menuService = useService("menu");
    this.actionService = useService("action");
    this.user = useService("user");
    this.state = useState({
      UserPOS: false,
      Client: false,
      usename: "2",
    });

    onWillStart(async () => {
      // Kiểm tra nếu người dùng là ERP Manager
      if (await this.user.hasGroup("base.group_erp_manager")) {
        return;
      }
      // Kiểm tra nếu người dùng thuộc nhóm User POS
      let investor = await this.user.hasGroup("logistic.group_user_pos");
      console.log(investor);

      // Gán trạng thái nếu thuộc nhóm User POS
      if (investor) this.state.UserPOS = true;
      // ---------------------------------------------

      // Kiểm tra nếu người dùng thuộc nhóm Client
      let clients = await this.user.hasGroup("logistic.group_client");
      console.log(clients);

      // Gán trạng thái nếu thuộc nhóm Client
      if (clients) this.state.Client = true;
    });
  },

});
