from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from .models import AWSCredential
import boto3
from botocore.exceptions import NoCredentialsError, ClientError, EndpointConnectionError

def home(request):
    """Render the home page."""
    return render(request, 'myapp/home.html')

def about(request):
    """Render the about page."""
    return render(request, 'myapp/about.html')

@csrf_protect
def register_view(request):
    """Handle user registration."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')
    return render(request, 'myapp/register.html')

@csrf_protect
def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('credentials')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'myapp/login.html')

@login_required
def logout_view(request):
    """Log out the user and clear the session."""
    logout(request)
    request.session.flush()
    return redirect('home')

@login_required
@csrf_protect
def credentials_view(request):
    """Handle AWS credentials management."""
    error_message = None
    if request.method == 'POST':
        access_key_id = request.POST.get('access')
        secret_access_key = request.POST.get('secret')
        print(f'Received credentials: {access_key_id}')
        
        # Verify credentials by attempting a simple AWS operation
        try:
            session = boto3.Session(
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name='us-west-2'
            )
            print('Session created successfully.')
            ec2_client = session.client('ec2')
            print('EC2 client created successfully.')
            ec2_client.describe_regions()
            print('describe_regions call successful.')
            
            # If successful, save the credentials
            AWSCredential.objects.create(
                user=request.user,
                access_key_id=access_key_id,
                secret_access_key=secret_access_key
            )
            print('AWS credentials saved successfully.')
            messages.success(request, 'AWS credentials added successfully.')
            return redirect('profile')
        except (NoCredentialsError, ClientError, EndpointConnectionError) as e:
            print(f'Error verifying AWS credentials: {e}')
            messages.error(request, f'Invalid AWS credentials: {e}')
    
    print('Rendering credentials form.')
    return render(request, 'myapp/credentials.html', {'error_message': error_message})

@login_required
def profile_view(request):
    """Display user profile with AWS credentials."""
    credentials = AWSCredential.objects.filter(user=request.user)
    return render(request, 'myapp/profile.html', {'credentials': credentials})

@login_required
def delete_credential(request, cred_id):
    """Delete a specific AWS credential."""
    credential = get_object_or_404(AWSCredential, id=cred_id, user=request.user)
    credential.delete()
    messages.success(request, 'Credential deleted successfully.')
    return redirect('profile')

@login_required
def app_view(request):
    """Fetch and display AWS instances for the authenticated user."""
    aws_credentials = AWSCredential.objects.filter(user=request.user)
    if not aws_credentials:
        messages.error(request, 'No AWS credentials found')
        return redirect('credentials')

    try:
        instances = []
        for credential in aws_credentials:
            access_key = credential.get_access_key_id()
            secret_key = credential.get_secret_access_key()
            instances.extend(get_instances_from_all_zones(access_key, secret_key))
        return render(request, 'myapp/app.html', {'instances': instances})
    except (NoCredentialsError, ClientError) as e:
        messages.error(request, f'Error fetching instances: {e}')
        return render(request, 'myapp/app.html')

def get_instances_from_all_zones(aws_access_key_id, aws_secret_access_key):
    """Fetch EC2 instances from all availability zones using provided AWS credentials."""
    try:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='us-west-2'
        )
        ec2_client = session.client('ec2')
        regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
        instances = []
        for region in regions:
            ec2_client = session.client('ec2', region_name=region)
            response = ec2_client.describe_instances()

            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_details = {
                        'InstanceId': instance['InstanceId'],
                        'InstanceType': instance['InstanceType'],
                        'State': instance['State']['Name'],
                        'OwnerId': reservation.get('OwnerId', ''),
                        'AvailabilityZone': instance['Placement']['AvailabilityZone'],
                        'ImageId': instance['ImageId'],
                        'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                        'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                        'Platform': instance.get('Platform', 'Linux'),
                        'Tenancy': instance['Placement']['Tenancy'],
                        'Architecture': instance['Architecture'],
                        'CapacityReservationId': instance.get('CapacityReservationId', 'N/A'),
                        'CurrentInstanceBootMode': instance.get('CurrentInstanceBootMode', 'N/A'),
                        'DnsName': instance.get('PublicDnsName', 'N/A'),
                        'EbsOptimized': instance.get('EbsOptimized', False),
                        'EnaSupport': instance.get('EnaSupport', False),
                        'HostId': instance.get('HostId', 'N/A'),
                        'IamInstanceProfile': instance.get('IamInstanceProfile', {}).get('Arn', 'N/A'),
                        'InstanceLifecycle': instance.get('InstanceLifecycle', 'N/A'),
                        'SecurityGroups': [sg['GroupName'] for sg in instance.get('SecurityGroups', [])],
                        'LaunchTime': instance['LaunchTime'],
                        'MonitoringState': instance.get('Monitoring', {}).get('State', 'N/A'),
                        'NetworkInterfaces': [ni['NetworkInterfaceId'] for ni in instance.get('NetworkInterfaces', [])],
                        'PlacementGroupName': instance.get('Placement', {}).get('GroupName', 'N/A'),
                        'PlatformDetails': instance.get('PlatformDetails', 'N/A'),
                        'ProductCodes': [pc['ProductCodeId'] for pc in instance.get('ProductCodes', [])],
                        'ReservationId': reservation['ReservationId'],
                        'RootDeviceType': instance['RootDeviceType'],
                        'SpotInstanceRequestId': instance.get('SpotInstanceRequestId', 'N/A'),
                        'SubnetId': instance.get('SubnetId', 'N/A'),
                        'TpmSupport': instance.get('TpmSupport', 'N/A'),
                        'UsageOperation': instance.get('UsageOperation', 'N/A'),
                        'VpcId': instance.get('VpcId', 'N/A'),
                        'Region': region,
                        'KeyName': instance.get('KeyName'),
                        'AccountID': reservation.get('OwnerId'),
                        'BlockDeviceMapping': [
                                        {
                                            'DeviceName': bd.get('DeviceName', ''),
                                            'VolumeId': bd.get('Ebs', {}).get('VolumeId', '')
                                        } for bd in instance.get('BlockDeviceMappings', [])
                        ],
                        'MetadataOptions': {
                                        'HttpEndpoint': instance.get('MetadataOptions', {}).get('HttpEndpoint', ''),
                                        'HttpTokens': instance.get('MetadataOptions', {}).get('HttpTokens', '')
                        },
                    }

                    instances.append(instance_details)
        return instances
    except (NoCredentialsError, ClientError, EndpointConnectionError) as e:
        raise e
