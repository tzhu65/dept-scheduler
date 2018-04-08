import * as React from "react";

import { UploadFiles } from "./FileUpload/UploadFiles";
import { GenerateScheduleInput } from "./FileUpload/GenerateScheduleInput";

export class Frame extends React.Component<null, null> {
  public render() {
    return (
      <div>
        Test Component
        <UploadFiles />
        <br />
        <GenerateScheduleInput />
      </div>
    );
  }
}
