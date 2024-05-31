import { Component } from '@angular/core';
import { ProposalFormComponent } from '../proposal-form/proposal-form.component';
import { MatTableModule } from '@angular/material/table'
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatInput } from '@angular/material/input';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-style-selection',
  standalone: true,
  imports: [
    CommonModule,
    ProposalFormComponent,
    MatTableModule,
    MatFormField,
    MatLabel,
    MatInput,
    ReactiveFormsModule
  ],
  templateUrl: './style-selection.component.html',
  styleUrl: './style-selection.component.css'
})
export class StyleSelectionComponent {
  // columnsToDisplay = ['Styles']
  // rowData = ['']

  // styleFormData: FormGroup

  // constructor(private formBuilder: FormBuilder){
  //   this.styleFormData = this.formBuilder.group({
  //     styles: [[], Validators.nullValidator]
  //   })
  // }

  // handleStyleInput(){
  //   console.log(this.styleFormData.value)
  //   if(this.styleFormData.value > 1){
  //     this.rowData.push('')
  //   }
  // }
  rows: string[] = [''];

  handlePaste(event: ClipboardEvent): void {
    if (!event.clipboardData){
      return;
    }
    const clipboardData = event.clipboardData;
    const pastedText = clipboardData.getData('text');
    const pastedRows = pastedText.split('\n');

    this.rows = pastedRows.map(row => row.trim());
  }

  addRow(): void {
    this.rows.push('');
  }

}
