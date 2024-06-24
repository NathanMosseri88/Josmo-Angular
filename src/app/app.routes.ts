import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { ProposalFormComponent } from './proposal-form/proposal-form.component';
import { SignupComponent } from './signup/signup.component';
import { ComparativeStyleComponent } from './comparative-style/comparative-style.component';

export const routes: Routes = [
    {path: 'login', component: LoginComponent},
    {path: 'signup', component: SignupComponent},
    {path: 'proposal-form', component: ProposalFormComponent},
    {path: 'styles-report', component: ComparativeStyleComponent},
    {path: '', component: HomeComponent},
    {path: '**', component: NotFoundComponent}
];
