from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from conferences.models import Conference
from proposals.forms import ProposalForm
from proposals.models import ConferenceProposalSection, ConferenceProposalType, \
    Proposal, ProposalSection, ProposalType


try:
    conference = Conference.objects.get(pk=1)  # TODO: Remove it
except:
    pass  # Create it

def _get_proposal_section_choices():
    return [tuple([str(cps.id), cps.proposal_section.name])
            for cps in ConferenceProposalSection.objects.filter(conference=conference)]

def _get_proposal_type_choices():
    return [tuple([str(cpt.id), cpt.proposal_type.name])
            for cpt in ConferenceProposalType.objects.filter(conference=conference)]

@require_http_methods(['GET'])
def list_proposals(request):
    proposals_list = Proposal.objects.all()
    return render(request, 'proposals/list.html', {'proposals_list' : proposals_list, })

@login_required
@require_http_methods(['GET', 'POST'])
def create_proposal(request):

    if request.method == 'GET':
        form = ProposalForm()
        form.fields['proposal_section'].choices = _get_proposal_section_choices()
        form.fields['proposal_type'].choices = _get_proposal_type_choices()
        return render(request, 'proposals/create.html', {'form':form, })

    form = ProposalForm(request.POST)

    if not form.is_valid():
        form.fields['proposal_section'].choices = _get_proposal_section_choices()
        form.fields['proposal_type'].choices = _get_proposal_type_choices()
        return render(request, 'proposals/create.html', {'form':form, 'errors':form.errors, })

    Proposal.objects.create(author=request.user,
                            conference=conference,
                            title=form.cleaned_data['title'],
                            description=form.cleaned_data['description'],
                            target_audience=form.cleaned_data['target_audience'],
                            prerequisites=form.cleaned_data['prerequisites'],
                            content_urls=form.cleaned_data['content_urls'],
                            speaker_info=form.cleaned_data['speaker_info'],
                            speaker_links=form.cleaned_data['speaker_links'],
                            status=form.cleaned_data['status'],
                            review_status=form.cleaned_data['review_status'],
                            proposal_type=ProposalType.objects.get(id=int(form.cleaned_data['proposal_type'])),
                            proposal_section=ProposalSection.objects.get(id=int(form.cleaned_data['proposal_section'])))

    return HttpResponseRedirect(reverse('proposals-list'))

def detail_proposal(request, proposal_id):
    proposal = Proposal.objects.get(id=proposal_id)  # TODO: Send 404 for incorrect ID
    return render(request, 'proposals/detail.html', {'proposal':proposal, })

@require_http_methods(['GET', 'POST'])
def edit_proposal(request, proposal_id):
    proposal = Proposal.objects.get(id=proposal_id)
    if request.method == 'GET':
        form = ProposalForm(initial={'title':proposal.title,
                                     'description':proposal.description,
                                     'target_audience':proposal.target_audience,
                                     'prerequisites':proposal.prerequisites,
                                     'content_urls':proposal.content_urls,
                                     'speaker_info':proposal.speaker_info,
                                     'speaker_links':proposal.speaker_links,
                                     'status':proposal.status,
                                     })
        form.fields['proposal_section'].choices = _get_proposal_section_choices()
        form.fields['proposal_type'].choices = _get_proposal_type_choices()

        return render(request, 'proposals/edit.html', {'form':form})