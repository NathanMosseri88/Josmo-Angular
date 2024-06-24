import { Component } from '@angular/core';
import {MatSelectModule} from '@angular/material/select'
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatCardModule} from '@angular/material/card'
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatCardModule,
    RouterLink,
    RouterLinkActive,
    MatButtonModule,
    ReactiveFormsModule,
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {

  loginFormData: FormGroup
  // initializes the API services to send requests to the flask API
  // initializes Angular reactive forms form group to gather form data from inputs 
  // initializes routing to navigate users to different pages
  constructor(private formBuilder: FormBuilder, private apiService: ApiService, private router: Router) {
    this.loginFormData = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  handleSubmit(e:any){
    this.apiService.login(this.loginFormData.value).subscribe( // sends authorization post request to flask API's user endpoint
      res => { // credentials match and user authorized
        console.log(res)
        sessionStorage.setItem('user', res.access_token) // store user's auth token in browser's session storage
        this.loginFormData.reset() // reset login form data
        this.router.navigate(['/proposal-form']) // send user to proposal form page
      },
      error => {
        console.log(error)
        alert(error.error.error)
      }
    )
  }
}
