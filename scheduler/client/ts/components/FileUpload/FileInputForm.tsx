import * as React from "react";

import { AppActions } from "../../actions/AppActions";

import { FileUploadFormStore, IFileUploadFormStoreState } from "../../stores/FileUploadFormStore";

import { DownloadScheduleButton } from "./DownloadScheduleButton";
import { FileInputSubmitButton } from "./FileInputSubmitButton";
import { FileUploadMode } from "./FileUploadMode";
import { SemesterSelect } from "./SemesterSelect";

function timestampToString(timestamp: string) {
  const date = new Date(parseInt(timestamp, 10));

  const month = date.getMonth() + 1;
  const day = date.getDate();
  const year = date.getFullYear();
  const hour = date.getHours();
  const minutes = date.getMinutes();
  const seconds = date.getSeconds();

  const monthStr = month < 10 ? "0" + month : month;
  const dayStr = day < 10 ? "0" + day : day;
  const hourStr = hour < 10 ? "0" + hour : hour;
  const minutesStr = minutes < 10 ? "0" + minutes : minutes;
  const secondsStr = seconds < 10 ? "0" + seconds : seconds;

  const timeString = monthStr + "/"
    + dayStr + "/"
    + year + " @ "
    + hourStr + ":"
    + minutesStr + ":"
    + secondsStr;
  return timeString;
}

export class FileInputForm extends React.Component<null, IFileUploadFormStoreState> {

  constructor(props: any) {
    super(props);
    this.onChange = this.onChange.bind(this);
  }

  public componentWillMount() {
    this.setState(FileUploadFormStore.getState());
  }

  public componentDidMount() {
    FileUploadFormStore.listen(this.onChange);

    // Load filestyle manually here
    const style = {text: "Choose File", buttonBefore: true, placeholder: ""};

    style.placeholder = this.state.coursesFileName === null ? "" : this.state.coursesFileName;
    ($("#vs-courses-input-id") as any).filestyle(style);

    style.placeholder = this.state.peopleFileName === null ? "" : this.state.peopleFileName;
    ($("#vs-people-input-id") as any).filestyle(style);

    style.placeholder = this.state.facultyFileName === null ? "" : this.state.facultyFileName;
    ($("#vs-faculty-input-id") as any).filestyle(style);
  }

  public componentWillUnmount() {
    FileUploadFormStore.unlisten(this.onChange);
  }

  public onChange(state: IFileUploadFormStoreState) {
    this.setState(state);
  }

  public onSubmit(e: any) {
    e.preventDefault();
    const fileInputForm = (new FormData(($("#file-input-id")[0] as HTMLFormElement)) as any);

    // Add the files from local storage
    const coursesText = FileUploadFormStore.getCoursesFile();
    const coursesBlob = new Blob([coursesText], {type: "text/csv"});
    const peopleText = FileUploadFormStore.getPeopleFile();
    const peopleBlob = new Blob([peopleText], {type: "text/csv"});
    const facultyText = FileUploadFormStore.getFacultyFile();
    const facultyBlob = new Blob([facultyText], {type: "text/csv"});

    fileInputForm.set("courses", coursesBlob);
    fileInputForm.set("people", peopleBlob);
    fileInputForm.set("faculty", facultyBlob);

    // Get the semester mode
    const semester = $("#semester-select-id input:radio:checked").val();
    if (semester === "fall") {
      fileInputForm.set("semester", "FALL");
    } else if (semester === "spring") {
      fileInputForm.set("semester", "SPRING");
    }

    const mode = $("#file-upload-mode-id input:radio:checked").val();
    if (mode === "check") {
      AppActions.checkSchedule(fileInputForm);
    } else if (mode === "generate") {
      AppActions.generateSchedule(fileInputForm);
    }
  }

  public onClickGenerator(id: string, resetAction: any) {
    return (e: any) => {

      // Reset the input
      const input = ($("#" + id) as any);
      input.val("");
      input.filestyle("placeholder", "");
      input.filestyle("clear");

      // Send an action to the store to reset
      resetAction();
    };
  }

  public onChangeGenerator(id: string, updateAction: any, resetAction: any) {

    if (typeof Storage === "undefined") {
      return (e: any) => {
        return;
      };
    }

    // Return a function that will store the file in local storage
    return (e: any) => {

      if (e.target.files[0] === undefined) {
        // Reset in local storage if no file selected
        resetAction();
        return;
      }
      // Update the file in local storage
      const file = e.target.files[0];
      updateAction(file);
    };
  }

  public render() {
    return (
      <div>
        <form
          id="file-input-id"
          action="/verifySchedule"
          method="post"
          encType="multipart/form-data"
          onSubmit={this.onSubmit}
        >
          <div className="row">
            <FileUploadMode />
            <div className="text-right">
              <SemesterSelect />
            </div>
          </div>

          <div className="form-group">
            <label><b>Schedule</b></label>
            <input
              id="vs-courses-input-id"
              type="file"
              className="filestyle"
              name="courses"
              data-placeholder={this.state.coursesFileName === null ? "" : this.state.coursesFileName}
              onClick={this.onClickGenerator("vs-courses-input-id", AppActions.resetCourses)}
              onChange={this.onChangeGenerator("vs-courses-input-id", AppActions.updateCourses,
                AppActions.resetCourses)}
            />
            <label className="lb-sm">
              {this.state.coursesLastUploaded === null ? "" : "Last uploaded: " +
              timestampToString(this.state.coursesLastUploaded)}
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="vs-people-input-id"><b>TA Preferences</b></label>
            <input
              id="vs-people-input-id"
              type="file"
              className="filestyle"
              name="people"
              data-placeholder={this.state.peopleFileName === null ? "" : this.state.peopleFileName}
              onClick={this.onClickGenerator("vs-people-input-id", AppActions.resetPeople)}
              onChange={this.onChangeGenerator("vs-people-input-id", AppActions.updatePeople,
                AppActions.resetPeople)}
            />
            <label className="lb-sm">
              {this.state.peopleLastUploaded === null ? "" : "Last uploaded: " +
              timestampToString(this.state.peopleLastUploaded)}
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="vs-faculty-input-id"><b>Faculty Hours</b></label>
            <input
              id="vs-faculty-input-id"
              type="file"
              className="filestyle"
              name="faculty"
              data-placeholder={this.state.facultyFileName === null ? "" : this.state.facultyFileName}
              onClick={this.onClickGenerator("vs-faculty-input-id", AppActions.resetFaculty)}
              onChange={this.onChangeGenerator("vs-faculty-input-id", AppActions.updateFaculty,
                AppActions.resetFaculty)}
            />
            <label className="lb-sm">
              {this.state.facultyLastUploaded === null ? "" : "Last uploaded: " +
              timestampToString(this.state.facultyLastUploaded)}
            </label>
          </div>

          <FileInputSubmitButton />
          <DownloadScheduleButton />

        </form>
      </div>
    );
  }
}
