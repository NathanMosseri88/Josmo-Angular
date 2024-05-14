import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MatFormField, MatFormFieldControl } from '@angular/material/form-field';
import { MatSelect, MatOption } from '@angular/material/select';
import { MatLabel } from '@angular/material/form-field';
import { CommonModule } from '@angular/common';
import { MatInput } from '@angular/material/input';
import {MatCheckboxModule} from '@angular/material/checkbox'
import { MatCardModule } from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button'

@Component({
  selector: 'app-proposal-form',
  standalone: true,
  imports: [
    CommonModule,
    MatFormField,
    MatSelect,
    MatOption,
    MatLabel,
    MatInput,
    ReactiveFormsModule,
    MatCheckboxModule,
    MatCardModule,
    MatButtonModule
  ],
  templateUrl: './proposal-form.component.html',
  styleUrl: './proposal-form.component.css'
})
export class ProposalFormComponent {
  runTypes = ['Size Run']
  viewBy = ['UPC', 'Size']
  pairsCases = ['Pairs', 'Cases']
  includeColumns = ['Price', 'Cost', 'Landed', 'In Stock', 'ATS', 'Incoming', 'Brand', 'Descript', 'Note']
  stockFilters = ['In Stock Only', 'Include 0 Quantities']
  statuses = ['Active']

  formData: FormGroup

  constructor(private formBuilder: FormBuilder) {
    this.formData = this.formBuilder.group({
      type: ['', Validators.nullValidator],
      view: ['', Validators.required],
      pC: ['', Validators.required],
      columns: [[], Validators.required],
      filters: ['', Validators.required],
      status: ['', Validators.required],
      filename: ['', Validators.required],
    });
  }
  handleStateChange(type: string, value: string){
    console.log(this.formData.value[type])
  }

  handleSubmit(e:any){
    console.log(this.formData.value)
  }

  handleCancel(){
    this.formData.reset()
  }

}
