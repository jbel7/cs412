# File: voter_analytics/views.py
# Name: Jed Belsany
# BU email: belsanyj@bu.edu
# Description: Views for voter analytics application inclding list and detail views with filtering 

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Q
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
# Create your views here.

class VoterListView(ListView):
    """
    View to display a paginated list of voters with filtering options.
    
    Provides filtering by party affiliation, birth year range, voter score,
    and specific election participation.
    """
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        """
        Get the filtered queryset of voters based on query parameters.
        
        Returns:
            QuerySet: Filtered set of Voter objects
        """
        queryset = Voter.objects.all()
        
        # Filter by party affiliation
        party = self.request.GET.get('party_affiliation')
        if party:
            queryset = queryset.filter(party_affiliation=party)
        
        # Filter by minimum birth year
        min_year = self.request.GET.get('min_birth_year')
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
        
        # Filter by maximum birth year
        max_year = self.request.GET.get('max_birth_year')
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
        
        # Filter by voter score
        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        
        # Filter by specific elections
        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template including filter options.
        
        Parameters:
            **kwargs --> Additional keyword arguments
            
        Returns:
            dict --> Context dictionary with filter options and current values
        """
        context = super().get_context_data(**kwargs)
        
        # Get unique party affiliations
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        
        # Generate birth year range (from min to max in database)
        min_year = Voter.objects.order_by('date_of_birth').first().date_of_birth.year if Voter.objects.exists() else 1900
        max_year = Voter.objects.order_by('-date_of_birth').first().date_of_birth.year if Voter.objects.exists() else 2024
        context['birth_years'] = range(min_year, max_year + 1)
        
        # Voter scores (0-5)
        context['voter_scores'] = range(0, 6)
        
        # Pass current filter values back to template
        context['current_party'] = self.request.GET.get('party_affiliation', '')
        context['current_min_year'] = self.request.GET.get('min_birth_year', '')
        context['current_max_year'] = self.request.GET.get('max_birth_year', '')
        context['current_voter_score'] = self.request.GET.get('voter_score', '')
        context['current_v20state'] = self.request.GET.get('v20state', '')
        context['current_v21town'] = self.request.GET.get('v21town', '')
        context['current_v21primary'] = self.request.GET.get('v21primary', '')
        context['current_v22general'] = self.request.GET.get('v22general', '')
        context['current_v23town'] = self.request.GET.get('v23town', '')
        
        return context


class VoterDetailView(DetailView):
    """
    View to display detailed information about a single voter.
    
    Shows all voter information including full voting history and
    provides a link to Google Maps for the voter's address.
    """
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'
    
    def get_context_data(self, **kwargs):
        """
        Add Google Maps URL to context.
        
        Parameters:
            **kwargs: Additional keyword arguments
            
        Returns:
            dict: Context dictionary with Google Maps URL
        """
        context = super().get_context_data(**kwargs)
        voter = self.object
        
        # Create Google Maps URL
        address = f"{voter.street_number} {voter.street_name}, Newton, MA {voter.zip_code}"
        context['google_maps_url'] = f"https://www.google.com/maps/search/?api=1&query={address.replace(' ', '+')}"
        
        return context
    
class GraphsView(ListView):
    """
    View to display graphs of voter data with filtering options.
    
    Generates three graphs using Plotly:
    1. Histogram of voters by year of birth
    2. Pie chart of voters by party affiliation
    3. Bar chart of voter participation by election
    """
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    
    def get_queryset(self):
        """
        Get the filtered queryset of voters based on query parameters.
        Reuses the same filtering logic as VoterListView.
        
        Returns:
            QuerySet: Filtered set of Voter objects
        """
        queryset = Voter.objects.all()
        
        # Filter by party affiliation
        party = self.request.GET.get('party_affiliation')
        if party:
            queryset = queryset.filter(party_affiliation=party)
        
        # Filter by minimum birth year
        min_year = self.request.GET.get('min_birth_year')
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
        
        # Filter by maximum birth year
        max_year = self.request.GET.get('max_birth_year')
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
        
        # Filter by voter score
        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        
        # Filter by specific elections
        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Add graph visualizations and filter options to context.
        
        Parameters:
            **kwargs: Additional keyword arguments
            
        Returns:
            dict: Context dictionary with graph HTML and filter options
        """
        context = super().get_context_data(**kwargs)
        
        # Get filtered voters
        voters = self.get_queryset()
        
        # Graph 1: Histogram of voters by year of birth
        birth_years = [voter.date_of_birth.year for voter in voters]
        year_counts = Counter(birth_years)
        
        fig1 = go.Figure(data=[
            go.Bar(
                x=sorted(year_counts.keys()),
                y=[year_counts[year] for year in sorted(year_counts.keys())],
                marker_color='#6B7FFF'
            )
        ])
        fig1.update_layout(
            title=f'Voter distribution by Year of Birth (n={len(voters)})',
            xaxis_title='Year of Birth',
            yaxis_title='Count',
            plot_bgcolor='#E8ECEF',
            paper_bgcolor='white',
            font=dict(size=14)
        )
        context['birth_year_graph'] = fig1.to_html(full_html=False)
        
        # Graph 2: Pie chart of voters by party affiliation
        party_counts = Counter([voter.party_affiliation for voter in voters])
        
        fig2 = go.Figure(data=[
            go.Pie(
                labels=list(party_counts.keys()),
                values=list(party_counts.values()),
                textposition='inside',
                textinfo='percent+label'
            )
        ])
        fig2.update_layout(
            title=f'Voter distribution by Party Affiliation (n={len(voters)})',
            font=dict(size=14)
        )
        context['party_affiliation_graph'] = fig2.to_html(full_html=False)
        
        # Graph 3: Bar chart of voter participation by election
        elections = {
            'v20state': sum(1 for v in voters if v.v20state),
            'v21town': sum(1 for v in voters if v.v21town),
            'v21primary': sum(1 for v in voters if v.v21primary),
            'v22general': sum(1 for v in voters if v.v22general),
            'v23town': sum(1 for v in voters if v.v23town),
        }
        
        fig3 = go.Figure(data=[
            go.Bar(
                x=list(elections.keys()),
                y=list(elections.values()),
                marker_color='#6B7FFF'
            )
        ])
        fig3.update_layout(
            title=f'Vote Count by Election (n={len(voters)})',
            xaxis_title='Election',
            yaxis_title='Number of Voters',
            plot_bgcolor='#E8ECEF',
            paper_bgcolor='white',
            font=dict(size=14)
        )
        context['election_participation_graph'] = fig3.to_html(full_html=False)
        
        # Add filter options (reuse from VoterListView)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        
        min_year = Voter.objects.order_by('date_of_birth').first().date_of_birth.year if Voter.objects.exists() else 1900
        max_year = Voter.objects.order_by('-date_of_birth').first().date_of_birth.year if Voter.objects.exists() else 2024
        context['birth_years'] = range(min_year, max_year + 1)
        
        context['voter_scores'] = range(0, 6)
        
        # Pass current filter values back to template
        context['current_party'] = self.request.GET.get('party_affiliation', '')
        context['current_min_year'] = self.request.GET.get('min_birth_year', '')
        context['current_max_year'] = self.request.GET.get('max_birth_year', '')
        context['current_voter_score'] = self.request.GET.get('voter_score', '')
        context['current_v20state'] = self.request.GET.get('v20state', '')
        context['current_v21town'] = self.request.GET.get('v21town', '')
        context['current_v21primary'] = self.request.GET.get('v21primary', '')
        context['current_v22general'] = self.request.GET.get('v22general', '')
        context['current_v23town'] = self.request.GET.get('v23town', '')
        
        return context