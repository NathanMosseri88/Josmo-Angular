import { Component } from '@angular/core';
import {MatSelectModule} from '@angular/material/select'
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatCardModule} from '@angular/material/card'
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatCardModule,
    RouterLink,
    RouterLinkActive,
    MatButtonModule,
    ReactiveFormsModule
  ],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent {

  signupFormData: FormGroup
  constructor(private formBuilder: FormBuilder, private apiService:ApiService) {
    this.signupFormData = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      email: ['', Validators.required]
    });
  }
  
  handleSubmit(e:any){
    console.log(this.signupFormData)
    let token = sessionStorage.getItem('user') 
    if(!token){
      alert('Please log in')
      return
    }
    this.apiService.signup(this.signupFormData.value, token).subscribe(
      res => { 
        console.log(res)
        this.signupFormData.reset() 
        alert(`User created with username: ${res.username}`)
      },
      error => {
        console.log(error)
        alert(error.error.error)
      }
    )
  }
}
