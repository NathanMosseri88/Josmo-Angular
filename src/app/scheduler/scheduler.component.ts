import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatFormField } from '@angular/material/form-field';
import { MatInput, MatInputModule } from '@angular/material/input';
import { MatSelect, MatOption } from '@angular/material/select';
import {provideNativeDateAdapter} from '@angular/material/core';
import {MatDatepickerModule} from '@angular/material/datepicker';
import { MatButton, MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-scheduler',
  standalone: true,
  imports: [
    CommonModule,
    MatFormField,
    MatInput,
    MatInputModule,
    MatSelect,
    MatOption,
    MatDatepickerModule,
    MatButtonModule
  ],
  providers: [provideNativeDateAdapter()],
  templateUrl: './scheduler.component.html',
  styleUrl: './scheduler.component.css'
})
export class SchedulerComponent {
  frequency:string = ''

  frequencySelection(value:string) {
    console.log(value)
    this.frequency = value
  }

}
