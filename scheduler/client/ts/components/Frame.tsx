import * as React from "react";

import { UploadFiles } from "./FileUpload/UploadFiles";

export class Frame extends React.Component<null, null> {
  public render() {
    return (
      <div>
        Test Component
        <UploadFiles />
      </div>
    );
  }
}
