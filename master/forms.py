from django import forms
from .models import *
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission
from authentication.models import User
from django.forms import widgets
from django_select2.forms import Select2MultipleWidget

global form_labels, form_fields
form_labels = {
    'code': 'Code',
    'name_en': 'Name',
    'name_lc': 'नाम',
    'display_order': 'Display Order',
}

form_fields = ('code', 'name_en', 'name_lc', 'display_order')

def check_group(user,group_name):
    return user.groups.filter(name=group_name).exists()

class UploadFileForm(forms.Form):
    file = forms.FileField()

class CustomSelect2MultipleWidget(Select2MultipleWidget):
    # def __init__(self, attrs=None, ajax=None, **kwargs):
    #     super().__init__(attrs, **kwargs)
    #     self.ajax = ajax
    template_name = "widgets/selec2_multiple.html"


class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = "widgets/image_widget.html"

class ProvinceForm(forms.ModelForm):

    class Meta:
        model = Province
        fields = form_fields
        labels = form_labels

    def __init__(self, user=None, *args, **kwargs):
        super(ProvinceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class DistrictForm(forms.ModelForm):

    class Meta:
        model = District
        fields = form_fields[:1]+('province',)+form_fields[1:]
        form_labels.update({'province': 'Province'})
        labels = form_labels

    def __init__(self, user=None, *args, **kwargs):
        super(DistrictForm, self).__init__(*args, **kwargs)
        self.fields['province'].empty_label = "Select Province"
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class LocalLevelTypeForm(forms.ModelForm):
    class Meta:
        model = LocalLevelType
        fields = form_fields
        labels = form_labels

    def __init__(self, user=None, *args, **kwargs):
        super(LocalLevelTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class LocalLevelForm(forms.ModelForm):
    class Meta:
        model = LocalLevel
        fields = form_fields[:1]+('district',
                                  'local_level_type')+form_fields[1:]
        fields = fields[:5]+('wards_count', 'gps_lat', 'gps_long')+fields[5:]

        form_labels.update({'district': 'District',
                            'local_level_type': 'Local Level Type',
                            'wards_count': 'Wards Count',
                            'gps_lat': 'GPS Latitude',
                            'gps_long': 'GPS Longitude'})
        labels = form_labels

    def __init__(self, user=None, *args, **kwargs):
        super(LocalLevelForm, self).__init__(*args, **kwargs)
        self.fields['district'].empty_label = "Select District"
        self.fields['local_level_type'].empty_label = "Select Locallevel Type"
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class FiscalYearForm(forms.ModelForm):
    class Meta:
        model = FiscalYear
        fields = ('code', 'from_date_bs', 'from_date_ad',
                  'to_date_bs', 'to_date_ad', 'display_order')
        form_labels.update({'from_date_bs': 'From Date(B.S)',
                            'from_date_ad': 'From Date(A.D)',
                            'to_date_bs': 'To Date(B.S)',
                            'to_date_ad': 'To Date(A.D)'})
        labels = form_labels
        widgets = {
            'from_date_bs': forms.TextInput(attrs={'class': 'input-nepali-date', 'id': 'from_date_bs', 'relatedId': 'from_date_ad', 'placeholder': 'yyyy-mm-dd', 'onclick': 'fieldDateChange(this)'}),
            'to_date_bs': forms.TextInput(attrs={'class': 'input-nepali-date', 'id': 'to_date_bs', 'relatedId': 'to_date_ad', 'placeholder': 'yyyy-mm-dd', 'onclick': 'fieldDateChange(this)'}),
            'from_date_ad': forms.DateInput(attrs={'id': 'from_date_ad', 'type': 'date'}),
            'to_date_ad': forms.DateInput(attrs={'id': 'to_date_ad', 'type': 'date'})
        }
    def __init__(self, user=None, *args, **kwargs):
        super(FiscalYearForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class NepaliMonthForm(forms.ModelForm):

    class Meta:
        model = NepaliMonth
        fields = form_fields
        labels = form_labels

    def __init__(self, user=None, *args, **kwargs):
        super(NepaliMonthForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class GenderForm(forms.ModelForm):
    class Meta:
        model = Gender
        fields = form_fields
        labels = form_labels

    def __init__(self, user=None, *args, **kwargs):
        super(GenderForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class AppClientForm(forms.ModelForm):
    class Meta:
        model = AppClient
        fields = form_fields[:3]+('province','district','local_level','admin_email')+form_fields[3:]
        form_labels.update({
                            'province': 'Province',
                            'district': 'District',
                            'local_level': 'Local Level',
                            'admin_email': 'Admin E-mail'})
        labels = form_labels
        widgets = {
            'district': forms.Select(attrs={'class': 'district_id', 'id': 'district_id'}),
            'local_level': forms.Select(attrs={'class': 'local_level_id', 'id': 'local_level_id'}),
        }
    def __init__(self, user=None, *args, **kwargs):
        super(AppClientForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('client','name_en', 'name_lc','parent','province','district','local_level',
                    'address','block_no','floor_no','flat_no','room_no','total_area','price',
                    'display_order','photo','own_porperty','is_active','remarks')

        form_labels.update({
                    'client':'Client',
                    'parent':'Parent',
                    'province': 'Province',
                    'district': 'District',
                    'local_level':'Local Level',
                    'address':'Address',
                    'block_no':'Block No',
                    'floor_no':'Floor No',
                    'flat_no':'Flat No',
                    'room_no':'Room No',
                    'total_area':'Total Area',
                    'own_porperty':'Own Porperty?',
                    'price':'Price',
                    'is_active':'Is Active?',
                    'remarks': 'Remarks',
                    'photo':'Property Photo',
                })
        labels = form_labels
        widgets = {
            'district': forms.Select(attrs={'class': 'district_id', 'id': 'district_id'}),
            'local_level': forms.Select(attrs={'class': 'local_level_id', 'id': 'local_level_id'}),
            'photo' : ImageWidget,
            'remarks': forms.Textarea(attrs={'class': 'remarks', 'id': 'remarks','cols':4,'rows':3}),
        }
    def extra():
        return ('code','province','district','local_level','own_porperty','is_active')

    def __init__(self,user=None, *args, **kwargs):

        super(PropertyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'remarks':
                visible.field.widget.attrs['col'] = 'col-md-12'
            else:
                visible.field.widget.attrs['col'] = 'col-md-4'
            # make client hidden if user is client's user
            if(visible.name =='client'):
                if(check_group(user,'Super Admin') is False):
                    visible.field.widget = forms.HiddenInput(attrs={'value':user.app_client_id})

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('client','name_en', 'name_lc','province','district','local_level',
                        'address','contact','secondary_contact','email','display_order','photo')
        form_labels.update({
                    'client':'Client',
                    'province': 'Province',
                    'district': 'District',
                    'local_level':'Local Level',
                    'address':'Address',
                    'contact':'Contact',
                    'secondary_contact':'Secondary Contact',
                    'email':'Email',
                    'photo':'Profile Image'
                })
        labels = form_labels
        widgets = {
            'district': forms.Select(attrs={'class': 'district_id', 'id': 'district_id'}),
            'local_level': forms.Select(attrs={'class': 'local_level_id', 'id': 'local_level_id'}),
            'photo' :ImageWidget,
        }
    def extra():
        return ('code','province','district','local_level')

    def __init__(self,user=None, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            # make client hidden if user is client's user
            if(visible.name =='client'):
                if(check_group(user,'Super Admin') is False):
                    visible.field.widget = forms.HiddenInput(attrs={'value':user.app_client_id})
            if visible.name == 'photo':
                visible.field.widget.attrs['col'] = 'col-md-12'
            else:
                visible.field.widget.attrs['col'] = 'col-md-4'

class BillingCycleForm(forms.ModelForm):
    class Meta:
        model = BillingCycle
        fields = ('name_en', 'name_lc','days_count','display_order')
        form_labels.update({
                    'days_count':'Cycle Days',
                })
        labels = form_labels

    def __init__(self, user=None, *args, **kwargs):
        super(BillingCycleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ('client','province','district','local_level','address','contact','secondary_contact','email','is_active','photo')
        labels = {
            'client':'Client',
            'province':'Province',
            'district':'District',
            'local_level':'Local Level',
            'address':'Address',
            'contact':'Contact',
            'secondary_contact':'Secondary Contact',
            'email':'Email',
            'photo':'Photo',
            'is_active':'Is Active ?',
        }
        widgets = {
            'district': forms.Select(attrs={'class': 'district_id', 'id': 'district_id'}),
            'local_level': forms.Select(attrs={'class': 'local_level_id', 'id': 'local_level_id'}),
            'photo' :ImageWidget,
        }
    def __init__(self, user=None, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

        # make client hidden if user is client's user
        if(visible.name =='client'):
            if(check_group(user,'Super Admin') is False):
                visible.field.widget = forms.HiddenInput(attrs={'value':user.app_client_id})

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ('client','customer','name_en', 'name_lc','property','billing_cycle',
                        'date_from','date_to','rent_amount','increment_year','increment_rate','display_order','contract_file')
        form_labels.update({
                    'client':'Client',
                    'property':'Property',
                    'customer': 'Customer',
                    'billing_cycle': 'Billing Cycle',
                    'contract_file':'Scanned Copy',
                    'date_from':'Date From',
                    'date_to':'Date To',
                    'rent_amount':'Rent Amount',
                    'increment_year':'Increment Year',
                    'increment_rate':'Increment Rate'
                })
        labels = form_labels
        widgets = {
            'contract_file' :ImageWidget,
            'date_from': forms.DateInput(attrs={'id': 'date_from', 'type': 'date'}),
            'date_to': forms.DateInput(attrs={'id': 'date_to', 'type': 'date'}),
        }
    def extra():
        return ('contract_file',)

    def __init__(self,user=None, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'contract_file':
                visible.field.widget.attrs['col'] = 'col-md-12'
            else:
                visible.field.widget.attrs['col'] = 'col-md-4'

            # make client hidden if user is client's user
            if(visible.name =='client'):
                if(check_group(user,'Super Admin') is False):
                    visible.field.widget = forms.HiddenInput(attrs={'value':user.app_client_id})
                    self.fields['property'].queryset =Property.objects.filter(client=user.app_client_id)
                    self.fields['customer'].queryset =Customer.objects.filter(client=user.app_client_id)



class SubPropertyForm(forms.ModelForm):
    class Meta:
        model = SubProperty
        fields = ('name_en', 'name_lc', 'property', 'contract', 'block_no','floor_no','flat_no',
                  'room_no','total_area','display_order','is_active','file','remarks')
        labels = {
            'property': 'Property',
            'contract': 'Contract',
            'block_no': 'Block Nunber',
            'floor_no': 'Floor Number',
            'flat_no': 'Flat Number',
            'room_no': 'Room No',
            'total_area': 'Total Area',
            'remarks': 'Remarks',
            'file': 'File',
            'is_active': 'Is Active ?',
        }
        widgets = {
            'file' :ImageWidget,
            'remarks': forms.Textarea(attrs={'class': 'remarks', 'id': 'remarks','cols':4,'rows':3}),
        }
    def extra():
        return ('file',)

    def __init__(self, user=None, *args, **kwargs):
        super(SubPropertyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'remarks':
                visible.field.widget.attrs['col'] = 'col-md-12'
            else:
                visible.field.widget.attrs['col'] = 'col-md-4'

        if(check_group(user,'Super Admin') is False):
            # get property and contract list only related to customer
            user_properties = Contract.objects.filter(customer=user.customer_id,client=user.app_client_id).values_list('property_id')
            self.fields['property'].queryset =Property.objects.filter(id__in=user_properties)
            self.fields['contract'].queryset =Contract.objects.filter(client=user.app_client_id,customer=user.customer_id,property__in=user_properties)

class EndUserForm(forms.ModelForm):
    class Meta:
        model = EndUser
        fields = ('client','sub_property','province','district','local_level','address','contact','secondary_contact',
                  'email','photo','is_active')
        labels = {
            'client':'Client',
            'sub_property':'Sub Property',
            'province':'Province',
            'district':'District',
            'local_level':'Local Level',
            'address':'Address',
            'contact':'Contact',
            'secondary_contact':'Secondary Contact',
            'email':'Email',
            'photo':'Photo',
            'is_active':'Is Active ?',
        }
        widgets = {
            'district': forms.Select(attrs={'class': 'district_id', 'id': 'district_id'}),
            'local_level': forms.Select(attrs={'class': 'local_level_id', 'id': 'local_level_id'}),
            'photo' : ImageWidget,
        }
    def __init__(self, user=None, *args, **kwargs):
        super(EndUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['app_client','first_name','last_name','email','username','groups']
        labels = {
            'app_client':'Client',
            'first_name':'First Name',
            'last_name':'Last Name',
            'username':'User Name',
            'email':'Email address',
            'groups':'Role',
        }
        widgets = {
            'first_name':forms.TextInput(attrs={'data-min_length':6,'required':'required'}),
        }

    def __init__(self,user=None,*args,**kwargs):
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

        # make client hidden if user is client's user
        if(visible.name =='app_client'):
            if(check_group(user,'Super Admin') is False):
                visible.field.widget = forms.HiddenInput(attrs={'value':user.app_client_id})
        if(check_group(user,'Super Admin') is False):
            self.fields['groups'].queryset = Group.objects.exclude(id__in=[1, 2])

    def extra():
        return ("groups",)

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name','permissions')
        labels = {
            'name':'Role Name',
            'permissions':'permission Name',
        }
        widgets = {
            'permissions': forms.CheckboxSelectMultiple(attrs={'required': True})
        }
    def extra():
        return ("permissions",)

    def __init__(self, user=None, *args, **kwargs):
        super(GroupForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-12'

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('name', 'middle_name', 'surname','province', 'district', 'local_level', 'address', 'contact', 'secondary_contact', 'email', 'photo','property', 'is_active' )
        labels = {
            'name':'Name',
            'middle_name':'Middle Name',
            'surname':'SurName',
            'province':'Province',
            'district':'District',
            'local_level':'Local Level',
            'address':'Address',
            'contact':'Contact',
            'secondary_contact':'Secondary Contact',
            'email':'Email',
            'photo':'Photo',
            'id_no':'ID Number',
            'property':'Property',
            'is_active':'Is Active',
        }
    def __init__(self, user=None, *args, **kwargs):
        super(AgentForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ('property','contract','bill_generated_date','status','billing_cycle','total_amount','paid_amount','pending_amount','fine_amount')
        labels = {
            'property':'Property',
            'contract':'Contract',
            'bill_generated_date':'Bill Date',
            'status':'Status',
            'billing_cycle':'Billing Cycle',
            'total_amount':'Total Amount',
            'paid_amount':'Paid Amount',
            'pending_amount':'Pending Amount',
            'fine_amount':'Fine Amount',
        }

    def __init__(self, user=None, *args, **kwargs):
        super(BillingForm,self).__init__(*args,**kwargs)
        self.fields['property'].widget.attrs['disabled'] = True
        self.fields['contract'].widget.attrs['disabled'] = True
        self.fields['bill_generated_date'].widget.attrs['readonly'] = True
        self.fields['billing_cycle'].widget.attrs['disabled'] = True
        self.fields['total_amount'].widget.attrs['readonly'] = True
        self.fields['pending_amount'].widget.attrs['readonly'] = True
        self.fields['fine_amount'].widget.attrs['readonly'] = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-4'



# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = form_fields[:4]+('remarks',)+form_fields[4:]
#         form_labels.update({'remarks': 'remarks'})
#         labels = form_labels


# class ComplaintTypeForm(forms.ModelForm):
#     class Meta:
#         model = ComplaintType
#         fields = form_fields[:4]+('remarks',)+form_fields[4:]
#         form_labels.update({'remarks': 'remarks'})
#         labels = form_labels


# class ComplaintSeverityForm(forms.ModelForm):
#     class Meta:
#         model = ComplaintSeverity
#         fields = form_fields[:4]+('remarks',)+form_fields[4:]
#         form_labels.update({'remarks': 'remarks'})
#         labels = form_labels


# class ComplaintDetailForm(forms.ModelForm):
#     class Meta:
#         model = ComplaintDetail
#         fields = form_fields[:1]+('complaint_detail_number',
#                                   'client', 'date_bs', 'date_ad', 'province', 'district', 'local_level', 'ward_no', 'tole', 'complaint_type', 'complaint_severity', 'complaint_description', 'file_upload', 'user',)+form_fields[4:]
#         form_labels.update({'complaint_detail_number': 'Complaint Detail Number',
#                             'client': 'Client',
#                             'date_bs': 'Date BS',
#                             'date_ad': 'Date AD',
#                             'province': 'Province',
#                             'district': 'District',
#                             'local_level': 'Local Level',
#                             'ward_no': 'Ward Number',
#                             'tole': 'Tole',
#                             'complaint_type': 'Complaint Type',
#                             'complaint_severity': 'Complaint Severity',
#                             'complaint_description': 'Complaint Description',
#                             'file_upload': 'File Upload',
#                             'user': 'User'
#                             })
#         labels = form_labels
#         widgets = {
#             'date_bs': forms.TextInput(attrs={'class': 'input-nepali-date', 'id': 'date_bs', 'relatedId': 'date_ad', 'placeholder': 'yyyy-mm-dd', 'onclick': 'fieldDateChange(this)'}),
#             'date_ad': forms.DateInput(attrs={'id': 'date_ad', 'type': 'date'}),
#         }


# class ComplaintTransferForm(forms.ModelForm):
#     class Meta:
#         model = ComplaintTransfer
#         fields = ('complaint', 'ministry',
#                   'department', 'remarks', 'is_solved')

#         labels = ({'complaint': 'Complaint',
#                             'ministry': 'Ministry',
#                             'department': 'Department',
#                             'remarks': 'Remarks',
#                             'is_solved': 'Is the problem solved ?'})