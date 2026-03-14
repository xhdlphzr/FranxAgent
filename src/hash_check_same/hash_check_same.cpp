#include <bits/stdc++.h>
#define ull unsigned long long
#define base 131
using namespace std;
string str1,str2;
int w_long;
vector<ull> hash_(string str,int w_long){
	vector<ull> ans;
	ull h=0,p=1;
	for(int i=1;i<=w_long;i++){
		p*=base;
	}
	for(int i=0;i<str.size();i++){
		h=h*base+str[i];
		if(i>=w_long){
			h-=str[i-w_long]*p;
		}
		if(i>=w_long-1){
			ans.push_back(h);
		}
	}
	return ans;
}
int main(){
	freopen("interface_hashcheck.txt","r",stdin);
	getline(cin,str1);
	getline(cin,str2);
	cin>>w_long;
	vector<ull> v1=hash_(str1,w_long);
	vector<ull> v2=hash_(str2,w_long); 
	sort(v1.begin(),v1.end());
	sort(v2.begin(),v2.end());
	int same=0;
	for(int i=0;i<v1.size();i++){
		if(binary_search(v2.begin(),v2.end(),v1[i])){
			same++;
		}
	}
	double ans=2.0*same/(v1.size()+v2.size());
	freopen("interface_hashcheck.txt","w",stdout);
	cout<<fixed<<setprecision(2)<<ans*100<<"%";
	return 0; 
}
