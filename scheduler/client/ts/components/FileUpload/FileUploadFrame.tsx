import * as React from "react";

import { AppActions } from "../../actions/AppActions";
import { DownloadScheduleButton } from "./DownloadScheduleButton";
import { FileInputForm } from "./FileInputForm";
// import { GenerateScheduleInput } from "./GenerateScheduleInput";
// import { VerifyScheduleInput } from "./VerifyScheduleInput";

export class FileUploadFrame extends React.Component<null, null> {

  public render() {
    return (
      <div>
        <FileInputForm />
      </div>
    );
  }
}
