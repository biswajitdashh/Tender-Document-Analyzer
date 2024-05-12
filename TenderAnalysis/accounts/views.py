from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import fitz
import openai
import re
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration/login.html', {})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully. You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def dashboard_view(request):
    context = {'processed_text': None}
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        global test_path
        test_path=pdf_file

        uploads_dir = 'uploads'
        fs = FileSystemStorage(location=uploads_dir)
        filename = fs.save(pdf_file.name, pdf_file)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        request.session['uploaded_file_url'] = uploaded_file_url

        def extract_text_from_pdf(pdf_path=uploaded_file_url):
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        extracted_text = extract_text_from_pdf(fs.path(filename))

        def find_dates(text):
            # Regular expression to match various date formats, adjusted for extra spaces
            date_patterns = [
                # Matches dates like "8th May 1987" with optional ordinal indicators and variable spacing
                r'\b(\d{1,2}(?:st|nd|rd|th)?)\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4}\b',
                # Matches dates with slashes "10/03/2002" allowing spaces around slashes
                r'\b(\d{1,2})\s*/\s*(\d{1,2})\s*/\s*(\d{2,4})\b',
                # Matches various date formats with dashes, like "10-03-2002", allowing spaces around dashes
                r'\b(\d{1,2})\s*-\s*(\d{1,2})\s*-\s*(\d{2,4})\b',
                # Matches month names followed by day and year with variable spacing and optional commas
                r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{2,4}\b',
                # Matches weekdays, month names, day and year with variable spacing and optional commas
                r'\b(?:Mon(?:day)?|Tue(?:sday)?|Wed(?:nesday)?|Thu(?:rsday)?|Fri(?:day)?|Sat(?:urday)?|Sun(?:day)?)\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{2,4}\b',
                # Specifically for capturing dates with irregular spaces like "2006 - 06 - 16"
                r'\b(\d{4})\s*-\s*(\d{2})\s*-\s*(\d{2})\b',
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
                # "April 2006"

            ]

            dates_only = []
            for pattern in date_patterns:
                for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                    found_date = match.group(0)
                    dates_only.append(found_date)

            return dates_only

        dates = find_dates(extracted_text)
        cleaned_set = set(date.replace('\n', '') for date in dates)
        def process_text_with_chatgpt (extracted_text,dates):
            all_dates_information = {}
            for date in dates:

                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Behave like an analyst."},
                        {"role": "user", "content": extracted_text},
                        {"role": "assistant", "content": "Summarise the information"},
                        {"role": "user",
                         "content": "tell me what happened on the date of " + str(date) + " short and precise manner"}
                    ])
                all_dates_information[date] = response.choices[0].message.content
            return all_dates_information
        processed_text = process_text_with_chatgpt(extracted_text=extracted_text,dates=list(cleaned_set))
        request.session['processed_text'] = processed_text
        context['processed_text'] = processed_text
        return redirect('processed_info')
    return render(request, 'dashboard.html', context)

def processed_info_view(request):
    # Retrieve the processed text and any other necessary data
    #processed_text = ...  # Retrieve processed text from session or database
    processed_text = request.session.get('processed_text', None)
    pdf_url = request.session.get('uploaded_file_url', None)
    #pdf_url="C:/Users/chuck/TenderDocExtraction/TenderAnalysis/uploads/360_degree_camera_mc_medium_complexity_july20171_1[1].pdf"
    #pdf_url="https://research.google.com/pubs/archive/44678.pdf"#testing for URLS after uploading in S3
    # global test_path
    # pdf_url=test_pat

    if processed_text is None:
        return render(request, 'error.html', {'message': 'No processed text found. Please upload and process a PDF first.'})
    # Render the template with the processed information
    return render(request, 'processed_info.html', {'processed_text': processed_text, 'pdf_url': pdf_url})


