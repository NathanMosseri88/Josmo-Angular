import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatOption, MatSelect } from '@angular/material/select';

@Component({
  selector: 'app-preset-options',
  standalone: true,
  imports: [
    CommonModule,
    MatFormField,
    MatSelect,
    MatOption,
    MatLabel
  ],
  templateUrl: './preset-options.component.html',
  styleUrl: './preset-options.component.css'
})
export class PresetOptionsComponent {
  presetOptions = ['ex1', 'ex2', 'ex3']

  handleDropdown(e: any) {
    console.log(e.value)
  }

}
