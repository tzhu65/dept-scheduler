import * as React from "react";

declare let jQuery: any;
let $ = jQuery;

export class UploadFiles extends React.Component<null, null> {

  public onSubmit(e: any) {
    e.preventDefault();
    console.log("hello");
    console.log(e);
    // console.log($("#verify-schedule-id").serialize());
    // console.log($("#verify-schedule-id"))
    // console.log($(this).serialize());
    console.log(document.getElementById("file-select").files);
  }

  public render() {
    return (
      <form
        id="verify-schedule-id"
        action="/verifySchedule"
        method="post"
        encType="multipart/form-data"
        onSubmit={this.onSubmit.bind(this)}
      >
        Select image to upload:
        <input id="file-select" type="file" name="fileToUpload" />
        <input type="submit" value="Upload Image" name="submit" />
      </form>
    );
  }
}
