/** @odoo-module **/
import {
  EventBus,
  Component,
  onWillStart,
  onMounted,
  markup,
  useState,
} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class CameraCaptureField extends Component {
  setup() {
    this.state = useState({cameraVideos: false });
    this.notification = useService("notification");
    this.rpc = useService("rpc");
    this.user = useService("user");
    this.orm = useService("orm");
    onWillStart(async () => await this.initialize());

    onMounted(() => {
      const self = this;
      self.state.cameraVideos = document.querySelectorAll("video");
      let availableDevices = [];

      // Lấy danh sách các thiết bị camera
      async function getVideoDevices() {
        try {
          const devices = await navigator.mediaDevices.enumerateDevices();
          availableDevices = devices.filter(
            (device) => device.kind === "videoinput"
          );

          // Gán webcam mặc định cho camera1
          // if (availableDevices.length > 0) {
          //   const camera1Device = availableDevices[0].deviceId;
          //   initializeCamera(self.state.cameraVideos[0], camera1Device);
          // }

          // Gán các camera còn lại cho các video tiếp theo
          self.state.cameraVideos.forEach((videoElement, index) => {
            if (availableDevices[index]) {
              const deviceId = availableDevices[index].deviceId;
              initializeCamera(videoElement, deviceId);
            }
          });
        } catch (error) {
          console.error("Lỗi khi lấy danh sách camera:", error);
        }
      }

      // Khởi tạo stream cho từng video
      async function initializeCamera(videoElement, deviceId) {
        try {
          // Dừng stream cũ nếu có
          const existingStream = videoElement.srcObject;
          if (existingStream) {
            existingStream.getTracks().forEach((track) => track.stop());
          }

          // Khởi tạo stream mới
          const constraints = {
            video: { deviceId: deviceId ? { exact: deviceId } : undefined },
          };

          const stream = await navigator.mediaDevices.getUserMedia(constraints);
          videoElement.srcObject = stream;
        } catch (error) {
          console.error("Lỗi khi khởi tạo camera:", error);
        }
      }

      function stopCameras() {
        self.state.cameraVideos.forEach((video) => {
          if (video.srcObject) {
            video.srcObject.getTracks().forEach((track) => track.stop());
          }
        });
      }

      // Xử lý khi mở modal
      document
        .getElementById("cameraModal")
        .addEventListener("show.bs.modal", async () => {
          await getVideoDevices();
        });

      // Xử lý khi đóng modal
      document
        .getElementById("cameraModal")
        .addEventListener("hide.bs.modal", stopCameras);
    });
  }

  // Hiển thị thông báo
  showNotification(content, title, type) {
    const notification = this.notification;
    notification.add(content, {
      title: title,
      type: type,
      className: "p-4",
    });
  }
  async onCapture() {
    let imagesData = [];
    this.state.cameraVideos.forEach((element) => {
      element.pause();
      const canvas = document.createElement("canvas");
      canvas.width = element.videoWidth;
      canvas.height = element.videoHeight;
      const context = canvas.getContext("2d");
      context.drawImage(element, 0, 0, canvas.width, canvas.height);

      // Convert canvas to base64 image
      const imageBase64 = canvas.toDataURL("image/jpeg");

      // Remove the data URL prefix for Odoo
      const base64Image = imageBase64.split(",")[1];
      imagesData.push(base64Image);
    });
    console.log(this);
    // Save image to the current record's image field
    await this.props.record.update(
      {
        image_1920_1: imagesData[0],
        image_1920_2: imagesData[1],
        image_1920_3: imagesData[2],
        image_1920_4: imagesData[3],
      },
      { save: true }
    );

    setTimeout(() => {
      this.state.cameraVideos.forEach((element) => {
        element.play();
      });
    }, 3000);

    this.showNotification(`Đã chụp hình!`, "Thành Công", "success");
  }
  onReset() {
    this.state.cameraVideos.forEach((element) => {
      element.play();
    });
    this.showNotification(`Đã reset!`, "Thành Công", "info");
  }
  async initialize() {}
}

CameraCaptureField.template = "camera.capture";

export const cameraCapture = {
  component: CameraCaptureField,
  displayName: _t("Capture"),
  useSubView: true,
  supportedTypes: ["boolean"],
  supportedOptions: [],
  extractProps: ({ attrs, options }) => ({}),
};

registry.category("fields").add("camera.capture", cameraCapture);
