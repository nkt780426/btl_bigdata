# HƯỚNG DẪN BUILD K8S CLUSTER

- Project sau triển khai trên môi trường Linux-Ubuntu, hãy chắc chắn máy bạn đang ở môi trường này
- Nếu máy bạn không phải Ubuntu, bạn có thể dùng [wsl2](https://learn.microsoft.com/en-us/windows/wsl/install) hoặc [ubuntu server](https://ubuntu.com/download/server) kết hợp [virtualbox](https://www.virtualbox.org/)
- Hướng dẫn sau cung cấp giải pháp chạy project trên AWS trong khuôn khổ free tier của AWS (cập nhật đến ngày 29/12/2023) hoặc minikube (tuy nhiên bạn vẫn phải có tài khoản aws)
- Tuyên bố miễn trừ trách nhiệm: Chúng tôi không chịu bất kỳ trách nhiệm nào đối với khoản phí phát sinh khi bạn làm theo hướng dẫn sau đây

## Workspace
- Trong linux có 2 loại tài khoản chính là root user và regular user (tài khoản thường), khi thực hiện các lệnh sau hãy chú ý bạn đang dùng tài khoản gì. Cách chuyển đổi giữa 2 loại tài khoản như sau
### Thoát root user
    '''
        exit
    '''
### Đăng nhập root user
    '''
        sudo su
    '''
- Trong regular user hãy cd đến 1 workspaces trống hoặc tạo 1 workspaces mới
'''
    mkdir bigdata_project
    cd bigdata_project
'''
- Hướng dẫn sau sử dụng trình soạn thảo vim mặc định của linux, chi tiết xem tại [đây](https://viblo.asia/p/co-ban-ve-vim-cho-nguoi-moi-bat-dau-GrLZDavnlk0). Về cơ bản bạn chỉ cần phải thực hiện các lệnh :wq! để thoát và lưu thay đổi file hoặc :q! để thoát và không lưu thay đổi file
## Chuẩn bị môi trường và cấu hình
Sử dụng root user cài đặt các pakage sau
### Cài git
'''
    sudo apt-get install git -y
'''
### Clone project trên vào workspace
'''
    git clone https://github.com/nkt780426/btl_bigdata.git
'''
### Project sử dụng phiên bản oracle-java 17 và apache spark 3.5.0. Nếu bạn muốn thay đổi phiên bản sửa đoạn [java](https://www.oracle.com/java/technologies/downloads/) và [apache spark](https://spark.apache.org/downloads.html) chỉ cần thay đổi trong đoạn mã prebuild.sh. Sau thay đổi tiến hành chạy đoạn mã sau ở workspace với root user
'''
    # 
    cd build
    chmod +x prebuild.sh
    
    # Trong quá trình chạy chọn phiên bản java 17 đã cài
    ./prebuild.sh    
'''
### Tạo AWS_ACCESS_KEY và AWS_SECRET_KEY
- Truy cập vào trang chủ [aws](https://aws.amazon.com/) và đăng nhập
- Chọn vào tài khoản trên giao diện => Security credentials
- Lướt xuống dưới tại mục access key và tạo chúng, hãy download về và giữ nó bí mật cho bản thân

### Cài Docker. Nếu bạn sử dụng wsl2 và đã cài docker trên windows rồi thì không cần cài nữa, vì bản docker đã sử dụng wsl2. Nếu bạn không có xem cách cài đặt tại [đây](https://docs.docker.com/desktop/install/windows-install/)


## Tạo cụm k8s
### Sử dụng minikube
Lý thuyết

- Việc bạn sử dụng minikube để triển khai cụm k8s là không thực tế khi đi làm, vì cách này chỉ build cụm k8s trên 1 node/host duy nhất không phản ánh khả năng kết hợp nhiều host để tạo thành cụm k8s có khả năng xử lý cao. Tuy nhiên nhược điểm của nó chỉ có vậy, khi bạn build thành công cụm k8s mọi thao tác của project sau đều hoạt động. Ưu điểm của giải pháp này, là việc học tập cách triển khai 1 ứng dụng trên môi trường k8s thực tế (việc sau đây chúng ta sẽ làm) cũng như học các câu lệnh kubectl để quản lý tài nguyên k8s trong môi trường prodcution

Chuẩn bị

- Tải minikube về, xem tại [đây](https://kubernetes.io/vi/docs/tasks/tools/install-minikube/)

Tạo cụm k8s
- Triển khai cụm k8s trên regular user
    '''
        # 1 khi đã start cụm thì sẽ không thể cung cấp tài nguyên hãy chắc chắn cung cấp đủ tài nguyên khi start minikube
        minikube start --cpu=<your cpu size> --memory=<your mem size> --disk=<your disk size>

        # Ở đây chúng tôi start mặc định
        minikube start
    '''
Kiểm tra
    '''
        # Câu lệnh sau sẽ hiện ra số node có được sử dụng tạo cụm k8s và bạn sẽ chỉ thấy 1 node tên minikube
        kubectl get nodes
    '''
### Sử dụng kops

Lý thuyết

- Giống như eks, gks, ... Kops là 1 kubernetes operators dùng để tạo cụm k8s 1 cách tự động. 
- Ưu điểm kops: Có thể tạo cụm k8s trên nhiều clouds provider khác nhau thậm chí on-primise. Các tool như eks, gks, ... chỉ tạo được cụm k8s trên chính cloud provider của họ, không có khả năng build cụm k8s đa nền tảng. Ngoài ra phiên bản kuberneter cài đặt là phiên bản free trên github, bạn không cần phải trả bất kỳ khoản phí nào liên quan đến kubernetes operator, nếu sử dụng các tool khác họ sẽ cài phiên bản kuberneter của riêng họ. Các tool tương tự kops: kubeadm (không hay dùng nữa vì không tạo cụm k8s auto mà phải config rất nhiều)
- Nhược điểm: Bạn phải tự quản lý cụm k8s của mình mà không nhận được sự hỗ trợ từ cloud provider

Chuẩn bị

- Tải kops tại [đây](https://kops.sigs.k8s.io/install/)
- Tải aws cli về, chi tiết xem tại [đây](https://aws.amazon.com/vi/cli/)
- Cấu hình aws cli
'''
    # Chạy lệnh sau và làm theo hướng dẫn, chú ý set miền đúng với tài khoản aws của bạn, nếu không khả năng cao bạn sẽ mất phí dù thực hiện service free của aws
    aws configure
'''
- Bạn có thể giữ nguyên tài khoản root của aws trong aws cli, hoặc tạo tài khoản IAM user của aws để giới hạn quyền sử dụng tài khoản
'''
    # Tạo tài khoản IAM
    aws iam create-group --group-name kops

    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess --group-name kops
    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonRoute53FullAccess --group-name kops
    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --group-name kops
    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/IAMFullAccess --group-name kops
    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonVPCFullAccess --group-name kops
    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonSQSFullAccess --group-name kops
    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonEventBridgeFullAccess --group-name kops

    aws iam create-user --user-name kops

    aws iam add-user-to-group --user-name kops --group-name kops

    aws iam create-access-key --user-name kops
    
    # Kết quả trả về là 1 json chứa AWS_ACCESS_KEY và AWS_SECRET_KEY của tài khoản IAM
    # Cấu hình lại aws cli bằng tài khoản này bằng lệnh
    aws configure
'''
- Kiểm tra tên các zones trong region hiện tại có thể deploy k8s và chọn 1 cái bất kỳ, gần bạn nhất càng tốt
- Ví dụ region của tôi là ap-southeast-2 và có 3 zones ap-southeast-2a, ap-southeast-2b, ap-southeast-2c có thể tạo cụm k8s
'''
    aws ec2 describe-availability-zones --region <your regions>
'''

Tạo cụm k8s

- Kops sử dụng s3 bucket để lưu config của cụm k8s
'''
    aws s3api create-bucket \
    --bucket <tự tạo tên bucket> \
    --region <your region>
'''
- Tạo biến môi trường cho terminal session, khi chạy lệnh sau đảm bảo không tắt terminal này cho đến khi tạo xong cụm k8s trên aws
'''
    export NAME=<your cluster name> (ex: google.com, mycluser.k8s.local, bừa-tên.net .....)
    export KOPS_STATE_STORE=s3://<tên s3 bucket đã tạo>
    export ZONE=<Tến zone đã chọn>
'''
- Tạo cụm k8s: câu lệnh sau chỉ tạo cấu hình cụm k8s rồi lưu tại s3, nó vẫn chưa thực sự triển khai cụm k8s trên cloud nên bạn không cần lo lắng. Đợi tầm 5 phút để nó tạo
'''
    kops create cluster \
    --name=${NAME} \
    --cloud=aws \
    --zones={ZONE} \
    --discovery-store={KOPS_STATE_STORE}
    --authorization=AlwaysAllow
'''
- Sau khi tạo thành công, kops sẽ gợi ý cho bạn 3 câu lệnh chỉnh sửa cấu hình cụm k8s và 1 câu lệnh update để triển khai k8s thật
Hãy sử dụng những câu lệnh đó thay vì những câu lệnh sau để chỉnh sửa cấu hình cụm k8s cho hợp lý trước khi thực sự triển khai
'''
    # Chỉnh sửa metadata (câu lệnh họ cung cấp sẽ tương tự thế này)
    kops edit cluster --name ${NAME}
    # Chỉnh sửa cấu hình control plane/master node về t2.micro để miễn phí, ngoài ra bạn có thể điều chỉnh số lượng theo ý muốn
    kops edit 
    # Chỉnh sửa cấu hình node groud/worker về t2.micro để miễn phí, ngoài ra bạn có thể điều chỉnh số lượng node theo ý muốn
    kops edit
    # Sau khi chắc chắn sửa đổi cấu hình như mong muốn, tiến hành triển khai cụm k8s trên aws
    kops update cluster --name ${NAME} --yes --admin
'''
- Việc tạo cụm k8s có thể mất tầm 5-7 phút. Bạn có thể sử dụng câu lệnh sau để kops báo lại kết quả sau khi build cụm
'''
    kops validate cluster --wait 10m
'''
- Hướng dẫn này chỉ thực hiện được trước ngày 29/12/2023, nếu sau 10 phút không có chuyển biến, bạn có thể đã thất bại. Vào trang chủ của kops hoặc sử dụng chatgpt hoặc sử dụng stack over flow để biết thêm thông tin chi tiết về lỗi của mình

Kiếm tra
'''
    # Bạn có thể tạo ra bao nhiêu cụm k8s. Sử dụng lệnh sau để kiểm tra tên tất cả các cụm k8s đã tạo
    # Chú ý nó lấy thông tin về các cụm k8s trên s3 bucket đã tạo, nếu bạn tạo các cụm kops trên các s3 bucket khác nhau, bạn sẽ không thể kiểm tra được, hãy chắc chắn bạn đã chọn đúng nơi lưu trữ k8s cluster config
    kops get clusters

    # Kiểm tra kubectl có trỏ về chính xác cụm k8s bạn muốn kiểm soát không
    kubectl congfig current-context

    # Thiết lập Kubectl context trỏ về chính xác cụm k8s bạn muốn kiểm soát
    kops export kubecfg --name=your-cluster-name

    # Kiểm tra số node của cụm
    kubectl get nodes
'''
# Triển khai cơ sở hạ tầng trên k8s
Từ bước này trở đi gần như không có sự khác biệt giữa việc triển khai cụm k8s bằng bất kỳ công cụ gì
- Tải repo bitnami về
'''
    helm repo add bitnami https://charts.bitnami.com/bitnami
''' 
- Cài đặt cụm kafka với 2 broker và 1 topic có 2 partition
'''
    kubectl create namespace apache-kafka
    helm install apache-kafka bitnami/kafka -n apache-kafka -f kafka-values.yaml
'''
- Cài đặt cụm apache spark với 1 master node và 2 worker node
'''
    kubectl create namespace apache-spark
    helm install apache-spark bitnami/spark -n apache-spark -f spark-values.yaml
'''
- Cài đặt prometheus và grapana
'''
    kubectl create namespace monitoring
    helm install prometheus bitnami/prometheus -n monitoring -f prometheus-values.yaml
    helm install grafana bitnami/grafana -n monitoring -f grafana-values.yaml
'''
- Cài đặt elasticsearch và kibana
'''
    kubectl create namespace elk-stack
    helm install elasticsearch bitnami/elasticsearch -n elk-stack -f elasticsearch-values.yaml
    helm install kibana bitnami/kibana -n elk-stack -f kibana-values.yaml
'''
# Expose service ra internet
Sử dụng nginx làm load balancer
Tạo 
### Nếu bạn triển khai cụm k8s bằng minikube
- Minikube không có khả năng expose web ra open internet. Tuy nhiên bạn có thể tự tạo 1 địa chỉ ở local và sử dụng nó tại local
- Tạo host name
'''
    # Lấy địa chỉ ip của cụm k8s minikube
    minikube ip
    # Dùng root user mở file, nếu không có thì tạo
    vi /etc/hosts
    # Copy dòng sau vào file và lưu lại (mặc định DNS là example.com)
    <minikube ip> <DNS bạn muốn>
    # Sư dụng ingress controller
    minikube addons enable ingress
    # Đợi 1 lúc và kiểm tra lại ingress controller đã chạy chưa
    kubectl get pods -n ingress-nginx
'''
- Điều chỉnh lại tên host theo DNS trong file ingress mà bạn đã cài, sau đó tạo ingress resource trên k8s
'''
    kubectl apply -f ingress.yaml
'''
### Nếu bạn triển khai cụm k8s bằng kops
- Thêm nginx controller vào cụm k8s
'''
    # Thêm repo helm cho nginx ingress
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

    # Cài đặt nginx ingress controller
    helm install my-release ingress-nginx/ingress-nginx
'''
- Lấy địa chỉ của loadbalancer
'''
    # Tìm đến ingress service, bạn sẽ thấy ip ở code EXTERNAL-IP (chỉ có 1 service có nó nếu bạn chỉ triển khai 1 ingress controller)
    kubectl get services -o wide
'''
- Sau khi có địa chỉ ip của cụm k8s, làm theo hướng dẫn [sau](https://www.youtube.com/watch?v=0bmopLboeIc&t=30s) để tạo được subdomain free
- Điều chỉnh lại tên host theo DNS trong file ingress mà bạn đã cài, sau đó tạo ingress resource trên k8s
'''
    kubectl apply -f ingress.yaml
'''
# Submit job lên cụm apache spark
- Kiểm tra bạn có quyền tạo pod từ terminal của mình không
'''
    kubectl auth can-i create pods
'''
- Nếu bạn không có quyền xem lại bạn đang sử dụng root user hay regular user. Hoặc nếu bạn sử dụng kops, xem lại bạn có cấu hình aws cli đúng tài khoản có quyền tạo pod không
- Khi bạn đã có quyền, chạy file sau
'''
    source .bash_profile
'''
- Submit đoạn code spark-streaming lên cụm apache spark và đoạn code crawl lên cụm k8s
'''
    kubectl apply -f crawl-deployment.yaml
'''
# Kiểm tra kết quả
