import React, { Component } from 'react';
import { Textarea, Input, Button, Label } from '@fluentui/react-components';
import { MessageBar, MessageBarType } from '@fluentui/react';
import { MedicationManager } from '../backend/cmd-parser';
// import axios from 'axios';
// import apiService from '../api-service/ApiService';


interface FormState {
    inputValue: string;
    remotePath: string;
    branch: string;
    username: string;
    password: string;
    showMessageBar: boolean;
}

class MyForm extends Component<{}, FormState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      inputValue: '',
      remotePath: 'https://r.danim.space/d/snote-1.git',
      branch: 'master',
      username: '',
      password: '',
      showMessageBar: false,
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);

  }
  async handleSubmit(e: { preventDefault: () => void; }) {
    e.preventDefault();

    try {
        // const response = await axios.post('http://danim.space:8035/log_meds', {
        //   text: this.state.inputValue,
        //   remotePath: this.state.remotePath,
        //   branch: this.state.branch,
        // });
        // console.log(response.data);

        // 使用示例
        const manager = new MedicationManager('data.db', 'data.json');
        manager.logMeds(this.state.inputValue, {
            remote_path: this.state.remotePath,
            local_path: './test_vault_dir',
            username: 'd',
            email: 'danimeon@outlook.com',
            branch: this.state.branch
        });

        console.log('Submitted value:', this.state.inputValue);
        this.setState({ showMessageBar: true });
      } catch (error) {
        console.error(error);
      }
  }

  handleChange(e: { target: { value: any; }; }) {
    this.setState({ inputValue: e.target.value });
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div>
          <Label htmlFor="inputId">远端仓库URL：</Label>
          <Input id="remotePath" name="remotePath" value={this.state.remotePath}></Input>
        </div>
        <div>
          <Label htmlFor="inputId">分支：</Label>
          <Input id="branch" name="branch" value={this.state.branch}></Input>
        </div>
        <div>
          <Label htmlFor="inputId">服药记录命令：</Label>
          <Textarea
          id="comment"
          name="comment"
          value={this.state.inputValue}
          onChange={this.handleChange}
          rows={4}
          cols={50}
          placeholder="示例：tmxt,1 apzl tmxt10"
        ></Textarea>
      </div>
        <Button type="submit">提交</Button>
        {this.state.showMessageBar && (
        <MessageBar
          messageBarType={MessageBarType.success}
          isMultiline={false}
          onDismiss={() => {this.setState({ showMessageBar: false });}}
        >
          提交成功！
        </MessageBar>
      )}
      </form>

      <div dangerouslySetInnerHTML={{ __html: markdown }} />
    );
  }
}

export default MyForm;